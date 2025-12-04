@echo off
REM Quick start script for the Landing Page Generator web app

echo ====================================
echo Landing Page Generator - Web App
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org
    pause
    exit /b 1
)

echo Python is installed
echo.

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install -r requirements_flask.txt
    if errorlevel 1 (
        echo ERROR: Failed to install Flask dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting web server...
echo.
echo ====================================
echo Open your browser and go to:
echo http://localhost:5000
echo ====================================
echo.

python app.py
