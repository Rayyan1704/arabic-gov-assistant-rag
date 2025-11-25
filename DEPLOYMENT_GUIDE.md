# 🚀 Deployment Guide - AraGovAssist

Complete guide to deploying your RAG system to production.

---

## 📋 Pre-Deployment Checklist

- [ ] All tests passing
- [ ] `.env` file configured
- [ ] Requirements.txt updated
- [ ] Documentation complete
- [ ] UI tested locally
- [ ] Performance acceptable

---

## 🎯 Deployment Options

### Option 1: Streamlit Cloud (Easiest) ⭐

**Pros:** Free, easy, automatic updates  
**Cons:** Limited resources, public by default

**Steps:**

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Complete RAG system with UI"
git remote add origin https://github.com/yourusername/aragov-assist.git
git push -u origin main
```

2. **Create Streamlit Cloud Account**
- Go to https://streamlit.io/cloud
- Sign in with GitHub
- Click "New app"

3. **Configure Deployment**
- Repository: `yourusername/aragov-assist`
- Branch: `main`
- Main file: `app.py`
- Python version: 3.9

4. **Add Secrets**
- Go to App settings → Secrets
- Add your `.env` contents:
```toml
GEMINI_API_KEY = "your_key_here"
```

5. **Deploy!**
- Click "Deploy"
- Wait 5-10 minutes
- Your app is live! 🎉

**URL:** `https://yourusername-aragov-assist.streamlit.app`

---

### Option 2: Docker (Flexible)

**Pros:** Portable, consistent, scalable  
**Cons:** Requires Docker knowledge

**Steps:**

1. **Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Create .dockerignore**
```
.venv/
__pycache__/
*.pyc
.git/
.env
notebooks/
*.md
```

3. **Build Image**
```bash
docker build -t aragov-assist .
```

4. **Run Container**
```bash
docker run -p 8501:8501 \
  -e GEMINI_API_KEY=your_key_here \
  aragov-assist
```

5. **Access App**
- http://localhost:8501

---

### Option 3: AWS EC2 (Production)

**Pros:** Full control, scalable, professional  
**Cons:** Costs money, requires AWS knowledge

**Steps:**

1. **Launch EC2 Instance**
- AMI: Ubuntu 22.04
- Instance type: t3.medium (2 vCPU, 4 GB RAM)
- Storage: 20 GB
- Security group: Allow ports 22, 80, 443, 8501

2. **Connect to Instance**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Dependencies**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.9 python3-pip -y

# Install git
sudo apt install git -y
```

4. **Clone Repository**
```bash
git clone https://github.com/yourusername/aragov-assist.git
cd aragov-assist
```

5. **Install Requirements**
```bash
pip3 install -r requirements.txt
```

6. **Configure Environment**
```bash
nano .env
# Add: GEMINI_API_KEY=your_key_here
```

7. **Run with Systemd (Auto-restart)**
```bash
# Create service file
sudo nano /etc/systemd/system/aragov.service
```

```ini
[Unit]
Description=AraGovAssist Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/aragov-assist
Environment="PATH=/home/ubuntu/.local/bin"
ExecStart=/home/ubuntu/.local/bin/streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable aragov
sudo systemctl start aragov
sudo systemctl status aragov
```

8. **Setup Nginx (Optional)**
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/aragov
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/aragov /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

9. **Setup SSL (Optional)**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

### Option 4: Google Cloud Run (Serverless)

**Pros:** Auto-scaling, pay-per-use  
**Cons:** Cold starts, requires GCP knowledge

**Steps:**

1. **Install Google Cloud SDK**
```bash
# Follow: https://cloud.google.com/sdk/docs/install
```

2. **Create Dockerfile** (same as Option 2)

3. **Build and Push**
```bash
gcloud builds submit --tag gcr.io/your-project/aragov-assist
```

4. **Deploy**
```bash
gcloud run deploy aragov-assist \
  --image gcr.io/your-project/aragov-assist \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key_here
```

5. **Access App**
- URL provided by Cloud Run

---

### Option 5: Heroku (Simple)

**Pros:** Easy, free tier available  
**Cons:** Limited resources, slower

**Steps:**

1. **Install Heroku CLI**
```bash
# Follow: https://devcenter.heroku.com/articles/heroku-cli
```

2. **Create Heroku App**
```bash
heroku create aragov-assist
```

3. **Add Buildpack**
```bash
heroku buildpacks:set heroku/python
```

4. **Create Procfile**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

5. **Set Environment Variables**
```bash
heroku config:set GEMINI_API_KEY=your_key_here
```

6. **Deploy**
```bash
git push heroku main
```

7. **Open App**
```bash
heroku open
```

---

## 🔒 Security Best Practices

### 1. Environment Variables
```bash
# Never commit .env file
echo ".env" >> .gitignore

# Use secrets management
# - Streamlit Cloud: App settings → Secrets
# - Docker: -e flag or docker-compose
# - AWS: Systems Manager Parameter Store
# - GCP: Secret Manager
```

### 2. API Key Protection
```python
# In app.py
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    st.error("API key not configured!")
    st.stop()
```

### 3. Rate Limiting
```python
# Add to app.py
import time
from functools import wraps

def rate_limit(max_calls=10, period=60):
    calls = []
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - period]
            if len(calls) >= max_calls:
                st.error("Rate limit exceeded. Please wait.")
                return None
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=10, period=60)
def process_query(query):
    # Your query processing
    pass
```

### 4. Input Validation
```python
# Add to app.py
def validate_query(query):
    if not query or len(query.strip()) == 0:
        return False, "Query cannot be empty"
    if len(query) > 500:
        return False, "Query too long (max 500 chars)"
    return True, ""

# Use it
is_valid, error = validate_query(query)
if not is_valid:
    st.error(error)
    st.stop()
```

---

## 📊 Monitoring & Analytics

### 1. Basic Logging
```python
# Add to app.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Log queries
logging.info(f"Query: {query}")
logging.info(f"Category: {detected_category}")
logging.info(f"Results: {len(results)}")
```

### 2. Google Analytics (Optional)
```python
# Add to app.py
import streamlit.components.v1 as components

# Google Analytics tracking
ga_code = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
"""

components.html(ga_code, height=0)
```

### 3. Error Tracking (Sentry)
```bash
pip install sentry-sdk
```

```python
# Add to app.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

---

## 🔧 Performance Optimization

### 1. Model Caching (Already Implemented)
```python
@st.cache_resource
def load_models():
    # Models loaded once
    pass
```

### 2. Query Caching
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_answer(query):
    # Cached results
    pass
```

### 3. Lazy Loading
```python
# Load models only when needed
if 'models_loaded' not in st.session_state:
    st.session_state.models_loaded = load_models()
```

### 4. Compression
```python
# In Dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

---

## 🧪 Testing Before Deployment

### 1. Local Testing
```bash
streamlit run app.py
# Test all features
# Check error handling
# Verify performance
```

### 2. Load Testing
```bash
pip install locust

# Create locustfile.py
from locust import HttpUser, task

class WebsiteUser(HttpUser):
    @task
    def query(self):
        self.client.get("/?query=test")

# Run
locust -f locustfile.py
```

### 3. Security Testing
```bash
# Check for vulnerabilities
pip install safety
safety check

# Check dependencies
pip-audit
```

---

## 📝 Post-Deployment Checklist

- [ ] App accessible via URL
- [ ] All features working
- [ ] Error handling tested
- [ ] Performance acceptable
- [ ] Monitoring setup
- [ ] Backups configured
- [ ] Documentation updated
- [ ] Team notified

---

## 🆘 Troubleshooting

### Issue: App won't start
**Solution:**
```bash
# Check logs
streamlit run app.py --logger.level=debug

# Check dependencies
pip list
pip install -r requirements.txt --upgrade
```

### Issue: Models not loading
**Solution:**
```bash
# Check file paths
ls -la index/

# Check permissions
chmod 644 index/*

# Re-download models
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')"
```

### Issue: API errors
**Solution:**
```bash
# Check API key
echo $GEMINI_API_KEY

# Test API
python test_gemini_api.py

# Check quota
# Visit: https://console.cloud.google.com/
```

### Issue: Slow performance
**Solution:**
```python
# Reduce initial_k
initial_k = 10  # Instead of 20

# Disable reranking for speed
use_reranking = False

# Use smaller model
model = SentenceTransformer('all-MiniLM-L6-v2')
```

---

## 🎯 Recommended: Streamlit Cloud

For most users, **Streamlit Cloud** is the best option:

✅ **Free**  
✅ **Easy** (5 minutes to deploy)  
✅ **Automatic updates** (push to GitHub)  
✅ **HTTPS** (secure by default)  
✅ **No server management**  

**Perfect for:**
- Demos
- Portfolios
- MVPs
- Small projects

---

## 🚀 Quick Deploy to Streamlit Cloud

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Complete RAG system"
git push

# 2. Go to streamlit.io/cloud
# 3. Click "New app"
# 4. Select your repo
# 5. Add GEMINI_API_KEY to secrets
# 6. Deploy!

# Done! Your app is live in 5 minutes! 🎉
```

---

**Choose your deployment option and go live!** 🚀
