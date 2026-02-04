# Render.com Deployment Checklist

## Critical: Environment Variables

Make sure these are set in Render Dashboard → Environment:

```
GEMINI_API_KEY=your-actual-gemini-api-key-here
LLM_MODEL=gemini-pro
API_KEY=9f3a1c8b2a4e7c6d91f8a0c1e2b3d4f567890abcd
HOST=0.0.0.0
PORT=8000
DEBUG=False
MIN_MESSAGES_BEFORE_END=10
MAX_MESSAGES_PER_SESSION=30
MIN_INTELLIGENCE_ITEMS=3
GUVI_CALLBACK_URL=https://hackathon.guvi.in/api/updateHoneyPotFinalResult
```

## Build Settings

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `cd honeypot && python run.py`
  OR
- **Start Command:** `python honeypot/run.py`

## Timeout Issue Fix

The code now includes:
- ✅ 5-second timeout on Gemini API calls
- ✅ Immediate fallback to contextual replies if Gemini fails
- ✅ Graceful handling of missing GEMINI_API_KEY
- ✅ Fast response times (<2 seconds)

## Testing Your Deployment

### 1. Health Check
```bash
curl https://guvi-honeypot-dvsq.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "honeypot-api",
  "gemini_configured": true,
  "version": "1.0.0"
}
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
      "text": "Your bank account will be blocked today. Verify immediately.",
      "timestamp": 1769776085000
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

## Common Issues

### Issue: Timeout after 30 seconds
**Cause:** Gemini API key not set or invalid
**Fix:** Set `GEMINI_API_KEY` in Render environment variables

### Issue: "gemini-1.5-flash not found"
**Cause:** Wrong model name
**Fix:** Set `LLM_MODEL=gemini-pro` in environment variables

### Issue: Cold start delays
**Cause:** Render free tier spins down after inactivity
**Fix:** 
- Upgrade to paid tier for always-on
- Or accept 10-15 second first request delay
- Code now has fast fallbacks to handle this

## Performance Optimizations

The code now:
1. ✅ Detects if Gemini is unavailable immediately
2. ✅ Uses fast contextual replies as fallback
3. ✅ Has 5-second timeout on AI calls
4. ✅ Returns response in <2 seconds even without Gemini
5. ✅ Logs all errors for debugging

## Deployment Steps

1. **Push code to GitHub**
2. **Go to Render Dashboard**
3. **Click "New +" → "Web Service"**
4. **Connect your GitHub repo**
5. **Set environment variables** (see above)
6. **Deploy**
7. **Wait 2-3 minutes for build**
8. **Test with health check**
9. **Test with message endpoint**
10. **Submit to GUVI**

## GUVI Submission

- **URL:** `https://guvi-honeypot-dvsq.onrender.com/api/message`
- **API Key:** `9f3a1c8b2a4e7c6d91f8a0c1e2b3d4f567890abcdeffedcba1234567890abcd`

## Monitoring

Check Render logs for:
- `Gemini client initialized successfully` - Good!
- `Gemini not available, using contextual reply` - Fallback working
- `Error generating agent reply` - Check API key

## Support

If issues persist:
1. Check Render logs
2. Verify environment variables are set
3. Test locally first
4. Ensure GEMINI_API_KEY is valid
