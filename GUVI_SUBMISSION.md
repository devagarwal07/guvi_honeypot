# GUVI Hackathon Submission Details

## 🎯 What to Submit to GUVI Tester

### Honeypot API Endpoint URL
```
https://guvi-honeypot-dvsq.onrender.com/api/message
```

**IMPORTANT:** Make sure to include `/api/message` at the end!

### API Key (x-api-key header)
```
9f3a1c8b2a4e7c6d91f8a0c1e2b3d4f567890abcdeffedcba1234567890abcd
```

---

## ✅ Verification Steps

### 1. Test Health Endpoint
```bash
curl https://guvi-honeypot-dvsq.onrender.com/health
```

Expected response:
```json
{"status":"healthy","service":"honeypot-api"}
```

### 2. Test Message Endpoint
```bash
curl -X POST https://guvi-honeypot-dvsq.onrender.com/api/message \
  -H "x-api-key: 9f3a1c8b2a4e7c6d91f8a0c1e2b3d4f567890abcdeffedcba1234567890abcd" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-123",
    "message": {
      "sender": "scammer",
      "text": "Your bank account will be blocked. Verify immediately.",
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

Expected response:
```json
{
  "status": "success",
  "reply": "Why will my account be blocked?"
}
```

---

## 📋 GUVI Tester Form

When filling out the GUVI Honeypot Endpoint Tester:

1. **Honeypot API Endpoint URL:**
   ```
   https://guvi-honeypot-dvsq.onrender.com/api/message
   ```

2. **Headers section - x-api-key:**
   ```
   9f3a1c8b2a4e7c6d91f8a0c1e2b3d4f567890abcdeffedcba1234567890abcd
   ```

3. Click "Test Honeypot Endpoint"

---

## 🔍 Troubleshooting

### If you get "INVALID_REQUEST_BODY" error:

1. **Check the URL** - Must end with `/api/message`
   - ✅ Correct: `https://guvi-honeypot-dvsq.onrender.com/api/message`
   - ❌ Wrong: `https://guvi-honeypot-dvsq.onrender.com`

2. **Check the API Key** - Must be exact (64 characters)
   - Copy-paste from above to avoid typos

3. **Check Headers** - Must include:
   - `x-api-key: YOUR_KEY`
   - `Content-Type: application/json`

4. **Render Cold Start** - First request might timeout
   - Wait 30 seconds and try again
   - Render free tier has cold starts

### If you get timeout:

1. Visit the health endpoint first to wake up the server:
   ```
   https://guvi-honeypot-dvsq.onrender.com/health
   ```

2. Wait 10 seconds

3. Try the test again

---

## 🚀 Deployment Status

- **Service**: Render.com
- **Status**: ✅ Active
- **Region**: Global
- **Health Check**: https://guvi-honeypot-dvsq.onrender.com/health

---

## 📊 Expected Test Results

When GUVI tests your endpoint, they will:

1. Send a scam message
2. Receive an AI-generated reply
3. Continue the conversation
4. Receive your callback with extracted intelligence

**Expected Metrics:**
- Response time: < 2 seconds
- Scam detection: First message
- Engagement: 10-20 messages
- Intelligence: 3-5 items extracted
- Callback: Automatic after sufficient engagement

---

## 🎯 Final Checklist

Before submitting to GUVI:

- [x] Endpoint URL includes `/api/message`
- [x] API key is correct (64 characters)
- [x] Health endpoint returns 200 OK
- [x] Message endpoint returns proper JSON
- [x] AI responses are varied and realistic
- [x] Intelligence extraction working
- [x] Callback endpoint configured
- [x] Gemini API key set on Render

---

**Ready to submit!** ✅

Copy the URL and API key from above and paste them into the GUVI tester.
