@echo off
echo ========================================
echo Excel to PDF Converter - Starting...
echo ========================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

echo.
echo Installing/Updating dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Starting Production Server...
echo ========================================
echo.

python run_production.py

pause
