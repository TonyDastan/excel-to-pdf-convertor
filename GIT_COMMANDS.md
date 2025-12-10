# Git Commands for Your Project

## 🚀 Quick Start - Deploy to GitHub & Render

### Your GitHub Repository:
```
https://github.com/TonyDastan/excel-to-pdf-convertor.git
```

---

## Step 1: Initialize Git and Push to GitHub

Open PowerShell or Command Prompt in your project folder and run these commands **one by one**:

```bash
# Navigate to your project folder
cd C:\development\Txt-marger\Txt-marger\txt-merger

# Initialize git repository
git init

# Add all files to staging
git add .

# Commit all files
git commit -m "Initial commit - Excel to PDF Converter"

# Add your GitHub repository as remote
git remote add origin https://github.com/TonyDastan/excel-to-pdf-convertor.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## Step 2: Verify Upload

Go to your GitHub repository and refresh the page:
```
https://github.com/TonyDastan/excel-to-pdf-convertor
```

You should see all your files uploaded!

---

## Step 3: Deploy to Render

1. **Go to Render:**
   - Visit: https://render.com
   - Click "Get Started" or "Sign In"
   - Sign in with your GitHub account

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - You'll see your repositories
   - Click "Connect" next to `excel-to-pdf-convertor`

3. **Configure Service:**
   ```
   Name: excel-to-pdf-convertor
   Region: Choose closest to you
   Branch: main
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   Plan: Free
   ```

4. **Deploy:**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - You'll get a URL like: https://excel-to-pdf-convertor.onrender.com

---

## 📝 Common Git Commands

### Check Status
```bash
git status
```

### See What Changed
```bash
git diff
```

### Update Code (After Making Changes)
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

### Pull Latest Changes
```bash
git pull origin main
```

### View Commit History
```bash
git log
```

### Undo Last Commit (Keep Changes)
```bash
git reset --soft HEAD~1
```

---

## 🔧 Troubleshooting

### Error: "fatal: remote origin already exists"
**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/TonyDastan/excel-to-pdf-convertor.git
```

### Error: "failed to push some refs"
**Solution:**
```bash
git pull origin main --rebase
git push origin main
```

### Error: "Permission denied (publickey)"
**Solution:**
Use HTTPS instead of SSH, or set up SSH keys:
```bash
git remote set-url origin https://github.com/TonyDastan/excel-to-pdf-convertor.git
```

### Need to Start Over?
```bash
# Remove git folder
rm -rf .git

# Start fresh
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TonyDastan/excel-to-pdf-convertor.git
git push -u origin main
```

---

## 📋 Pre-Push Checklist

Before pushing to GitHub:
- [ ] All files saved
- [ ] Tested locally: `python app.py`
- [ ] No sensitive data (passwords, API keys)
- [ ] .gitignore file exists
- [ ] All required files present:
  - [ ] app.py
  - [ ] requirements.txt
  - [ ] Procfile
  - [ ] runtime.txt
  - [ ] templates/
  - [ ] static/

---

## 🎯 Your Deployment URL

After deploying to Render, your app will be available at:
```
https://excel-to-pdf-convertor-XXXX.onrender.com
```

Share this URL with your office workers!

---

## 📞 Need Help?

**GitHub Issues:**
- Repository not found → Check URL is correct
- Permission denied → Make sure you're logged in
- Push rejected → Pull first, then push

**Render Issues:**
- Build failed → Check logs on Render dashboard
- App not starting → Verify Procfile and requirements.txt
- 404 error → Ensure templates folder uploaded

---

## ✅ Success Checklist

- [ ] Git initialized
- [ ] Files committed
- [ ] Pushed to GitHub
- [ ] Repository visible on GitHub
- [ ] Connected to Render
- [ ] Deployed successfully
- [ ] App URL works
- [ ] Tested PDF conversion
- [ ] Shared URL with team

---

**You're all set! Follow these commands to deploy your app.** 🚀