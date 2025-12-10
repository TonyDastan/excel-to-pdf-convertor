# Excel to PDF Converter

A powerful web application that converts Excel files to professionally formatted PDFs with intelligent color-coding for attendance tracking and data visualization. Supports both single file and batch processing modes!

Made with  by MarsCom@2025

## ✨ Features

📊 **Excel to PDF Conversion** – Convert .xlsx, .xls, and .csv files to beautifully formatted PDFs

🎯 **Smart Color Coding** – Automatically highlights:

- **Yellow cells** for Absenteeism (empty check-in)
- **Red font** for Late Comers (check-in after 08:34)

🔄 **Batch Processing** – Convert entire folders with multiple Excel files at once

- Process multiple files simultaneously
- Each PDF named after its respective Excel file
- Auto-zipped for easy download

✏️ **Customizable Reports** – Customize titles, subtitles, and report dates

📋 **Professional Formatting** – Tables with borders, proper alignment, and clear legends

📥 **One-Click Download** – Single file or zipped batch download

🎨 **Clean, Modern UI** – Responsive design with intuitive dual-mode interface

🛠️ **Tech Stack**

- **Flask** – Python backend framework
- **Pandas** – Data processing and Excel reading
- **ReportLab** – PDF generation and styling
- **HTML, CSS, JavaScript** – Frontend interface
- **Werkzeug** – Secure file handling

## 📋 Requirements

- Python 3.7+
- Flask
- Pandas
- ReportLab
- openpyxl (for Excel support)

## 🚀 How to Run Locally

### 1. Clone the repository:

```bash
git clone https://github.com/adrianadria
cd txt-merger
```

### 2. (Optional but recommended) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies:

```bash
pip install flask pandas reportlab openpyxl
```

### 4. Start the Flask app:

```bash
python app.py
```

The app will be available at `http://localhost:5000`

## 📖 How to Use

### Single File Mode

1. Click **"Single File"** button (default)
2. Upload your Excel file (drag & drop or browse)
3. Title auto-fills from filename, customize subtitle and date if needed
4. Click **"Convert to PDF"** button
5. Download your PDF named exactly like the Excel file

### Batch Mode

1. Click **"Batch Upload"** button
2. Select a folder containing multiple Excel files
3. Set common subtitle and report date for all files
4. Click **"Convert All to PDF"** button
5. Download `attendance_reports.zip` containing all PDFs
   - Each PDF is named after its respective Excel file
   - Each PDF maintains the Excel filename as its title

## 📝 Supported File Formats

- `.xlsx` – Microsoft Excel (2007 and later)
- `.xls` – Microsoft Excel (97-2003)
- `.csv` – Comma-separated values

## 🎨 Customization Options

- **Report Title** – Auto-filled from Excel filename (editable in single mode)
- **Report Subtitle** – Shared across all files in batch mode
- **Report Date** – Calendar date picker, applies to all files

## 📊 Example Use Case

Perfect for generating daily attendance reports with automatic flagging of:

- Employees who were absent (empty check-in) → **Yellow highlight**
- Employees who arrived late (after 08:34) → **Red text**

The color-coded output makes it easy to identify patterns at a glance!

## 🚀 Batch Processing Example

**Input Folder:**

```
attendance_files/
├── Mtendeni.xlsx
├── SAMORA_JM_MALL.xlsx
└── Godown_Afed.xlsx
```

**Output ZIP:**

```
attendance_reports.zip
├── Mtendeni.pdf
├── SAMORA_JM_MALL.pdf
└── Godown_Afed.pdf
```

Each PDF has its own title based on the filename and all contain the same subtitle and date you specified!

- `.xls` – Microsoft Excel (97-2003)
- `.csv` – Comma-separated values

## 🎨 Customization Options

- **Report Title** – Main title for the PDF
- **Report Subtitle** – Secondary title/date information
- **Late Threshold** – Hour of day (0-23) to mark arrivals as "late"

## 📊 Example Use Case

Perfect for generating daily attendance reports with automatic flagging of:

- Employees who were absent (empty check-in)
- Employees who arrived late

The color-coded output makes it easy to identify patterns at a glance!

Open the URL shown in your terminal (something like http://127.0.0.1:5000).

📁 Project Structure
txt-merger/
│── app.py # Flask backend
│── templates/ # HTML templates
│── static/ # CSS & JS (style.css, script.js)
│── uploads/ # Temporary uploaded files
│── results/ # Zipped merged outputs
│── README.md

🔮 Future Ideas

File type support beyond .txt (e.g., .csv, .log)

Option to choose custom output filenames

Cloud storage integration (Google Drive, Dropbox)

📜 License

Released under the MIT License.
