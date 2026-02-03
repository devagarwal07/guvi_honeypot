# Setup Checklist

Complete this checklist to get your Honey-Pot API running.

## ☐ Prerequisites

- [ ] Python 3.11 or higher installed
- [ ] pip package manager available
- [ ] OpenAI API account created
- [ ] OpenAI API key obtained

## ☐ Installation

- [ ] Navigate to honeypot directory: `cd honeypot`
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment:
  - Windows: `venv\Scripts\activate`
  - Linux/Mac: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`

## ☐ Configuration

- [ ] Copy environment template: `cp .env.example .env`
- [ ] Edit .env file
- [ ] Set API_KEY (create a secure random string)
- [ ] Set OPENAI_API_KEY (from OpenAI dashboard)
- [ ] Review other settings (optional)

## ☐ Verification

- [ ] Start server: `python run.py`
- [ ] Server starts without errors
- [ ] Health check works: `curl http://localhost:8000/health`
- [ ] Response: `{"status":"healthy","service":"honeypot-api"}`

## ☐ Testing

- [ ] Update API_KEY in test_api.py
- [ ] Run test: `python test_api.py`
- [ ] Observe conversation flow
- [ ] Check logs for callback status

## ☐ Production (Optional)

- [ ] Set DEBUG=False in .env
- [ ] Configure reverse proxy (nginx)
- [ ] Set up SSL certificate
- [ ] Configure firewall rules
- [ ] Set up monitoring
- [ ] Configure log rotation

## ☐ Docker (Alternative)

- [ ] Docker installed
- [ ] Create .env file
- [ ] Run: `docker-compose up -d`
- [ ] Check logs: `docker-compose logs -f`
- [ ] Test health endpoint

## 🎯 Quick Commands

```bash
# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your keys

# Run
python run.py

# Test
curl http://localhost:8000/health

# Full test
python test_api.py
```

## 🔑 Required API Keys

### API_KEY
- Your own secure key for API authentication
- Generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- Add to .env: `API_KEY=your-generated-key`

### OPENAI_API_KEY
- Get from: https://platform.openai.com/api-keys
- Format: `sk-...`
- Add to .env: `OPENAI_API_KEY=sk-your-key`

## ✅ Success Indicators

- [ ] Server starts on port 8000
- [ ] Health endpoint returns 200 OK
- [ ] Test message returns human-like reply
- [ ] Logs show scam detection
- [ ] Callback sent after engagement
- [ ] No errors in logs

## 🆘 Troubleshooting

**Port already in use:**
```bash
# Change PORT in .env
PORT=8001
```

**OpenAI API error:**
- Verify key is correct
- Check billing/quota
- Test key: https://platform.openai.com/playground

**Module not found:**
```bash
pip install -r requirements.txt
```

**Permission denied:**
```bash
chmod +x start.sh
./start.sh
```

## 📚 Next Steps

After setup:
1. Read API_DOCUMENTATION.md for API details
2. Review ARCHITECTURE.md for system design
3. Check DEPLOYMENT.md for production setup
4. Run test_api.py to see it in action

## ✨ You're Ready!

Once all checkboxes are complete, your Honey-Pot API is ready to detect and engage scammers!

**Test endpoint:**
```bash
curl -X POST http://localhost:8000/api/message \
  -H "x-api-key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-123",
    "message": {
      "sender": "scammer",
      "text": "Your account will be blocked. Update KYC now.",
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
  "reply": "Why will my account be blocked? Which bank is this?"
}
```

🎉 **Congratulations! Your Honey-Pot API is operational!**
