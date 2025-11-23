
from flask import Flask, render_template_string
from waitress import serve
import os

app = Flask(__name__)

@app.route('/')
@app.route('/<path:path>')
def offline():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Site Temporarily Offline</title>
    <style>
        body { 
            font-family: sans-serif; background: #1a1a2e; color: white; 
            display: flex; align-items: center; justify-content: center;
            min-height: 100vh; margin: 0; text-align: center;
        }
        .container { 
            background: rgba(255,255,255,0.1); 
            padding: 3rem; border-radius: 20px; max-width: 500px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚧 Site Temporarily Offline</h1>
        <p><strong>All payment processing has been disabled.</strong></p>
        <p>We're making updates and improvements.</p>
        <p>Please check back later.</p>
    </div>
</body>
</html>
    ''')

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
