
import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import stripe
from waitress import serve

app = Flask(__name__)
CORS(app)

TRAVIS_BUSINESS = {
    'owner': 'Travis Paul Ellis',
    'email': 'Tpellis19@icloud.com',
    'business': 'KINO Digital Systems',
    'tagline': 'AI Solutions That Actually Help People'
}

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>{{ business.business }} - {{ business.owner }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); color: white; margin: 0; padding: 2rem; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { font-size: 3.5rem; text-align: center; margin-bottom: 1rem; }
        .tagline { text-align: center; font-size: 1.5rem; margin-bottom: 3rem; opacity: 0.9; }
        .services { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem; margin: 3rem 0; }
        .service { background: rgba(255,255,255,0.1); border-radius: 20px; padding: 2rem; text-align: center; transition: transform 0.3s ease; border: 2px solid rgba(255,255,255,0.2); }
        .service:hover { transform: translateY(-5px); }
        .service h3 { font-size: 1.5rem; margin-bottom: 1rem; color: #4ECDC4; }
        .service p { margin-bottom: 1.5rem; line-height: 1.6; }
        .price { font-size: 2rem; color: #FFD700; font-weight: bold; margin: 1rem 0; }
        .btn { background: linear-gradient(45deg, #FF6B6B, #4ECDC4); border: none; color: white; padding: 1rem 2rem; border-radius: 25px; cursor: pointer; width: 100%; font-weight: bold; font-size: 1rem; }
        .btn:hover { opacity: 0.9; }
        .footer { text-align: center; margin-top: 4rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.2); }
        .nav { text-align: center; margin-bottom: 2rem; }
        .nav a { color: #4ECDC4; text-decoration: none; margin: 0 1rem; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">🏠 Home</a>
            <a href="/about">👤 About</a>
            <a href="/contact">📧 Contact</a>
            <a href="/payment">💳 Payment Options</a>
        </div>
        
        <h1>{{ business.business }}</h1>
        <p class="tagline">{{ business.tagline }}</p>
        
        <div class="services">
            <div class="service">
                <h3>🧠 AI Strategy & Implementation</h3>
                <p>Get clear, actionable AI strategies for your business. No fluff, just results that work.</p>
                <div class="price">$297</div>
                <button class="btn" onclick="book('AI Strategy', 297)">Get Started</button>
            </div>
            
            <div class="service">
                <h3>🚀 Business Process Optimization</h3>
                <p>Streamline your operations with AI. Save time, reduce costs, increase efficiency.</p>
                <div class="price">$497</div>
                <button class="btn" onclick="book('Business Optimization', 497)">Optimize Now</button>
            </div>
            
            <div class="service">
                <h3>🎯 Custom AI Solutions</h3>
                <p>Tailored AI tools built specifically for your unique business needs and challenges.</p>
                <div class="price">$997</div>
                <button class="btn" onclick="book('Custom AI Solutions', 997)">Build Solution</button>
            </div>
            
            <div class="service">
                <h3>📊 Data Analysis & Insights</h3>
                <p>Turn your data into actionable insights. Understand your business like never before.</p>
                <div class="price">$397</div>
                <button class="btn" onclick="book('Data Analysis', 397)">Get Insights</button>
            </div>
            
            <div class="service">
                <h3>🤝 AI Training & Support</h3>
                <p>Learn to use AI effectively. Training that actually makes sense for real people.</p>
                <div class="price">$197</div>
                <button class="btn" onclick="book('AI Training', 197)">Learn AI</button>
            </div>
            
            <div class="service">
                <h3>🌟 Complete AI Transformation</h3>
                <p>Full business transformation with AI integration. End-to-end solution and support.</p>
                <div class="price">$1,997</div>
                <button class="btn" onclick="book('AI Transformation', 1997)">Transform Business</button>
            </div>
        </div>
        
        <div class="footer">
            <h3>{{ business.owner }}</h3>
            <p>{{ business.email }}</p>
            <p>Helping businesses and people succeed with AI technology that actually works.</p>
        </div>
    </div>
    
    <script>
        function book(service, price) {
            if (confirm('Book ' + service + ' for $' + price + '?')) {
                window.location.href = '/payment?service=' + encodeURIComponent(service) + '&price=' + price;
            }
        }
    </script>
</body>
</html>
    ''', business=TRAVIS_BUSINESS)

@app.route('/payment')
def payment():
    service = request.args.get('service', 'AI Consultation')
    price = request.args.get('price', '297')
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Payment Options - {{ business.business }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2rem; min-height: 100vh; }
        .container { max-width: 700px; margin: 0 auto; }
        .payment-grid { display: grid; gap: 1.5rem; margin: 2rem 0; }
        .payment-option { background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px; text-align: center; }
        .payment-btn { background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white; padding: 1rem 2rem; border-radius: 25px; text-decoration: none; font-weight: bold; display: inline-block; margin: 0.5rem; }
        .copy-text { background: rgba(0,0,0,0.3); padding: 0.5rem; border-radius: 5px; margin: 0.5rem 0; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1 style="text-align: center;">💳 Payment for {{ service }}</h1>
        <h2 style="text-align: center; color: #FFD700;">${{ price }}</h2>
        
        <div class="payment-grid">
            <div class="payment-option">
                <h3>📱 Zelle (Instant)</h3>
                <div class="copy-text">{{ business.email }}</div>
                <p>Send ${{ price }} with "{{ service }}" in memo</p>
            </div>
            
            <div class="payment-option">
                <h3>💚 Venmo</h3>
                <div class="copy-text">@TravisEllis19</div>
                <a href="https://venmo.com/TravisEllis19" class="payment-btn" target="_blank">Open Venmo</a>
            </div>
            
            <div class="payment-option">
                <h3>💵 Cash App</h3>
                <div class="copy-text">$TravisEllis19</div>
                <a href="https://cash.app/$TravisEllis19" class="payment-btn" target="_blank">Open Cash App</a>
            </div>
            
            <div class="payment-option">
                <h3>💙 PayPal</h3>
                <a href="https://paypal.me/TravisEllis19/{{ price }}" class="payment-btn" target="_blank">Pay ${{ price }} via PayPal</a>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 2rem; background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px;">
            <h3>✅ After Payment</h3>
            <p>Email confirmation to: <strong>{{ business.email }}</strong></p>
            <p>Include: {{ service }}, payment method, amount</p>
            <p><strong>Response within 24 hours guaranteed</strong></p>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/" style="color: #4ECDC4; text-decoration: none; font-size: 1.2rem;">← Back to Services</a>
        </div>
    </div>
</body>
</html>
    ''', service=service, price=price, business=TRAVIS_BUSINESS)

@app.route('/about')
def about():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>About {{ business.owner }} - {{ business.business }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2rem; min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; }
        .content { background: rgba(255,255,255,0.1); padding: 3rem; border-radius: 20px; line-height: 1.8; }
        .nav { text-align: center; margin-bottom: 2rem; }
        .nav a { color: #4ECDC4; text-decoration: none; margin: 0 1rem; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">🏠 Home</a>
            <a href="/about">👤 About</a>
            <a href="/contact">📧 Contact</a>
        </div>
        
        <div class="content">
            <h1>{{ business.owner }}</h1>
            <h2>🎯 Mission</h2>
            <p>I help businesses and individuals harness the power of AI to solve real problems and create genuine value. No buzzwords, no hype - just practical AI solutions that actually work.</p>
            
            <h2>🚀 Experience</h2>
            <p>I've spent years developing AI systems that operate at scale, from personal productivity tools to enterprise-level automation. My approach focuses on building systems that enhance human capability rather than replace it.</p>
            
            <h2>💡 Philosophy</h2>
            <p>AI should make life better for real people. Every solution I create is designed with this principle in mind - practical, ethical, and focused on positive outcomes.</p>
            
            <div style="text-align: center; margin-top: 2rem;">
                <a href="/" style="background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white; padding: 1rem 2rem; border-radius: 25px; text-decoration: none; font-weight: bold;">Work With Me</a>
            </div>
        </div>
    </div>
</body>
</html>
    ''', business=TRAVIS_BUSINESS)

@app.route('/contact')
def contact():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Contact - {{ business.business }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2rem; min-height: 100vh; }
        .container { max-width: 700px; margin: 0 auto; }
        .contact-info { background: rgba(255,255,255,0.1); padding: 3rem; border-radius: 20px; text-align: center; }
        .nav { text-align: center; margin-bottom: 2rem; }
        .nav a { color: #4ECDC4; text-decoration: none; margin: 0 1rem; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">🏠 Home</a>
            <a href="/about">👤 About</a>
            <a href="/contact">📧 Contact</a>
        </div>
        
        <div class="contact-info">
            <h1>📞 Let's Talk</h1>
            <h3>📧 Email</h3>
            <p><a href="mailto:{{ business.email }}" style="color: #4ECDC4; font-size: 1.2rem;">{{ business.email }}</a></p>
            
            <h3>⏰ Response Time</h3>
            <p>I respond to all inquiries within 24 hours. Usually much faster.</p>
            
            <div style="margin-top: 2rem;">
                <a href="/" style="background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white; padding: 1rem 2rem; border-radius: 25px; text-decoration: none; font-weight: bold;">Book Consultation</a>
            </div>
        </div>
    </div>
</body>
</html>
    ''', business=TRAVIS_BUSINESS)

@app.route('/success')
def success():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Thank You - {{ business.business }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); color: white; text-align: center; padding: 3rem; min-height: 100vh; }
        .success-box { background: rgba(255,255,255,0.1); border-radius: 20px; padding: 3rem; max-width: 600px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="success-box">
        <h1>🎉 Thank You!</h1>
        <p><strong>Your consultation is confirmed.</strong></p>
        <p>{{ business.owner }} will contact you within 24 hours.</p>
        <a href="/" style="color: #4ECDC4; text-decoration: none;">← Back to Services</a>
    </div>
</body>
</html>
    ''', business=TRAVIS_BUSINESS)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
    
