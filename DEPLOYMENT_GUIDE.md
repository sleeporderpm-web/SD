# 🚀 Deployment Guide - Sleep Disorder MVP

## Overview

This guide provides step-by-step instructions for deploying the sleep disorder classification MVP to Streamlit Cloud and alternative hosting platforms.

---

## 🎯 Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free & Easiest)
- **Cost**: Free tier available
- **Ease**: Very simple
- **Setup Time**: ~10 minutes
- **Best for**: Quick deployments, prototyping, demos

### Option 2: Docker + Cloud Run (Google Cloud)
- **Cost**: Pay-as-you-go (~$1-5/month with free tier)
- **Ease**: Moderate
- **Setup Time**: ~20 minutes
- **Best for**: Production, custom requirements

### Option 3: Heroku
- **Cost**: No free tier (from ~$5/month)
- **Ease**: Moderate
- **Setup Time**: ~15 minutes
- **Best for**: Reliable hosting, easy scaling

### Option 4: AWS App Runner
- **Cost**: Pay-as-you-go (~$1-10/month)
- **Ease**: Moderate
- **Setup Time**: ~20 minutes
- **Best for**: Enterprise, high traffic

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [x] All code is committed to GitHub
- [x] `requirements.txt` has all dependencies
- [x] `.env.example` is in repository (but `.env` is in `.gitignore`)
- [x] Supabase credentials are ready
- [x] Database tables are created
- [x] All tests pass locally
- [x] No hardcoded secrets in code

---

## 🟢 OPTION 1: Streamlit Cloud Deployment (Recommended)

### Step 1: Prepare Your GitHub Repository

Your repository is already ready! Just ensure everything is pushed:

```bash
# Verify all changes are committed
git status

# Push to GitHub (if not already done)
git push origin main
```

### Step 2: Create Streamlit Cloud Account

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign up"
3. Choose "Sign up with GitHub"
4. Authorize Streamlit to access your GitHub account
5. Grant permissions when prompted

### Step 3: Deploy Your App

1. On Streamlit Cloud, click **"New app"**
2. Select your repository: `sleeporderpm-web/SD`
3. Select branch: `main`
4. Select main file path: `streamlit_app.py`
5. Click **"Deploy"**

**Your app will deploy in 2-3 minutes!**

### Step 4: Add Secrets (Environment Variables)

After deployment completes:

1. Click **"Settings"** (gear icon, top right)
2. Go to **"Secrets"** tab
3. Paste your secrets as TOML:

```toml
# Supabase Configuration
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"

# Admin Configuration
ADMIN_PASSWORD = "your-secure-password"
```

4. Click **"Save"**
5. App will automatically refresh

### Step 5: Access Your Deployed App

Your app will be available at:
```
https://[your-username]-sd.streamlit.app
```

Share this URL with users!

### Streamlit Cloud Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | Check `requirements.txt` has all dependencies |
| Secrets not loading | Restart app from "Manage app" > "Reboot" |
| Database connection fails | Verify `SUPABASE_URL` and `SUPABASE_KEY` |
| PDF generation fails | Ensure `fpdf2` is in `requirements.txt` |

---

## 🔵 OPTION 2: Google Cloud Run with Docker

### Step 1: Install Docker

```bash
# macOS
brew install docker

# Linux
sudo apt-get install docker.io

# Windows
# Download Docker Desktop from docker.com
```

### Step 2: Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create .streamlit directory
RUN mkdir -p ~/.streamlit

# Create Streamlit config
RUN echo "\
[server]\n\
port = 8080\n\
headless = true\n\
" > ~/.streamlit/config.toml

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

### Step 3: Create .dockerignore

```
__pycache__
*.pyc
.git
.gitignore
.env
.env.local
.streamlit
.vscode
.idea
*.db
*.log
.pytest_cache
venv/
```

### Step 4: Test Docker Locally

```bash
# Build image
docker build -t sleep-disorder-app .

# Run locally
docker run -p 8501:8080 \
  -e SUPABASE_URL="your-url" \
  -e SUPABASE_KEY="your-key" \
  -e ADMIN_PASSWORD="your-password" \
  sleep-disorder-app

# Visit http://localhost:8501
```

### Step 5: Deploy to Google Cloud Run

```bash
# Install Google Cloud CLI
# Download from: https://cloud.google.com/sdk/docs/install

# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy sleep-disorder-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SUPABASE_URL="your-url",SUPABASE_KEY="your-key",ADMIN_PASSWORD="your-password"
```

**Your app will be available at the URL shown in the output!**

---

## 🟠 OPTION 3: Heroku Deployment

### Step 1: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Download installer from heroku.com/download
```

### Step 2: Create Procfile

Create `Procfile` in project root:

```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

### Step 3: Create runtime.txt

Create `runtime.txt` in project root:

```
python-3.9.16
```

### Step 4: Login and Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create sleep-disorder-app

# Set environment variables
heroku config:set SUPABASE_URL="your-url"
heroku config:set SUPABASE_KEY="your-key"
heroku config:set ADMIN_PASSWORD="your-password"

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Step 5: Access Your App

```
https://sleep-disorder-app.herokuapp.com
```

---

## 🟣 OPTION 4: AWS App Runner

### Step 1: Create ECR Repository

```bash
# Set AWS region
export AWS_REGION=us-east-1

# Create ECR repository
aws ecr create-repository \
  --repository-name sleep-disorder-app \
  --region $AWS_REGION
```

### Step 2: Build and Push Docker Image

```bash
# Login to ECR
aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin \
  YOUR_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build image
docker build -t sleep-disorder-app .

# Tag image
docker tag sleep-disorder-app:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/sleep-disorder-app:latest

# Push to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/sleep-disorder-app:latest
```

### Step 3: Create App Runner Service

1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner)
2. Click **"Create Service"**
3. **Service settings**:
   - Select **"ECR"**
   - Choose your repository
   - Select **"Automatic"** deployments
4. **Deployment settings**:
   - Port: **8080**
   - Environment variables:
     - `SUPABASE_URL`: your-url
     - `SUPABASE_KEY`: your-key
     - `ADMIN_PASSWORD`: your-password
5. Click **"Create & Deploy"**

Your app will be available at the provided URL!

---

## 📊 Post-Deployment Verification

After deploying, test these flows:

### User Registration & Login
```
1. Visit deployed URL
2. Register new account
3. Login with credentials
4. Verify redirect to dashboard
```

### Sleep Analysis
```
1. Submit sleep analysis form
2. Verify ML prediction
3. Check analysis appears in history
4. Download PDF report
```

### Admin Panel
```
1. Visit deployed URL
2. Click Admin Login
3. Enter admin password
4. View all patient analyses
5. Test quick actions
```

### Database Connectivity
```
1. Submit analysis
2. Check Supabase console for new record
3. Verify data is saved correctly
```

---

## 🔒 Security Checklist After Deployment

- [x] Secret keys are in platform's secret manager (NOT in repo)
- [x] HTTPS is enabled (automatic on Streamlit Cloud)
- [x] No sensitive data in logs
- [x] Admin password is strong (12+ chars, mixed case, symbols)
- [x] Supabase credentials are read-only (if possible)
- [x] Database backups enabled
- [x] Access logs enabled
- [x] Rate limiting configured (if applicable)

---

## 📈 Monitoring & Maintenance

### Streamlit Cloud

1. **View Logs**:
   - Click app settings
   - Go to "Logs" tab
   - Monitor for errors

2. **Restart App**:
   - Settings > "Manage app"
   - Click "Reboot"

3. **View Stats**:
   - Settings > "Usage"
   - Check memory and CPU usage

### Docker/Cloud Platforms

```bash
# View logs
docker logs [container-id]

# Monitor resource usage
docker stats

# Update and redeploy
git push
# Platform automatically rebuilds
```

---

## 🚀 Scaling Considerations

### Streamlit Cloud
- Free tier: 1 app, shared resources
- For multiple apps or higher traffic, upgrade plan

### Google Cloud Run
- Auto-scales based on demand
- Adjust max instances in settings

### Heroku
- Free tier deprecated
- Paid dynos auto-scale

### AWS App Runner
- Auto-scales based on traffic
- Configure concurrency settings

---

## 💾 Database Backups

### Supabase Backups
```bash
# Automatic daily backups enabled in Supabase
# Access backups in Supabase console:
# Settings > Backups > Recovery

# Manual backup via psql
pg_dump -h db.XXXXXXXXX.supabase.co \
  -U postgres -d postgres > backup.sql
```

---

## 🔄 Continuous Deployment

### Option 1: Automatic (Streamlit Cloud)
- Automatically deploys when you push to `main`
- Set up branch protections to prevent bad deploys

### Option 2: GitHub Actions
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Streamlit Cloud Deployment
        run: |
          echo "Deployed to Streamlit Cloud"
          # Streamlit Cloud auto-deploys on push
```

---

## 📞 Troubleshooting Deployment

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| App won't load | Missing dependency | Add to `requirements.txt` |
| Database errors | Wrong credentials | Check secrets manager |
| PDF generation fails | `fpdf2` not installed | Reinstall requirements |
| Memory exceeded | Too many users | Upgrade hosting plan |
| Slow performance | Network latency | Choose closer region |

### Debug Commands

```bash
# Test local deployment
streamlit run streamlit_app.py --logger.level=debug

# Check dependencies
pip list

# Test database connection
python -c "from lib.db import get_client; print(get_client())"
```

---

## 📋 Deployment Summary

| Platform | Cost | Ease | Speed | Best For |
|----------|------|------|-------|----------|
| Streamlit Cloud | Free | ⭐⭐⭐⭐⭐ | 5 min | Quick deploy |
| Google Cloud Run | $1-10/mo | ⭐⭐⭐ | 20 min | Scalability |
| Heroku | $5+/mo | ⭐⭐⭐⭐ | 15 min | Simplicity |
| AWS App Runner | $1-10/mo | ⭐⭐⭐ | 20 min | Enterprise |
| Docker (self-hosted) | Variable | ⭐⭐ | 30 min | Full control |

---

## ✅ Final Checklist

- [ ] Repository pushed to GitHub
- [ ] All files committed
- [ ] `requirements.txt` updated
- [ ] `.env` is in `.gitignore`
- [ ] Supabase account created
- [ ] Database tables created
- [ ] Admin password set
- [ ] Deployment platform chosen
- [ ] Secrets configured in platform
- [ ] App deployed and tested
- [ ] Backup strategy in place
- [ ] Monitoring enabled

---

## 🎉 You're Ready to Deploy!

Choose your preferred platform and follow the steps above. Streamlit Cloud is recommended for fastest deployment.

**Happy deploying!** 🚀😴

---

## 📞 Quick Reference URLs

- **Streamlit Cloud**: https://share.streamlit.io
- **Google Cloud Console**: https://console.cloud.google.com
- **Heroku Dashboard**: https://dashboard.heroku.com
- **AWS Console**: https://console.aws.amazon.com
- **Supabase Dashboard**: https://app.supabase.com

---

*Last Updated: February 13, 2026*
