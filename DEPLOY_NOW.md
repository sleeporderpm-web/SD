# 🚀 Quick Deployment Instructions

## Before You Deploy

Ensure you have:
- ✅ GitHub account
- ✅ Supabase account
- ✅ Supabase database configured (schema from README.md)
- ✅ All files committed and pushed to GitHub

---

## 🟢 RECOMMENDED: Streamlit Cloud (5 Minutes)

### Perfect for: Quick deployment, free hosting, automatic updates

#### Step 1: Go to Streamlit Cloud
```
https://share.streamlit.io
```

#### Step 2: Sign Up with GitHub
- Click "Sign up" → "Continue with GitHub"
- Click "Authorize streamlit"
- Complete GitHub authorization

#### Step 3: Deploy Your App
1. Click **"New app"** button (top right)
2. **Repository**: `sleeporderpm-web/SD`
3. **Branch**: `main`
4. **Main file path**: `streamlit_app.py`
5. Click **"Deploy"**

⏳ Wait 2-3 minutes for deployment to complete...

#### Step 4: Add Secrets
Once deployed:

1. Click ⚙️ **"Settings"** (top right)
2. Click **"Secrets"** tab
3. Paste your secrets:

```toml
# Copy and paste this exact format

SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-public-key"
ADMIN_PASSWORD = "your-secure-admin-password"
```

4. Click **"Save"**
5. App automatically refreshes

#### ✅ That's it! Your app is live!

Your app URL: `https://[username]-sd.streamlit.app`

---

## 🔵 ALTERNATIVE: Google Cloud Run (20 Minutes)

### Perfect for: Scalability, production deployments, custom control

#### Step 1: Install Google Cloud CLI
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

#### Step 2: Set up GCP
```bash
# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

#### Step 3: Deploy
```bash
# From the repository directory
gcloud run deploy sleep-disorder-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars \
    SUPABASE_URL="https://your-project.supabase.co",\
    SUPABASE_KEY="your-key",\
    ADMIN_PASSWORD="your-password"
```

#### ✅ Done! 
URL will appear in output

---

## 🟠 ALTERNATIVE: Heroku (15 Minutes)

### Perfect for: Simple deployment, easy scaling

#### Step 1: Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### Step 2: Deploy
```bash
# Login
heroku login

# Create app
heroku create sleep-disorder-app

# Set environment variables
heroku config:set SUPABASE_URL="https://your-project.supabase.co"
heroku config:set SUPABASE_KEY="your-key"
heroku config:set ADMIN_PASSWORD="your-password"

# Deploy
git push heroku main
```

#### ✅ Done!
Access at: `https://sleep-disorder-app.herokuapp.com`

---

## 🟣 ALTERNATIVE: Docker (Local or Self-Hosted)

### Perfect for: Full control, custom servers

#### Test Locally
```bash
# Build
docker build -t sleep-app .

# Run
docker run -p 8501:8080 \
  -e SUPABASE_URL="your-url" \
  -e SUPABASE_KEY="your-key" \
  -e ADMIN_PASSWORD="your-password" \
  sleep-app
```

Visit: `http://localhost:8501`

#### Deploy to Production
```bash
# Push to registry
docker tag sleep-app registry.example.com/sleep-app:latest
docker push registry.example.com/sleep-app:latest

# Deploy to your server
docker pull registry.example.com/sleep-app:latest
docker run -d -p 80:8080 \
  -e SUPABASE_URL="$SUPABASE_URL" \
  -e SUPABASE_KEY="$SUPABASE_KEY" \
  -e ADMIN_PASSWORD="$ADMIN_PASSWORD" \
  sleep-app
```

---

## ✅ Verify Your Deployment

After deploying to ANY platform:

### 1. Test User Registration
```
1. Visit your deployed URL
2. Click "Register" tab
3. Enter test email: test@example.com
4. Enter password: TestPass123!
5. Click "CREATE ACCOUNT"
✓ Should see "Account created!"
```

### 2. Test User Login
```
1. Click "Login" tab
2. Enter: test@example.com
3. Enter password: TestPass123!
4. Click "LOGIN"
✓ Should redirect to Sleep Analysis Dashboard
```

### 3. Test Sleep Analysis
```
1. Fill in all form fields
2. Click "GENERATE PREDICTION"
✓ Should display ML prediction result
✓ Should show "Prediction saved!"
```

### 4. Test Admin Panel
```
1. In main page, click "ADMIN LOGIN"
2. Enter your ADMIN_PASSWORD
3. Click "LOGIN AS ADMIN"
✓ Should see Hospital Action Panel
✓ Should display all patient reports
```

### 5. Test PDF Download
```
1. From any Report View page
2. Click "📄 DOWNLOAD PDF"
3. PDF should download
✓ File should be named: sleep_report_[ID].pdf
```

---

## 🔐 Security Checklist

- [ ] No `.env` file in repository (check `.gitignore`)
- [ ] All secrets in platform's secret manager
- [ ] Admin password changed from default
- [ ] SUPABASE_URL and SUPABASE_KEY configured
- [ ] Database backups enabled
- [ ] HTTPS enabled (automatic on most platforms)
- [ ] Access logs monitored

---

## 📊 Monitor Your Deployment

### Streamlit Cloud
- Dashboard → Settings → Usage
- View app traffic and resource usage

### Google Cloud Run
- Cloud Run console → Service metrics
- Monitor CPU, memory, and requests

### Heroku
- Dashboard → Logs
- Monitor app performance

---

## 🆘 Troubleshooting

### App won't load
```
Check: Are all dependencies in requirements.txt?
Fix: Add missing package and redeploy
```

### Database connection fails
```
Check: SUPABASE_URL and SUPABASE_KEY correct?
Fix: Update secrets in platform's secret manager
```

### PDF download fails
```
Check: Is fpdf2 in requirements.txt?
Fix: Add fpdf2>=2.7.0 and redeploy
```

### ML prediction not working
```
Check: Can app access database?
Fix: Verify Supabase connectivity
```

For more detailed troubleshooting, see `DEPLOYMENT_GUIDE.md`

---

## 📚 File Reference

| File | Purpose |
|------|---------|
| `DEPLOYMENT_GUIDE.md` | Comprehensive deployment guide |
| `Dockerfile` | Docker containerization |
| `Procfile` | Heroku configuration |
| `runtime.txt` | Python version for Heroku |
| `.github/workflows/` | CI/CD automation |
| `requirements.txt` | Dependencies |

---

## 🎯 Summary

1. **Choose platform**: Streamlit Cloud (recommended)
2. **Connect GitHub repository**
3. **Configure environment secrets**
4. **Deploy** ✅
5. **Test** ✅
6. **Monitor** ✅

---

## 💡 Pro Tips

✓ **Streamlit Cloud**: Auto-deploys when you push to main
✓ **Staging**: Create a `develop` branch for testing
✓ **Monitoring**: Set up alerts for high traffic
✓ **Backups**: Enable daily Supabase backups
✓ **Secrets**: Use platform's secure secret manager

---

## 📞 Need Help?

- **Streamlit Support**: https://discuss.streamlit.io
- **Supabase Support**: https://supabase.com/support
- **GitHub Actions**: https://github.com/features/actions
- **Docker Docs**: https://docs.docker.com

---

## 🎉 All Set!

Your sleep disorder MVP is ready to deploy!

**Choose your platform above and follow the steps.** 🚀

**Recommended**: Start with Streamlit Cloud for fastest deployment.

---

*Questions? Check DEPLOYMENT_GUIDE.md for detailed instructions.*
