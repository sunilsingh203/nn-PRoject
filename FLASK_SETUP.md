# Landing Page Generator - Web Application Setup Guide

## Overview
This Flask web application allows you to generate professional landing pages using AI (powered by Gemini). The interface is user-friendly and guides you through the generation process.

## Prerequisites
- Python 3.10+
- Virtual environment (recommended)
- Valid Gemini API Key

## Installation Steps

### 1. Install Flask Dependencies
```powershell
pip install -r requirements_flask.txt
```

Or install manually:
```powershell
pip install flask==3.0.0 werkzeug==3.0.0
```

### 2. Ensure You Have the Gemini API Key
Make sure your `.env` file has a valid Gemini API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

### 3. Start the Web Server
From the `landing_page_generator` directory, run:

```powershell
python app.py
```

You should see:
```
Starting Landing Page Generator Web Application...
Open your browser and navigate to: http://localhost:5000
```

### 4. Access the Application
Open your web browser and go to:
```
http://localhost:5000
```

## How to Use the Web Interface

1. **Enter Your Idea**: Describe what kind of landing page you want to create
   - Example: "Create a simple 2-page e-commerce website for selling handmade jewelry"

2. **Click Generate**: Click the "Generate Landing Page" button

3. **Wait for Completion**: The status shows real-time progress
   - Analyzing idea
   - Expanding with AI
   - Choosing templates
   - Finalizing project

4. **Download**: Once complete, click "Download Project" to get your landing page as a ZIP file

## Features

- ✅ User-friendly web interface
- ✅ Real-time progress tracking
- ✅ Powered by Google Gemini AI
- ✅ Generates complete 2-page landing pages
- ✅ Downloads as ZIP file
- ✅ Mobile responsive design
- ✅ Error handling and validation

## Project Structure

```
landing_page_generator/
├── app.py                          # Flask application
├── requirements_flask.txt          # Flask dependencies
├── src/
│   └── landing_page_generator/
│       ├── crew.py                 # AI crew configuration
│       ├── main.py                 # Command-line interface
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       ├── tools/
│       │   ├── search_tools.py
│       │   ├── browser_tools.py
│       │   ├── file_tools.py
│       │   └── template_tools.py
│       └── templates/              # Tailwind templates (add yours)
├── templates/
│   └── index.html                  # Web interface
└── .env                            # API keys (create from .env.example)
```

## API Endpoints

### POST /api/generate
Generate a new landing page
- **Request**: `{ "idea": "your landing page idea" }`
- **Response**: `202 Accepted` when generation starts

### GET /api/status
Get current generation status
- **Response**: 
  ```json
  {
    "running": boolean,
    "progress": 0-100,
    "status": "current status message",
    "error": "error message if any",
    "idea": "the original idea"
  }
  ```

### GET /api/download
Download the generated landing page
- **Response**: ZIP file with the complete project

### GET /api/config
Check API configuration status
- **Response**:
  ```json
  {
    "has_google_api_key": boolean,
    "has_serper_key": boolean,
    "has_browserless_key": boolean
  }
  ```

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Missing API Key
Error: "API key not valid"
- Solution: Update your `.env` file with a valid Gemini API key

### Generation Taking Too Long
- The generation can take 10-45 minutes depending on:
  - The complexity of your idea
  - AI model response time
  - System resources
- Be patient and don't close the browser

### CORS Issues
If accessing from a different domain:
```python
from flask_cors import CORS
CORS(app)
```

## Performance Tips

1. **Reduce Complexity**: Simpler ideas generate faster
2. **Use Descriptive Text**: More details help AI generate better results
3. **Run Locally**: Local deployment is faster than cloud hosting
4. **Resource Allocation**: Ensure your system has adequate RAM (4GB+ recommended)

## Deployment

### Using Gunicorn (Production)
```powershell
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements_flask.txt .
RUN pip install -r requirements_flask.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t landing-page-generator .
docker run -p 5000:5000 landing-page-generator
```

## Support

For issues or questions:
1. Check the error messages in the web interface
2. Review the console output when running `python app.py`
3. Ensure your Gemini API key is valid and has sufficient quota
4. Verify internet connection (required for AI generation)

## License

This project is released under the MIT License.
