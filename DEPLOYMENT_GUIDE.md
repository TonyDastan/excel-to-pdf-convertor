# Deployment Guide - Excel to PDF Converter

This guide explains how to host your Excel to PDF Converter application so that office workers can access it.

---

## Option 1: Local Network (LAN) Hosting ⭐ EASIEST

**Best for:** Small office, everyone on same WiFi/network

### Steps:

1. **Find Your Computer's IP Address**
   
   On Windows, open Command Prompt and type:
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., `192.168.1.100`)

2. **Allow Firewall Access**
   
   - Open Windows Defender Firewall
   - Click "Allow an app through firewall"
   - Click "Change settings" → "Allow another app"
   - Browse and add Python (`python.exe`)
   - Check both "Private" and "Public" boxes

3. **Start the Application**
   
   ```bash
   cd C:\development\Txt-marger\Txt-marger\txt-merger
   python app.py
   ```

4. **Share the URL**
   
   Tell office workers to open their browser and go to:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   Example: `http://192.168.1.100:5000`

**✅ Pros:** Free, simple, fast setup
**❌ Cons:** Your computer must stay on, only works on same network

---

## Option 2: Production Server with Waitress (Recommended for Office)

**Best for:** More stable local hosting with better performance

### Steps:

1. **Install Waitress**
   ```bash
   pip install waitress
   ```

2. **Create a production runner file** (`run_production.py`):
   ```python
   from waitress import serve
   from app import app
   
   print("Starting production server...")
   print("Access at: http://YOUR_IP:8080")
   serve(app, host='0.0.0.0', port=8080, threads=4)
   ```

3. **Run the production server**
   ```bash
   python run_production.py
   ```

4. **Share the URL**
   ```
   http://YOUR_IP_ADDRESS:8080
   ```

**✅ Pros:** More stable, handles multiple users better
**❌ Cons:** Still requires your computer to be on

---

## Option 3: Cloud Hosting (Internet Access)

**Best for:** Remote workers, multiple offices, 24/7 access

### A. Render (Free & Easy)

1. **Create account** at [render.com](https://render.com)

2. **Create these files in your project:**

   **`requirements.txt`** (already exists):
   ```
   Flask==3.0.0
   pandas==2.1.4
   reportlab==4.0.7
   openpyxl==3.1.2
   Werkzeug==3.0.1
   gunicorn==21.2.0
   ```

   **`Procfile`** (create new):
   ```
   web: gunicorn app:app
   ```

3. **Push code to GitHub**
   - Create a GitHub repository
   - Push your code

4. **Deploy on Render**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render will auto-deploy!
   - You'll get a URL like: `https://your-app.onrender.com`

**✅ Pros:** Free, 24/7 access, no computer needed
**❌ Cons:** Slower on free tier, need GitHub account

---

### B. PythonAnywhere (Free Tier Available)

1. **Create account** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload your files** via their web interface

3. **Install dependencies** in their console:
   ```bash
   pip install --user flask pandas reportlab openpyxl
   ```

4. **Configure web app** in their Web tab

5. **Get your URL**: `https://yourusername.pythonanywhere.com`

**✅ Pros:** Very beginner-friendly, free tier
**❌ Cons:** Limited resources on free tier

---

### C. Heroku (Paid but Popular)

1. **Create account** at [heroku.com](https://www.heroku.com)

2. **Install Heroku CLI**

3. **Create files:**
   
   **`Procfile`**:
   ```
   web: gunicorn app:app
   ```
   
   **`runtime.txt`**:
   ```
   python-3.12.6
   ```

4. **Deploy:**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

**✅ Pros:** Professional, reliable, scalable
**❌ Cons:** Costs $7+/month

---

### D. AWS/Azure/Google Cloud (Enterprise)

**Best for:** Large organizations with IT department

- Most expensive but most powerful
- Requires technical expertise
- Full control and customization
- Recommended to consult with IT team

---

## Option 4: Windows Server / Office Server

**Best for:** Offices with existing Windows Server

### Steps:

1. **Install Python on the server**

2. **Copy your application** to the server

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up as Windows Service** using NSSM:
   
   Download NSSM from [nssm.cc](https://nssm.cc)
   
   ```bash
   nssm install ExcelToPDF "C:\Python\python.exe" "C:\path\to\app.py"
   nssm start ExcelToPDF
   ```

5. **Configure IIS** (optional) to proxy requests

**✅ Pros:** Professional, always on, controlled environment
**❌ Cons:** Needs server access, IT knowledge

---

## Recommended Setup for Most Offices

### For Small Office (5-20 people):
👉 **Use Option 1 or Option 2** (Local Network with Waitress)

### For Multiple Locations or Remote Workers:
👉 **Use Option 3A** (Render - Free Cloud Hosting)

### For Enterprise:
👉 **Use Option 4** (Windows Server) or consult IT department

---

## Security Considerations

⚠️ **Important Security Notes:**

1. **Local Network Only**: If using Options 1-2, ensure your network is secure

2. **No Sensitive Data**: The app doesn't store data permanently, but uploaded files are temporarily saved

3. **Add Authentication** (Optional): For cloud hosting, consider adding login:
   ```python
   from flask_httpauth import HTTPBasicAuth
   auth = HTTPBasicAuth()
   
   @auth.verify_password
   def verify_password(username, password):
       if username == "admin" and password == "your_password":
           return username
   
   @app.route("/")
   @auth.login_required
   def index():
       return render_template("index.html")
   ```

4. **HTTPS**: For cloud hosting, ensure HTTPS is enabled (most platforms do this automatically)

5. **File Upload Limits**: Consider setting maximum file sizes

---

## Troubleshooting

### "Connection Refused" Error
- Check firewall settings
- Verify IP address is correct
- Ensure the server is running

### "Slow Performance"
- Use Waitress instead of Flask development server
- Increase server resources
- Consider cloud hosting

### "Can't Access from Other Computers"
- Make sure `host="0.0.0.0"` is set in `app.run()`
- Check firewall allows port 5000
- Verify all computers are on same network

---

## Support

For technical issues:
1. Check this guide first
2. Verify all dependencies are installed
3. Check firewall and network settings
4. Consult your IT department for enterprise deployments

---

**Quick Start Recommendation:**

Start with **Option 2 (Waitress)** for immediate office use, then migrate to **Option 3A (Render)** if you need internet access or 24/7 availability.