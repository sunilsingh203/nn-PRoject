# 🚀 Landing Page Generator - Web Hosting Complete

## What's New
Your Landing Page Generator project is now ready to be hosted on the web using Flask! Here's what was added:

### Files Created:

1. **`app.py`** - Flask web application
   - Handles requests and responses
   - Manages background generation process
   - Provides REST API endpoints
   - Real-time status tracking

2. **`templates/index.html`** - Modern web interface
   - Beautiful gradient UI
   - Real-time progress tracking
   - File download functionality
   - Mobile responsive design
   - Character count validation
   - Error and success messages

3. **`requirements_flask.txt`** - Flask dependencies
   - Flask 3.0.0
   - Werkzeug 3.0.0

4. **`FLASK_SETUP.md`** - Complete setup guide
   - Installation instructions
   - How to use the web interface
   - API endpoints documentation
   - Troubleshooting guide
   - Deployment options

5. **`start_web.bat`** - Quick start script for Windows (Command Prompt)

6. **`start_web.ps1`** - Quick start script for Windows (PowerShell)

## Quick Start

### Option 1: Using PowerShell (Recommended)
```powershell
cd "c:\Users\Lenovo\Desktop\7th Sem\NN\Prac\projects2 (1)\projects2\agents\landing_page_generator"
.\start_web.ps1
```

### Option 2: Using Command Prompt
```cmd
cd "c:\Users\Lenovo\Desktop\7th Sem\NN\Prac\projects2 (1)\projects2\agents\landing_page_generator"
start_web.bat
```

### Option 3: Manual Start
```powershell
pip install -r requirements_flask.txt
python app.py
```

Then open your browser to: **http://localhost:5000**

## Features

✅ **Web Interface**
- Modern, responsive design
- Real-time progress tracking
- Easy idea submission
- One-click download

✅ **REST API**
- `/api/generate` - Start generation
- `/api/status` - Check progress
- `/api/download` - Download ZIP file
- `/api/config` - Check API configuration

✅ **Background Processing**
- Non-blocking generation
- Multi-threaded processing
- Real-time status updates
- Error handling

✅ **Security**
- Input validation
- Error handling
- File size limits
- Safe file operations

## Project Structure
```
landing_page_generator/
├── app.py                    # Flask application
├── start_web.bat            # Windows batch script
├── start_web.ps1            # PowerShell script
├── requirements_flask.txt   # Flask dependencies
├── FLASK_SETUP.md           # Setup documentation
├── GEMINI_SETUP.md          # Gemini configuration
├── templates/
│   └── index.html           # Web interface
├── src/
│   └── landing_page_generator/
│       ├── crew.py          # AI crew (already configured)
│       ├── config/
│       ├── tools/
│       └── templates/       # Add Tailwind templates here
└── .env                     # Your API keys
```

## System Requirements

- Python 3.10+
- 4GB RAM (minimum)
- Internet connection (for AI generation)
- Valid Gemini API key

## How to Use

1. **Start the server** using one of the methods above
2. **Open browser** to http://localhost:5000
3. **Enter your idea** (e.g., "2-page e-commerce website")
4. **Click Generate**
5. **Wait for completion** (10-45 minutes)
6. **Download your project** as ZIP file

## Example Ideas

- "Create a simple 2-page e-commerce website for selling handmade jewelry"
- "Build a landing page for a fitness coaching app with product listings"
- "Design a multi-page online store for digital products"
- "Make a professional website for selling courses"

## Important Notes

⚠️ **Gemini API Key Required**
- Get one free from: https://makersuite.google.com/app/apikey
- Update your `.env` file with the key

⚠️ **Generation Time**
- First run may take 10-45 minutes
- Subsequent runs are faster
- Be patient - the AI is working hard!

⚠️ **Tailwind Templates**
- Optional: Add templates to `src/landing_page_generator/templates/`
- Without templates, AI will still generate HTML files

## Troubleshooting

### Port 5000 Already in Use
Edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

### API Key Error
- Verify API key is in `.env` file
- Check the key is valid at: https://makersuite.google.com/app/apikey
- Make sure key hasn't expired

### Generation Fails
- Check internet connection
- Verify Gemini API quota
- Check console for detailed error messages

## Next Steps

1. ✅ Install Flask dependencies
2. ✅ Verify `.env` file has valid Gemini API key
3. ✅ Run `python app.py`
4. ✅ Open http://localhost:5000
5. ✅ Start generating landing pages!

## Production Deployment

For deploying to production, see `FLASK_SETUP.md` for:
- Gunicorn deployment
- Docker containerization
- Cloud hosting options

## Support

For detailed information:
- See `FLASK_SETUP.md` for setup and API documentation
- See `GEMINI_SETUP.md` for Gemini configuration
- Check console output for error messages

---

**You're all set! 🎉 Start creating amazing landing pages with AI!**
