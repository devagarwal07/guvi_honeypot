# Agentic Honey-Pot for Scam Detection & Intelligence Extraction

Production-ready backend system that detects scam messages and engages scammers using an autonomous AI agent to extract actionable intelligence.

## Features

- **REST API** with x-api-key authentication
- **Scam Intent Detection** using keyword matching and context escalation
- **Autonomous AI Agent** that behaves like a real human
- **Multi-turn Conversation** management with session state
- **Intelligence Extraction** (bank accounts, UPI IDs, phishing URLs, phone numbers)
- **Mandatory Callback** to evaluation endpoint
- **Production-ready** with proper error handling and logging

## Architecture

```
honeypot/
├── app.py                     # FastAPI entry point
├── auth.py                    # API key validation
├── config.py                  # Environment configuration
├── detector/
│   └── scam_classifier.py     # Scam intent detection
├── agent/
│   ├── persona.py             # AI agent prompts
│   └── agent_controller.py    # Agent decision logic
├── extractor/
│   └── intelligence.py        # Intelligence extraction
├── sessions/
│   └── memory_store.py        # Session state management
├── callbacks/
│   └── guvi_client.py         # Final callback sender
└── utils/
    └── validators.py          # Input validation
```

## Installation

1. **Install dependencies:**
```bash
cd honeypot
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

Required environment variables:
- `API_KEY`: Your API key for securing the endpoint
- `OPENAI_API_KEY`: OpenAI API key for the AI agent

## Running the Server

```bash
python app.py
```

Or with uvicorn directly:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## API Usage

### Endpoint: POST /api/message

**Headers:**
```
x-api-key: your-api-key-here
Content-Type: application/json
```

**Request Body:**
```json
{
  "sessionId": "unique-session-id",
  "message": {
    "sender": "scammer",
    "text": "Your account will be blocked. Click here to verify KYC",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "reply": "Why will my account be blocked? Which bank is this?"
}
```

## How It Works

1. **Message Reception**: API receives incoming message with session context
2. **Scam Detection**: Analyzes message for scam indicators using keywords and patterns
3. **Agent Engagement**: Once scam detected, AI agent takes over and generates human-like replies
4. **Intelligence Extraction**: Extracts bank accounts, UPI IDs, URLs, phone numbers from messages
5. **Conversation Management**: Tracks message count and intelligence gathered
6. **Final Callback**: When engagement complete, sends results to evaluation endpoint

## Agent Behavior

The AI agent:
- Sounds worried and cooperative
- Asks clarification questions naturally
- Pretends to face technical issues
- Extracts details without revealing detection
- Maintains believable human persona

Example agent replies:
- "Why will my account be blocked?"
- "The link is not opening. Can you send it again?"
- "Which bank is this? I have multiple accounts."
- "It's asking for UPI ID. What should I enter?"

## Intelligence Extraction

Automatically extracts:
- **Bank Account Numbers**: 9-18 digit sequences
- **UPI IDs**: username@bank format
- **Phishing URLs**: HTTP/HTTPS links and domains
- **Phone Numbers**: Indian mobile numbers
- **Suspicious Keywords**: Urgency, threats, phishing terms

## Final Callback

When engagement completes, sends to:
```
POST https://hackathon.guvi.in/api/updateHoneyPotFinalResult
```

Payload:
```json
{
  "sessionId": "abc123",
  "scamDetected": true,
  "totalMessagesExchanged": 18,
  "extractedIntelligence": {
    "bankAccounts": ["123456789012"],
    "upiIds": ["scammer@paytm"],
    "phishingLinks": ["http://fake-bank.com"],
    "phoneNumbers": ["9876543210"],
    "suspiciousKeywords": ["kyc", "blocked", "urgent"]
  },
  "agentNotes": "Banking/KYC scam attempt. Extracted: 1 bank account(s), 1 UPI ID(s). Engaged over 18 messages."
}
```

## Configuration

Key settings in `config.py`:
- `MIN_MESSAGES_BEFORE_END`: Minimum messages before ending (default: 8)
- `MAX_MESSAGES_PER_SESSION`: Maximum messages per session (default: 25)
- `MIN_INTELLIGENCE_ITEMS`: Minimum intelligence items to gather (default: 2)
- `LLM_MODEL`: OpenAI model to use (default: gpt-4o-mini)

## Error Handling

- Graceful fallback responses if AI generation fails
- Timeout handling for callback requests
- Input validation and sanitization
- Comprehensive logging for debugging

## Security

- API key authentication on all endpoints
- Input sanitization to prevent injection
- No exposure of scam detection status in responses
- Ethical constraints enforced in agent behavior

## Testing

Health check endpoint:
```bash
curl http://localhost:8000/health
```

Test message endpoint:
```bash
curl -X POST http://localhost:8000/api/message \
  -H "x-api-key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-123",
    "message": {
      "sender": "scammer",
      "text": "Your account will be blocked. Update KYC immediately.",
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

## Production Deployment

For production:
1. Set `DEBUG=False` in .env
2. Use a production WSGI server (gunicorn)
3. Set up proper logging and monitoring
4. Use environment-specific API keys
5. Configure rate limiting and request validation
6. Deploy behind a reverse proxy (nginx)

## License

Built for GUVI Hackathon - Agentic Honey-Pot Challenge
