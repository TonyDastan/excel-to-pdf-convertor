# Deploy to Render - Step by Step Guide

## 📋 Prerequisites

Before you start, make sure you have:
- ✅ A GitHub account
- ✅ Git installed on your computer
- ✅ A Render account (free - sign up at render.com)

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Files

Your project should have these files (already created):
- ✅ `app.py` - Main application
- ✅ `requirements.txt` - Dependencies
- ✅ `Procfile` - Tells Render how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `templates/` folder - HTML files
- ✅ `static/` folder - CSS/JS files

**Verify all files exist in your project folder.**

---

### Step 2: Create a GitHub Repository

#### Option A: Using GitHub Website (Easier)

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon (top right) → **"New repository"**
3. Repository name: `excel-to-pdf-converter` (or any name you like)
4. Description: "Excel to PDF Converter with Attendance Tracking"
5. Choose **Public** (for free Render deployment)
6. ✅ Check "Add a README file"
7. Click **"Create repository"**

#### Option B: Using Git Command Line

Open Command Prompt in your project folder:

```bash
# Navigate to your project
cd C:\development\Txt-marger\Txt-marger\txt-merger

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - Excel to PDF Converter"

# Create GitHub repo first (on github.com), then:
git remote add origin https://github.com/YOUR_USERNAME/excel-to-pdf-converter.git
git branch -M main
git push -u origin main
```

---

### Step 3: Upload Your Code to GitHub

#### If you used Option A (Website):

1. On your repository page, click **"uploading an existing file"**
2. Drag and drop ALL your project files/folders:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `templates/` folder
   - `static/` folder
   - All other files
3. Scroll down and click **"Commit changes"**

#### If you used Option B (Command Line):

Your code is already pushed! ✅

---

### Step 4: Create a Render Account

1. Go to [render.com](https://render.com)
2. Click **"Get Started"**
3. Sign up with your **GitHub account** (easiest option)
4. Authorize Render to access your GitHub repositories

---

### Step 5: Deploy Your App on Render

1. **On Render Dashboard**, click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - You'll see your GitHub repositories
   - Click **"Connect"** next to your `excel-to-pdf-converter` repo
   - (If you don't see it, click "Configure account" and grant access)

3. **Configure Your Web Service:**

   | Setting | Value |
   |---------|-------|
   | **Name** | `excel-to-pdf-converter` (or your choice) |
   | **Region** | Choose closest to your location |
   | **Branch** | `main` |
   | **Root Directory** | Leave blank |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn app:app` |

4. **Choose Plan:**
   - Select **"Free"** plan
   - Note: Free plan spins down after inactivity, takes ~30s to wake up

5. Click **"Create Web Service"**

---

### Step 6: Wait for Deployment

1. Render will start building your app
2. You'll see logs like:
   ```
   ==> Downloading Python...
   ==> Installing dependencies from requirements.txt...
   ==> Starting service...
   ```
3. Wait 3-5 minutes for first deployment
4. When you see **"Your service is live"** → ✅ Success!

---

### Step 7: Access Your App

1. On the Render dashboard, you'll see your app URL:
   ```
   https://excel-to-pdf-converter-xxxx.onrender.com
   ```

2. Click the URL or copy it

3. **Share this URL** with your office workers!

---

## 🎉 Your App is Now Live!

Anyone with the URL can now access your Excel to PDF converter from anywhere in the world!

**Example URL:**
```
https://excel-to-pdf-converter-abc123.onrender.com
```

---

## 📝 Important Notes

### ⚠️ Free Tier Limitations

- **Auto Sleep:** App sleeps after 15 minutes of inactivity
- **Wake Time:** Takes 30-50 seconds to wake up on first request
- **Monthly Limit:** 750 hours/month (enough for office use)
- **No Custom Domain:** Uses Render subdomain

**Workaround:** Visit the URL at least once every 15 minutes, or upgrade to paid plan ($7/month).

### 🔄 Updating Your App

When you make changes to your code:

1. **Push changes to GitHub:**
   ```bash
   git add .
   git commit -m "Updated features"
   git push origin main
   ```

2. **Render auto-deploys!** (if enabled)
   - Or manually click "Deploy latest commit" on Render dashboard

---

## 🔧 Troubleshooting

### Build Failed

**Problem:** `ModuleNotFoundError` or dependency errors

**Solution:**
1. Check `requirements.txt` has all dependencies
2. Verify file names are correct (case-sensitive)
3. Check build logs for specific error

### Service Not Starting

**Problem:** App shows "Deploy failed"

**Solution:**
1. Check `Procfile` contains exactly: `web: gunicorn app:app`
2. Verify `app.py` has `app = Flask(__name__)`
3. Check Python version in `runtime.txt` matches available versions

### 404 Not Found

**Problem:** URL loads but shows 404

**Solution:**
1. Ensure `templates/index.html` exists
2. Check folder structure is correct
3. Verify routes in `app.py` are correct

### Slow Performance

**Problem:** App is very slow or times out

**Solution:**
1. This is normal on free tier (cold start)
2. First request takes 30-50 seconds
3. Subsequent requests are fast
4. Upgrade to paid plan ($7/month) for always-on service

---

## 💰 Upgrading to Paid Plan (Optional)

**Benefits of Paid Plan ($7/month):**
- ✅ No sleep/wake delays
- ✅ Faster performance
- ✅ More resources (512MB → 1GB RAM)
- ✅ Better for frequent use

**To Upgrade:**
1. Go to your service on Render
2. Click "Settings" → "Plan"
3. Select "Starter" plan
4. Add payment method

---

## 🔒 Security Best Practices

1. **Don't commit sensitive data** (passwords, API keys) to GitHub
2. **Use environment variables** for secrets on Render:
   - Settings → Environment → Add Variable

3. **For production use**, consider adding authentication:
   ```python
   # Example: Simple password protection
   @app.before_request
   def check_auth():
       auth = request.authorization
       if not auth or auth.password != 'your_password':
           return Response('Login required', 401)
   ```

---

## 📊 Monitor Your App

On Render Dashboard you can:
- ✅ View logs (real-time)
- ✅ Check metrics (CPU, memory usage)
- ✅ See deployment history
- ✅ Monitor uptime

---

## ✅ Checklist Before Going Live

- [ ] All files uploaded to GitHub
- [ ] Procfile exists and is correct
- [ ] requirements.txt includes all dependencies
- [ ] App deployed successfully on Render
- [ ] Tested the live URL
- [ ] Shared URL with office workers
- [ ] Set up monitoring (optional)

---

## 🆘 Need Help?

**Render Issues:**
- Check [Render Docs](https://render.com/docs)
- Visit [Render Community](https://community.render.com)

**App Issues:**
- Check logs on Render dashboard
- Test locally first: `python app.py`
- Review deployment logs for errors

---

## 🎯 Quick Commands Reference

```bash
# Initialize git
git init

# Add all files
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push origin main

# Check git status
git status

# View git log
git log
```

---

**Congratulations! Your Excel to PDF Converter is now accessible to your entire office team from anywhere! 🎉**