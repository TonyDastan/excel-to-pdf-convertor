# Quick Setup Guide - Excel to PDF Converter

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

Open Command Prompt in this folder and run:

```bash
pip install -r requirements.txt
```

This installs: Flask, pandas, reportlab, openpyxl, waitress, and gunicorn.

---

### Step 2: Start the Server

**Option A: Double-click the batch file (Easiest)**
```
start_server.bat
```

**Option B: Run manually**
```bash
python run_production.py
```

**Option C: Development mode (testing only)**
```bash
python app.py
```

---

### Step 3: Share with Office Workers

Once the server starts, you'll see output like:

```
📍 Access the application at:
   Local:   http://127.0.0.1:8080
   Network: http://192.168.1.100:8080

📢 Share this URL with office workers:
   http://192.168.1.100:8080
```

**Share the Network URL** with your colleagues. They can access it from any computer on the same WiFi/network.

---

## ⚠️ Important Notes

1. **Keep Your Computer On**: The server runs on your computer, so it must stay on for others to access it.

2. **Firewall Setup**: Windows might ask for firewall permission - click "Allow access"

3. **Same Network Required**: All users must be on the same office WiFi/network

4. **Find Your IP Again**: 
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

---

## 📖 Features

✅ **Single File Mode**: Convert one Excel file to PDF  
✅ **Batch Mode**: Convert multiple files at once (gets ZIP file)  
✅ **Smart Color Coding**:
- Yellow highlight = Absent employees (no check-in)
- Red text = Late arrivals (after 08:34)

---

## 🐛 Troubleshooting

### "Can't connect" from other computers

1. Check firewall:
   - Open Windows Defender Firewall
   - Allow Python through firewall

2. Verify same network:
   - All computers must be on same WiFi

3. Use correct IP:
   - Run `ipconfig` to get your computer's IP
   - Share: `http://YOUR_IP:8080`

### "Module not found" error

```bash
pip install -r requirements.txt
```

### Port already in use

Stop other applications using port 8080, or edit `run_production.py` and change:
```python
port = 8080  # Change to 8081, 8082, etc.
```

---

## 🌐 For Internet Access (24/7 Hosting)

If you need remote access or don't want to keep your computer on, see **DEPLOYMENT_GUIDE.md** for cloud hosting options (Render, PythonAnywhere, etc.)

---

## 📞 Support

**Common Issues:**

| Problem | Solution |
|---------|----------|
| Python not found | Install Python 3.7+ from python.org |
| Permission denied | Run Command Prompt as Administrator |
| Can't access from phone | Ensure phone is on same WiFi network |
| Server keeps stopping | Don't close the Command Prompt window |

---

## 🎯 Quick Commands Reference

```bash
# Install everything
pip install -r requirements.txt

# Start production server
python run_production.py

# Start development server
python app.py

# Find your IP address
ipconfig

# Check Python version
python --version

# Update pip
python -m pip install --upgrade pip
```

---

**That's it! Your office can now convert Excel files to PDF reports with attendance tracking.** 🎉