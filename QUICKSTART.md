# Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Install Dependencies
```bash
cd honeypot
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
cp .env.example .env
```

Edit `.env` and set:
- `API_KEY=your-secure-api-key-here`
- `OPENAI_API_KEY=sk-your-openai-key-here`

### Step 3: Run the Server
```bash
python run.py
```

Server starts at `http://localhost:8000`

---

## 🧪 Test the API

### Health Check
```bash
curl http://localhost:8000/health
```

### Send Test Message
```bash
curl -X POST http://localhost:8000/api/message \
  -H "x-api-key: your-secure-api-key-here" \
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


### Run Full Test Conversation
```bash
# Update API_KEY in test_api.py first
python test_api.py
```

---

## 📁 Project Structure

```
honeypot/
├── app.py                     # FastAPI entry point
├── auth.py                    # API key validation
├── config.py                  # Configuration
├── detector/
│   └── scam_classifier.py     # Scam detection
├── agent/
│   ├── persona.py             # AI agent prompts
│   └── agent_controller.py    # Agent logic
├── extractor/
│   └── intelligence.py        # Intelligence extraction
├── sessions/
│   └── memory_store.py        # Session management
├── callbacks/
│   └── guvi_client.py         # Final callback
└── utils/
    └── validators.py          # Input validation
```

---

## 🔑 Key Features

✅ **Scam Detection** - Keyword matching + context analysis  
✅ **AI Agent** - Human-like conversation using GPT-4o-mini  
✅ **Intelligence Extraction** - Bank accounts, UPI IDs, URLs, phones  
✅ **Multi-turn Engagement** - Natural conversation flow  
✅ **Mandatory Callback** - Automatic result reporting  
✅ **Production Ready** - Error handling, logging, security  

---

## 📚 Documentation

- **README.md** - Overview and features
- **API_DOCUMENTATION.md** - Complete API reference
- **ARCHITECTURE.md** - System design and data flow
- **DEPLOYMENT.md** - Production deployment guide

---

## 🐳 Docker Quick Start

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## ⚙️ Configuration

Key environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| API_KEY | - | Your API key (required) |
| OPENAI_API_KEY | - | OpenAI key (required) |
| PORT | 8000 | Server port |
| LLM_MODEL | gpt-4o-mini | OpenAI model |
| MIN_MESSAGES_BEFORE_END | 8 | Min engagement length |
| MAX_MESSAGES_PER_SESSION | 25 | Max engagement length |

---

## 🔍 How It Works

1. **Receive Message** → API validates and processes
2. **Detect Scam** → Keyword + context analysis
3. **Engage Scammer** → AI agent generates human-like replies
4. **Extract Intelligence** → Parse accounts, UPIs, URLs, phones
5. **Track Progress** → Count messages, store intelligence
6. **Send Callback** → Report results to evaluation endpoint

---

## 💡 Example Conversation

**Scammer:** "Your account will be blocked. Update KYC now."  
**Agent:** "Why will my account be blocked? Which bank is this?"

**Scammer:** "State Bank. Click here: http://fake-bank.com"  
**Agent:** "The link is not opening. Can you send it again?"

**Scammer:** "Enter your account number and UPI ID."  
**Agent:** "What should I enter? I'm not sure how to do this."

*After sufficient engagement, system sends callback with extracted intelligence.*

---

## 🛠️ Troubleshooting

**Server won't start:**
- Check port 8000 is available
- Verify .env file exists with API keys

**OpenAI errors:**
- Verify OPENAI_API_KEY is correct
- Check API quota and billing

**Callback failures:**
- Check internet connectivity
- Verify GUVI endpoint is reachable

---

## 📞 Support

For detailed information, see:
- API_DOCUMENTATION.md - API reference
- ARCHITECTURE.md - System design
- DEPLOYMENT.md - Production setup

---

## ✨ Quick Commands

```bash
# Install
pip install -r requirements.txt

# Run
python run.py

# Test
python test_api.py

# Docker
docker-compose up -d

# Health check
curl http://localhost:8000/health
```

---

**Built for GUVI Hackathon - Agentic Honey-Pot Challenge**
