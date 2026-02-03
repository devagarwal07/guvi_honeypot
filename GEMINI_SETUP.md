# Google Gemini Setup Guide

## Get Your Free Gemini API Key

1. **Go to Google AI Studio**
   - Visit: https://aistudio.google.com/app/apikey

2. **Sign in with Google Account**
   - Use any Google account (Gmail)

3. **Create API Key**
   - Click "Create API Key"
   - Select "Create API key in new project" (or use existing project)
   - Copy the generated API key

4. **Update .env File**
   - Open `honeypot/.env`
   - Replace `your-gemini-api-key-here` with your actual API key:
   ```
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

## Free Tier Limits

- **15 requests per minute** (RPM)
- **1 million tokens per minute** (TPM)
- **1,500 requests per day** (RPD)

This is more than enough for testing and hackathon projects!

## Install Dependencies

```bash
conda activate lostandfound
cd honeypot
pip install -r requirements.txt
```

## Run the Server

```bash
conda activate lostandfound
python run.py
```

## Test the API

```bash
conda activate lostandfound
python test_api.py
```

## Model Used

- **gemini-1.5-flash** - Fast, efficient, and free
- Perfect for conversational AI
- Low latency responses

## Troubleshooting

**API Key Error:**
- Make sure you copied the full API key
- Check that GEMINI_API_KEY is set in .env file
- Verify the key is active at https://aistudio.google.com

**Rate Limit Error:**
- Free tier: 15 requests/minute
- Wait a minute and try again
- For production, consider upgrading

**Import Error:**
- Run: `pip install google-generativeai`
- Make sure you're in the lostandfound conda environment
