# Honey-Pot API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

All API requests require authentication using an API key in the request header.

**Header:**
```
x-api-key: your-api-key-here
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Invalid or missing API key"
}
```

---

## Endpoints

### 1. Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /health`

**Authentication:** Not required

**Response:**
```json
{
  "status": "healthy",
  "service": "honeypot-api"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

---

### 2. Process Message

Main endpoint to receive and process suspected scam messages.

**Endpoint:** `POST /api/message`

**Authentication:** Required (x-api-key header)

**Content-Type:** `application/json`

#### Request Body

```json
{
  "sessionId": "string",
  "message": {
    "sender": "scammer" | "user",
    "text": "string",
    "timestamp": number
  },
  "conversationHistory": [
    {
      "sender": "scammer" | "user",
      "text": "string",
      "timestamp": number
    }
  ],
  "metadata": {
    "channel": "SMS" | "WhatsApp" | "Email" | "Chat",
    "language": "string",
    "locale": "string"
  }
}
```

#### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| sessionId | string | Yes | Unique identifier for the conversation session |
| message.sender | string | Yes | Either "scammer" or "user" |
| message.text | string | Yes | The message content |
| message.timestamp | number | Yes | Unix timestamp in milliseconds |
| conversationHistory | array | Yes | Array of previous messages (empty for first message) |
| metadata.channel | string | Yes | Communication channel |
| metadata.language | string | Yes | Message language |
| metadata.locale | string | Yes | Locale code (e.g., "IN") |

#### Response

```json
{
  "status": "success",
  "reply": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| status | string | Always "success" |
| reply | string | Human-like response to the message |

#### Example Request

```bash
curl -X POST http://localhost:8000/api/message \
  -H "x-api-key: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "session-123",
    "message": {
      "sender": "scammer",
      "text": "Your account will be blocked. Update KYC immediately by clicking this link.",
      "timestamp": 1770005528731
    },
    "conversationHistory": [],
    "metadata": {
      "channel": "SMS",
      "language": "English",
      "locale": "IN"
    }
  }'
```

#### Example Response

```json
{
  "status": "success",
  "reply": "Why will my account be blocked? Which bank is this?"
}
```

---

## Conversation Flow

### First Message
- `conversationHistory` is empty array `[]`
- System detects scam intent
- Returns initial human-like response

### Subsequent Messages
- Include all previous messages in `conversationHistory`
- System continues conversation naturally
- Extracts intelligence from messages
- Decides when to end engagement

### Example Multi-Turn Conversation

**Turn 1:**
```json
{
  "sessionId": "abc123",
  "message": {
    "sender": "scammer",
    "text": "Your account will be blocked. Update KYC now.",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": { "channel": "SMS", "language": "English", "locale": "IN" }
}
```
Response: `"Why will my account be blocked?"`

**Turn 2:**
```json
{
  "sessionId": "abc123",
  "message": {
    "sender": "scammer",
    "text": "Due to pending verification. Click here: http://fake-bank.com",
    "timestamp": 1770005530000
  },
  "conversationHistory": [
    {
      "sender": "scammer",
      "text": "Your account will be blocked. Update KYC now.",
      "timestamp": 1770005528731
    },
    {
      "sender": "user",
      "text": "Why will my account be blocked?",
      "timestamp": 1770005529000
    }
  ],
  "metadata": { "channel": "SMS", "language": "English", "locale": "IN" }
}
```
Response: `"The link is not opening. Can you send it again?"`

---

## Callback Endpoint

When engagement completes, the system automatically sends results to:

**URL:** `https://hackathon.guvi.in/api/updateHoneyPotFinalResult`

**Method:** `POST`

**Payload:**
```json
{
  "sessionId": "string",
  "scamDetected": boolean,
  "totalMessagesExchanged": number,
  "extractedIntelligence": {
    "bankAccounts": ["string"],
    "upiIds": ["string"],
    "phishingLinks": ["string"],
    "phoneNumbers": ["string"],
    "suspiciousKeywords": ["string"]
  },
  "agentNotes": "string"
}
```

### Example Callback Payload

```json
{
  "sessionId": "abc123",
  "scamDetected": true,
  "totalMessagesExchanged": 12,
  "extractedIntelligence": {
    "bankAccounts": ["123456789012"],
    "upiIds": ["scammer@paytm"],
    "phishingLinks": ["http://fake-bank.com/verify"],
    "phoneNumbers": ["9876543210"],
    "suspiciousKeywords": ["kyc", "blocked", "urgent", "verify"]
  },
  "agentNotes": "Banking/KYC scam attempt. Extracted: 1 bank account(s), 1 UPI ID(s), 1 phishing link(s). Engaged over 12 messages. High urgency tactics used."
}
```

---

## Error Handling

### 400 Bad Request
Invalid request format or missing required fields.

```json
{
  "detail": [
    {
      "loc": ["body", "sessionId"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 401 Unauthorized
Missing or invalid API key.

```json
{
  "detail": "Invalid or missing API key"
}
```

### 500 Internal Server Error
Server error. The API will still return a safe response:

```json
{
  "status": "success",
  "reply": "Sorry, I didn't quite understand. Could you explain again?"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production:
- Recommended: 100 requests per minute per IP
- Implement using nginx or application-level middleware

---

## Best Practices

### Session Management
- Use unique `sessionId` for each conversation
- Include complete `conversationHistory` in each request
- Don't reuse session IDs across different conversations

### Message Timestamps
- Use Unix timestamp in milliseconds
- Ensure timestamps are sequential
- Current time: `Date.now()` in JavaScript or `int(time.time() * 1000)` in Python

### Error Handling
- Always check response status code
- Handle network timeouts gracefully
- Retry failed requests with exponential backoff

### Security
- Keep API key secure
- Use HTTPS in production
- Don't log sensitive data
- Validate all inputs

---

## Testing

### Using cURL

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Send Message:**
```bash
curl -X POST http://localhost:8000/api/message \
  -H "x-api-key: your-api-key" \
  -H "Content-Type: application/json" \
  -d @test_message.json
```

### Using Python

```python
import requests

url = "http://localhost:8000/api/message"
headers = {
    "x-api-key": "your-api-key",
    "Content-Type": "application/json"
}
payload = {
    "sessionId": "test-123",
    "message": {
        "sender": "scammer",
        "text": "Your account will be blocked.",
        "timestamp": 1770005528731
    },
    "conversationHistory": [],
    "metadata": {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
    }
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Using the Test Script

```bash
python test_api.py
```

This runs a complete scam conversation simulation.

---

## Scam Detection

The system detects scams using:

### Keyword Matching
- Banking urgency: "account blocked", "KYC update"
- Prize scams: "won", "lottery", "claim prize"
- Phishing: "click here", "enter OTP", "share password"
- Payment requests: "send money", "transfer amount"
- Impersonation: "bank official", "customer care"
- Threats: "legal action", "police complaint"

### Context Escalation
- Multiple suspicious keywords
- URLs/links with urgency
- Progressive pressure tactics
- Request for sensitive information

### Confidence Levels
- **High**: 2+ keyword matches
- **Medium**: 1 keyword + escalation patterns
- **Low**: Suspicious link + 1 keyword

---

## Intelligence Extraction

### Bank Accounts
- Pattern: 9-18 digit sequences
- Validation: Length and format checks

### UPI IDs
- Pattern: `username@bank`
- Validation: Contains @ symbol, valid format

### Phone Numbers
- Pattern: Indian mobile numbers (10 digits)
- Format: With or without country code (+91)

### URLs
- Pattern: HTTP/HTTPS links
- Includes: Domain-only references (www.example.com)

### Keywords
- Tracks: Urgency, threats, phishing terms
- Categories: Banking, payment, verification

---

## Agent Behavior

### Persona
- Middle-aged, not tech-savvy
- Worried but cooperative
- Asks clarification questions
- Reports technical issues

### Response Strategy
- Keep replies short (1-2 sentences)
- Ask questions to extract info
- Pretend links don't work
- Express confusion naturally
- Never reveal detection

### Example Responses
- "Why will my account be blocked?"
- "Which bank is this?"
- "The link is not opening."
- "What should I enter?"
- "How do I verify this is real?"

---

## Engagement Termination

The system ends engagement when:

1. **Minimum messages reached** (default: 8)
2. **Sufficient intelligence gathered** (default: 2+ items)
3. **Maximum messages reached** (default: 25)
4. **Conversation stalling** (very short responses)

After termination:
- Final callback is sent
- Session marked as complete
- Further messages still get responses

---

## Configuration

Environment variables control behavior:

| Variable | Default | Description |
|----------|---------|-------------|
| MIN_MESSAGES_BEFORE_END | 8 | Minimum messages before callback |
| MAX_MESSAGES_PER_SESSION | 25 | Maximum messages per session |
| MIN_INTELLIGENCE_ITEMS | 2 | Minimum intelligence to gather |
| LLM_MODEL | gpt-4o-mini | OpenAI model to use |
| LLM_TEMPERATURE | 0.7 | Response randomness (0-1) |
| LLM_MAX_TOKENS | 150 | Maximum response length |

---

## Support & Troubleshooting

### Common Issues

**"Invalid API key"**
- Check x-api-key header is set
- Verify API key matches .env file

**"Connection refused"**
- Ensure server is running
- Check port 8000 is not in use

**"OpenAI API error"**
- Verify OPENAI_API_KEY is set
- Check API quota and billing

**Slow responses**
- OpenAI API latency (normal)
- Consider using faster model
- Check network connectivity

### Debug Mode

Enable debug logging:
```bash
DEBUG=True python run.py
```

### Logs

Check logs for detailed information:
```bash
# View recent logs
tail -f logs/app.log

# Search for errors
grep ERROR logs/app.log
```

---

## Changelog

### Version 1.0.0
- Initial release
- Scam detection with keyword matching
- Autonomous AI agent
- Intelligence extraction
- GUVI callback integration
- Multi-turn conversation support
