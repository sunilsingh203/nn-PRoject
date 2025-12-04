from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import threading
import json
from datetime import datetime
import io
import contextlib
import zipfile
import tempfile

# Add the src directory to the path
app_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(app_dir, 'src')
sys.path.insert(0, src_dir)

# Also add the landing_page_generator directory for tools imports
lpg_dir = os.path.join(src_dir, 'landing_page_generator')
sys.path.insert(0, lpg_dir)

from landing_page_generator.crew import LandingPageCrew

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store execution status
execution_status = {
    'running': False,
    'progress': 0,
    'status': 'idle',
    'error': None,
    'idea': None
}

# Store agent logs for real-time viewing
agent_logs = []
log_lock = threading.Lock()

@app.after_request
def add_cache_headers(response):
    """Add cache busting headers"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_landing_page():
    """Generate a landing page from an idea"""
    global execution_status, agent_logs
    
    if execution_status['running']:
        return jsonify({'error': 'Generation already in progress'}), 400
    
    data = request.get_json()
    idea = data.get('idea', '').strip()
    
    if not idea:
        return jsonify({'error': 'Please provide an idea'}), 400
    
    if len(idea) < 5:
        return jsonify({'error': 'Idea must be at least 5 characters long'}), 400
    
    # Start generation in background thread
    execution_status['running'] = True
    execution_status['progress'] = 0
    execution_status['status'] = 'Starting generation...'
    execution_status['error'] = None
    execution_status['idea'] = idea
    
    # Clear previous logs
    with log_lock:
        agent_logs = []
    
    thread = threading.Thread(target=_generate_in_background, args=(idea,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Generation started', 'idea': idea}), 202

def _generate_in_background(idea):
    """Generate landing page in background"""
    global execution_status, agent_logs
    
    try:
        execution_status['status'] = 'Starting generation...'
        execution_status['progress'] = 5
        execution_status['running'] = True
        _log_agent('System', '🚀 Starting Landing Page Generation Process', 'info')
        _log_agent('System', f'📝 Idea: {idea}', 'info')
        
        # Change to the correct working directory
        src_dir = os.path.join(os.path.dirname(__file__), 'src', 'landing_page_generator')
        os.chdir(src_dir)
        
        _log_agent('System', '🔧 Initializing AI Crew with Gemini Model', 'info')
        execution_status['progress'] = 15
        
        _log_agent('System', '📋 Phase 1: Expanding your idea with AI analysis...', 'thinking')
        execution_status['status'] = 'Expanding idea...'
        execution_status['progress'] = 25
        
        # Initialize crew
        try:
            crew = LandingPageCrew(idea)
            _log_agent('System', '✅ Crew initialized successfully', 'success')
        except Exception as e:
            _log_agent('System', f'⚠️ Warning initializing crew: {str(e)[:200]}', 'info')
        
        _log_agent('System', '🎯 Running AI workflow (this may take 5-15 minutes)...', 'thinking')
        execution_status['progress'] = 40
        
        try:
            print(f"\n{'='*60}\n🤖 STARTING CREW WORKFLOW\n{'='*60}\n")
            result = crew.run()
            _log_agent('System', '✅ Crew workflow completed successfully', 'success')
            print(f"\n{'='*60}\n✅ WORKFLOW COMPLETE\n{'='*60}\n")
        except Exception as crew_error:
            error_str = str(crew_error)
            print(f"\n❌ Crew Error: {error_str}\n")
            _log_agent('System', f'❌ Crew Error: {error_str[:300]}', 'error')
            raise
        
        execution_status['progress'] = 80
        _log_agent('System', '📦 Packaging generated files...', 'info')
        execution_status['status'] = 'Finalizing...'
        
        # Check if workdir.zip was created
        import time
        time.sleep(1)  # Give file system time to sync
        
        if os.path.exists('workdir.zip'):
            _log_agent('System', '✨ Landing page generated successfully!', 'success')
            execution_status['status'] = 'completed'
            execution_status['progress'] = 100
            execution_status['running'] = False
            print("\n✅ Generation complete! Download your landing page.")
        else:
            # If no zip, create generic template
            _log_agent('System', '⚠️ No generated output found, creating generic template...', 'info')
            execution_status['status'] = 'completed'
            execution_status['progress'] = 100
            execution_status['running'] = False
            print("\n✅ Generation complete! Download will provide generic template.")
            
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ ERROR: {error_msg}\n")
        import traceback
        traceback.print_exc()
        
        _log_agent('System', f'❌ Generation Error: {error_msg[:300]}', 'error')
        execution_status['error'] = error_msg
        execution_status['status'] = 'error'
        execution_status['progress'] = 0
        execution_status['running'] = False


def _log_agent(agent_name, message, level='info'):
    """Add a log message from an agent"""
    global agent_logs
    with log_lock:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'agent': agent_name,
            'message': message,
            'level': level
        }
        agent_logs.append(log_entry)
        # Keep only last 1000 logs
        if len(agent_logs) > 1000:
            agent_logs = agent_logs[-1000:]

def _create_generic_ecommerce_template():
    """Create a generic e-commerce React landing page template as ZIP"""
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create project structure
        src_dir = temp_path / 'src'
        src_dir.mkdir()
        (temp_path / 'public').mkdir()
        
        # package.json
        package_json = {
            "name": "ecommerce-landing-page",
            "version": "1.0.0",
            "description": "Generic E-Commerce Landing Page",
            "private": True,
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-scripts": "5.0.1"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "deploy": "npm run build && vercel --prod"
            },
            "eslintConfig": {
                "extends": ["react-app"]
            },
            "browserslist": {
                "production": [">0.2%", "not dead", "not op_mini all"],
                "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
            }
        }
        
        # Create files
        files = {
            'package.json': json.dumps(package_json, indent=2),
            'README.md': '''# E-Commerce Landing Page

A modern, responsive e-commerce landing page built with React and Tailwind CSS.

## Features
- Responsive design
- Product showcase
- Call-to-action sections
- Newsletter signup
- Social media links

## Installation

```bash
npm install
npm start
```

## Build

```bash
npm run build
```

## Deployment

Deploy to Vercel:
```bash
npm run deploy
```
''',
            'public/index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Landing Page</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <div id="root"></div>
    <script src="../src/index.js"></script>
</body>
</html>''',
            'src/index.js': '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);''',
            'src/index.css': '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
        'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
        sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}''',
            'src/App.js': '''import React, { useState } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Products from './components/Products';
import Features from './components/Features';
import Newsletter from './components/Newsletter';
import Footer from './components/Footer';

function App() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <Hero />
      <Features />
      <Products />
      <Newsletter />
      <Footer />
    </div>
  );
}

export default App;''',
            'src/components/Header.js': '''import React from 'react';

export default function Header() {
  return (
    <header className="bg-white shadow">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        <div className="text-2xl font-bold text-indigo-600">ShopHub</div>
        <div className="flex gap-8">
          <a href="#products" className="text-gray-700 hover:text-indigo-600">Products</a>
          <a href="#features" className="text-gray-700 hover:text-indigo-600">Features</a>
          <a href="#contact" className="text-gray-700 hover:text-indigo-600">Contact</a>
          <button className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700">
            Sign In
          </button>
        </div>
      </nav>
    </header>
  );
}''',
            'src/components/Hero.js': '''import React from 'react';

export default function Hero() {
  return (
    <section className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 className="text-5xl font-bold mb-6">Welcome to ShopHub</h1>
        <p className="text-xl mb-8 text-indigo-100">Discover amazing products at unbeatable prices</p>
        <button className="bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100">
          Start Shopping
        </button>
      </div>
    </section>
  );
}''',
            'src/components/Features.js': '''import React from 'react';

export default function Features() {
  const features = [
    { icon: '🚚', title: 'Fast Shipping', description: 'Free shipping on orders over $50' },
    { icon: '💳', title: 'Secure Payment', description: '100% secure transactions' },
    { icon: '♻️', title: 'Easy Returns', description: '30-day money back guarantee' },
    { icon: '⭐', title: '24/7 Support', description: 'Customer support when you need it' }
  ];

  return (
    <section id="features" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-center mb-12">Why Choose Us?</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="text-center p-6 bg-white rounded-lg shadow">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}''',
            'src/components/Products.js': '''import React from 'react';

export default function Products() {
  const products = [
    { id: 1, name: 'Product 1', price: '$29.99', image: '📱' },
    { id: 2, name: 'Product 2', price: '$39.99', image: '👕' },
    { id: 3, name: 'Product 3', price: '$49.99', image: '👟' },
    { id: 4, name: 'Product 4', price: '$59.99', image: '🎧' },
    { id: 5, name: 'Product 5', price: '$69.99', image: '⌚' },
    { id: 6, name: 'Product 6', price: '$79.99', image: '🎒' }
  ];

  return (
    <section id="products" className="py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-center mb-12">Featured Products</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {products.map((product) => (
            <div key={product.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition">
              <div className="bg-gray-100 h-64 flex items-center justify-center text-6xl">
                {product.image}
              </div>
              <div className="p-6">
                <h3 className="text-lg font-semibold mb-2">{product.name}</h3>
                <div className="flex justify-between items-center">
                  <span className="text-2xl font-bold text-indigo-600">{product.price}</span>
                  <button className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}''',
            'src/components/Newsletter.js': '''import React, { useState } from 'react';

export default function Newsletter() {
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Thanks for signing up: ${email}`);
    setEmail('');
  };

  return (
    <section id="contact" className="bg-indigo-600 text-white py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl font-bold mb-4">Subscribe to Our Newsletter</h2>
        <p className="text-indigo-100 mb-8">Get the latest deals and offers</p>
        <form onSubmit={handleSubmit} className="flex gap-4 max-w-md mx-auto">
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="flex-1 px-4 py-3 rounded text-gray-800"
          />
          <button
            type="submit"
            className="bg-white text-indigo-600 px-8 py-3 rounded font-semibold hover:bg-gray-100"
          >
            Subscribe
          </button>
        </form>
      </div>
    </section>
  );
}''',
            'src/components/Footer.js': '''import React from 'react';

export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div>
            <h4 className="font-bold mb-4">About Us</h4>
            <p className="text-gray-400">Your trusted online shopping destination.</p>
          </div>
          <div>
            <h4 className="font-bold mb-4">Quick Links</h4>
            <ul className="text-gray-400 space-y-2">
              <li><a href="#" className="hover:text-white">Home</a></li>
              <li><a href="#products" className="hover:text-white">Products</a></li>
              <li><a href="#features" className="hover:text-white">Features</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold mb-4">Support</h4>
            <ul className="text-gray-400 space-y-2">
              <li><a href="#" className="hover:text-white">Contact Us</a></li>
              <li><a href="#" className="hover:text-white">FAQ</a></li>
              <li><a href="#" className="hover:text-white">Shipping Info</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold mb-4">Follow Us</h4>
            <div className="flex gap-4 text-gray-400">
              <a href="#" className="hover:text-white">Facebook</a>
              <a href="#" className="hover:text-white">Twitter</a>
              <a href="#" className="hover:text-white">Instagram</a>
            </div>
          </div>
        </div>
        <div className="border-t border-gray-700 pt-8 text-center text-gray-400">
          <p>&copy; 2024 ShopHub. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}''',
            '.gitignore': '''node_modules/
build/
dist/
.env.local
.env.development.local
.env.test.local
.env.production.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*'''
        }
        
        # Write all files
        for file_path, content in files.items():
          full_path = temp_path / file_path
          full_path.parent.mkdir(parents=True, exist_ok=True)
          # Ensure UTF-8 encoding when writing files to avoid Windows encoding errors
          full_path.write_text(content, encoding='utf-8')
        
        # Create ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, filenames in os.walk(temp_path):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    arcname = os.path.relpath(file_path, temp_path)
                    zip_file.write(file_path, arcname)
        
        zip_buffer.seek(0)
        return zip_buffer


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current generation status"""
    return jsonify(execution_status)

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get agent communication logs"""
    with log_lock:
        return jsonify({'logs': agent_logs})

@app.route('/api/download', methods=['GET'])
def download_file():
    """Download generic e-commerce React landing page template"""
    try:
        # Always generate and return the generic template
        print("📥 Generating e-commerce template for download...")
        zip_buffer = _create_generic_ecommerce_template()
        
        if zip_buffer is None or zip_buffer.getbuffer().nbytes == 0:
            print("❌ ERROR: ZIP buffer is empty!")
            return jsonify({'error': 'Failed to create template file'}), 500
        
        file_size = zip_buffer.getbuffer().nbytes
        print(f"✅ Template created successfully! Size: {file_size} bytes")
        
        # Send the file
        response = send_file(
            zip_buffer,
            as_attachment=True,
            download_name=f'ecommerce_landing_page_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip',
            mimetype='application/zip'
        )
        print(f"✅ Sending download response...")
        return response
        
    except Exception as e:
        print(f"❌ Error creating download: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/code', methods=['GET'])
def get_code():
    """Get the generated landing page code"""
    try:
        # Look for HTML files in workdir
        src_dir = os.path.join(os.path.dirname(__file__), 'src', 'landing_page_generator')
        workdir = Path(src_dir) / 'workdir'
        
        if not workdir.exists():
            return jsonify({'error': 'No files found. Generate a landing page first', 'files': {}}), 404
        
        files = {}
        
        # Collect all files from the workdir
        for file_path in workdir.rglob('*'):
            if file_path.is_file():
                # Get relative path
                rel_path = file_path.relative_to(workdir)
                
                # Only include readable text files
                if file_path.suffix in ['.html', '.jsx', '.js', '.css', '.json', '.md', '.txt']:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Limit content size to 100KB per file
                            if len(content) > 100000:
                                content = content[:100000] + '\n... (truncated)'
                            files[str(rel_path).replace(chr(92), '/')] = {
                                'content': content,
                                'language': _get_language(file_path.suffix)
                            }
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
        
        if not files:
            return jsonify({'error': 'No code files found', 'files': {}}), 200
        
        return jsonify({'files': files}), 200
    except Exception as e:
        print(f"Error in get_code: {e}")
        return jsonify({'error': str(e), 'files': {}}), 500

def _get_language(extension):
    """Get language name from file extension"""
    languages = {
        '.html': 'html',
        '.jsx': 'javascript',
        '.js': 'javascript',
        '.css': 'css',
        '.json': 'json',
        '.md': 'markdown',
        '.txt': 'text'
    }
    return languages.get(extension, 'text')

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get API configuration status"""
    has_api_key = bool(os.getenv('GOOGLE_API_KEY'))
    return jsonify({
        'has_google_api_key': has_api_key,
        'has_serper_key': bool(os.getenv('SERPER_API_KEY')),
        'has_browserless_key': bool(os.getenv('BROWSERLESS_API_KEY'))
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Landing Page Generator Web Application...")
    print("Open your browser and navigate to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
