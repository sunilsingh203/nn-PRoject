# Quick start script for the Landing Page Generator web app

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Landing Page Generator - Web App" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    python --version | Out-Null
    Write-Host "✓ Python is installed" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://www.python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check if Flask is installed
try {
    python -c "import flask" -ErrorAction Stop | Out-Null
    Write-Host "✓ Flask is installed" -ForegroundColor Green
} catch {
    Write-Host "Installing Flask dependencies..." -ForegroundColor Yellow
    pip install -r requirements_flask.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ ERROR: Failed to install Flask dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "Starting web server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Open your browser and go to:" -ForegroundColor Cyan
Write-Host "http://localhost:5000" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

python app.py
