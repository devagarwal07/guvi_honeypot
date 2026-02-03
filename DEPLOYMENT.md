# Deployment Guide

## Quick Start (Local Development)

1. **Install dependencies:**
```bash
cd honeypot
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
```

Edit `.env` and set:
- `API_KEY`: Your secure API key
- `OPENAI_API_KEY`: Your OpenAI API key

3. **Run the server:**
```bash
python run.py
```

Server will start at `http://localhost:8000`

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Create .env file:**
```bash
cp .env.example .env
# Edit .env with your keys
```

2. **Build and run:**
```bash
docker-compose up -d
```

3. **Check logs:**
```bash
docker-compose logs -f
```

4. **Stop:**
```bash
docker-compose down
```

### Using Docker directly

1. **Build image:**
```bash
docker build -t honeypot-api .
```

2. **Run container:**
```bash
docker run -d \
  -p 8000:8000 \
  -e API_KEY=your-api-key \
  -e OPENAI_API_KEY=your-openai-key \
  --name honeypot-api \
  honeypot-api
```

## Production Deployment

### Prerequisites
- Python 3.11+
- OpenAI API key
- Reverse proxy (nginx/Apache) recommended
- SSL certificate for HTTPS

### Using Gunicorn (Production WSGI)

1. **Install gunicorn:**
```bash
pip install gunicorn
```

2. **Run with gunicorn:**
```bash
gunicorn app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Nginx Reverse Proxy

Create `/etc/nginx/sites-available/honeypot`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/honeypot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Systemd Service

Create `/etc/systemd/system/honeypot.service`:

```ini
[Unit]
Description=Honey-Pot API Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/honeypot
Environment="PATH=/opt/honeypot/venv/bin"
ExecStart=/opt/honeypot/venv/bin/gunicorn app:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable honeypot
sudo systemctl start honeypot
sudo systemctl status honeypot
```

## Cloud Deployment

### AWS EC2

1. Launch EC2 instance (t3.small or larger)
2. Install Docker:
```bash
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
```

3. Clone and deploy:
```bash
git clone <your-repo>
cd honeypot
docker-compose up -d
```

4. Configure security group to allow port 8000

### Google Cloud Run

1. **Build and push image:**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/honeypot-api
```

2. **Deploy:**
```bash
gcloud run deploy honeypot-api \
  --image gcr.io/PROJECT_ID/honeypot-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars API_KEY=your-key,OPENAI_API_KEY=your-key
```

### Heroku

1. **Create Procfile:**
```
web: gunicorn app:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

2. **Deploy:**
```bash
heroku create honeypot-api
heroku config:set API_KEY=your-key
heroku config:set OPENAI_API_KEY=your-key
git push heroku main
```

## Environment Variables

Required:
- `API_KEY`: API authentication key
- `OPENAI_API_KEY`: OpenAI API key

Optional:
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Debug mode (default: False)
- `LLM_MODEL`: OpenAI model (default: gpt-4o-mini)
- `LLM_TEMPERATURE`: Response randomness (default: 0.7)
- `LLM_MAX_TOKENS`: Max response length (default: 150)
- `MIN_MESSAGES_BEFORE_END`: Min messages before callback (default: 8)
- `MAX_MESSAGES_PER_SESSION`: Max messages per session (default: 25)
- `MIN_INTELLIGENCE_ITEMS`: Min intelligence to gather (default: 2)

## Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Logs
```bash
# Docker
docker-compose logs -f

# Systemd
sudo journalctl -u honeypot -f

# Direct
tail -f logs/app.log
```

### Metrics to Monitor
- Request rate and latency
- OpenAI API usage and costs
- Callback success rate
- Session duration and message counts
- Intelligence extraction rates

## Security Checklist

- [ ] Set strong API_KEY
- [ ] Use HTTPS in production
- [ ] Keep OpenAI API key secure
- [ ] Enable rate limiting
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Monitor for abuse
- [ ] Implement request logging
- [ ] Set up alerts for anomalies

## Troubleshooting

### Server won't start
- Check if port 8000 is available
- Verify environment variables are set
- Check logs for errors

### OpenAI API errors
- Verify API key is valid
- Check API quota and billing
- Ensure internet connectivity

### Callback failures
- Check GUVI endpoint is reachable
- Verify payload format
- Check network/firewall rules

### High latency
- Increase worker count
- Use faster OpenAI model
- Optimize session storage
- Add caching layer

## Performance Tuning

### Gunicorn Workers
```bash
# Formula: (2 x CPU cores) + 1
gunicorn app:app --workers 5 --worker-class uvicorn.workers.UvicornWorker
```

### OpenAI Settings
- Use `gpt-4o-mini` for cost efficiency
- Reduce `max_tokens` for faster responses
- Adjust `temperature` for consistency

### Caching
Consider adding Redis for session storage in high-traffic scenarios.

## Backup and Recovery

### Session Data
Sessions are stored in-memory. For persistence:
1. Implement Redis/database backend
2. Regular session data exports
3. Backup configuration files

### Configuration
```bash
# Backup
tar -czf honeypot-backup.tar.gz honeypot/

# Restore
tar -xzf honeypot-backup.tar.gz
```

## Support

For issues or questions:
1. Check logs for error messages
2. Review configuration settings
3. Test with provided test script
4. Verify API keys and endpoints
