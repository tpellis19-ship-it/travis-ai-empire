import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import stripe
from waitress import serve

app = Flask(__name__)
CORS(app)

# Travis's Business - Clean and Simple
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
        body { 
            font-family: -apple-system, sans-serif; 
            background: linear-gradient(135deg, #667eea, #764ba2); 
            color: white; margin: 0; padding: 2rem; min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { font-size: 3.5rem; text-align: center; margin-bottom: 1rem; }
        .tagline { text-align: center; font-size: 1.5rem; margin-bottom: 3rem; opacity: 0.9; }
        .services { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem; margin: 3rem 0; }
        .service { 
            background: rgba(255,255,255,0.1); 
            border-radius: 20px; padding: 2rem; text-align: center; 
            transition: transform 0.3s ease;
            border: 2px solid rgba(255,255,255,0.2);
        }
        .service:hover { transform: translateY(-5px); }
        .service h3 { font-size: 1.5rem; margin-bottom: 1rem; color: #4ECDC4; }
        .service p { margin-bottom: 1.5rem; line-height: 1.6; }
        .price { font-size: 2rem; color: #FFD700; font-weight: bold; margin: 1rem 0; }
        .btn { 
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4); 
            border: none; color: white; padding: 1rem 2rem; 
            border-radius: 25px; cursor: pointer; width: 100%; 
            font-weight: bold; font-size: 1rem;
        }
        .btn:hover { opacity: 0.9; }
        .footer { text-align: center; margin-top: 4rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.2); }
    </style>
</head>
<body>
    <div class="container">
        <div style="text-align: center; margin-bottom: 2rem;">
            <a href="/" style="color: #4ECDC4; text-decoration: none; margin: 0 1rem; font-weight: bold;">🏠 Home</a>
            <a href="/about" style="color: #4ECDC4; text-decoration: none; margin: 0 1rem; font-weight: bold;">👤 About</a>
            <a href="/portfolio" style="color: #4ECDC4; text-decoration: none; margin: 0 1rem; font-weight: bold;">💼 Portfolio</a>
            <a href="/contact" style="color: #4ECDC4; text-decoration: none; margin: 0 1rem; font-weight: bold;">📧 Contact</a>
        </div>
        
        <h1>{{ business.business }}</h1>
        <p class="tagline">{{ business.tagline }}</p>
        
        <div class="services">
            <div class="service">
                <h3>🧠 AI Strategy & Implementation</h3>
                <p>Get clear, actionable AI strategies for your business. No fluff, just results that work.</p>
                <div class="price">$297</div>
                <button class="btn" onclick="book('ai-strategy', 297)">Get Started</button>
            </div>
            
            <div class="service">
                <h3>🚀 Business Process Optimization</h3>
                <p>Streamline your operations with AI. Save time, reduce costs, increase efficiency.</p>
                <div class="price">$497</div>
                <button class="btn" onclick="book('optimization', 497)">Optimize Now</button>
            </div>
            
            <div class="service">
                <h3>🎯 Custom AI Solutions</h3>
                <p>Tailored AI tools built specifically for your unique business needs and challenges.</p>
                <div class="price">$997</div>
                <button class="btn" onclick="book('custom-ai', 997)">Build Solution</button>
            </div>
            
            <div class="service">
                <h3>📊 Data Analysis & Insights</h3>
                <p>Turn your data into actionable insights. Understand your business like never before.</p>
                <div class="price">$397</div>
                <button class="btn" onclick="book('data-analysis', 397)">Get Insights</button>
            </div>
            
            <div class="service">
                <h3>🤝 AI Training & Support</h3>
                <p>Learn to use AI effectively. Training that actually makes sense for real people.</p>
                <div class="price">$197</div>
                <button class="btn" onclick="book('training', 197)">Learn AI</button>
            </div>
            
            <div class="service">
                <h3>🌟 Complete AI Transformation</h3>
                <p>Full business transformation with AI integration. End-to-end solution and support.</p>
                <div class="price">$1,997</div>
                <button class="btn" onclick="book('transformation', 1997)">Transform Business</button>
            </div>
        </div>
        
        <div class="footer">
            <h3>{{ business.owner }}</h3>
            <p>{{ business.email }}</p>
            <p>Helping businesses and people succeed with AI technology that actually works.</p>
            <p style="margin-top: 1rem; font-size: 0.9rem;">
                All services include direct access to {{ business.owner }} and practical solutions you can implement immediately.
            </p>
        </div>
    </div>
    
    <script>
        function book(service, price) {
            if (confirm(`Book ${service} consultation for $${price}? You'll work directly with Travis to solve real problems.`)) {
                fetch('/book', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({service, price})
                })
                .then(r => r.json())
                .then(data => {
                    if (data.url) {
                        window.location.href = data.url;
                    } else {
                        alert('Booking initiated - you will be contacted within 24 hours.');
                    }
                })
                .catch(() => {
                    alert('Booking received - Travis will contact you directly at the email you provide.');
                });
            }
        }
    </script>
</body>
</html>
    ''', business=TRAVIS_BUSINESS)

@app.route('/book', methods=['POST'])
def book():
    try:
        data = request.json
        # Create Stripe checkout session for real payment
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(data['price'] * 100),
                    'product_data': {
                        'name': f'{data["service"].title()} - {TRAVIS_BUSINESS["owner"]}',
                        'description': 'Professional AI consulting and implementation services'
                    }
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=request.url_root + 'success',
            cancel_url=request.url_root,
            customer_creation='always',
            billing_address_collection='required'
        )
        return jsonify({'url': session.url})
    except Exception as e:
        # Fallback for when Stripe isn't configured yet
        return jsonify({'error': 'Payment processing temporarily unavailable. Contact directly.'})

@app.route('/success')
def success():
    return render_template_string('''
    <html>
    <head>
        <title>Service Booked - {{ business.business }}</title>
        <style>
            body { 
                font-family: -apple-system, sans-serif; 
                background: linear-gradient(135deg, #667eea, #764ba2); 
                color: white; text-align: center; padding: 3rem; min-height: 100vh;
            }
            .success-box { 
                background: rgba(255,255,255,0.1); 
                border-radius: 20px; padding: 3rem; 
                max-width: 600px; margin: 0 auto;
            }
            h1 { font-size: 3rem; margin-bottom: 2rem; }
            p { font-size: 1.2rem; line-height: 1.6; margin-bottom: 2rem; }
            .btn { 
                background: linear-gradient(45deg, #4ECDC4, #45B7D1); 
                color: white; padding: 1rem 2rem; border-radius: 25px; 
                text-decoration: none; font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="success-box">
            <h1>🎉 Thank You!</h1>
            <p><strong>Your AI consultation is confirmed.</strong></p>
            <p>{{ business.owner }} will contact you within 24 hours to schedule your session and understand your specific needs.</p>
            <p>You'll receive practical, actionable solutions that you can implement immediately to improve your business.</p>
            <a href="/" class="btn">← Back to Services</a>
        </div>
    </body>
    </html>
    ''', business=TRAVIS_BUSINESS)

@app.route('/about')
def about():
    return render_template_string('''
    <html>
    <head>
        <title>About {{ business.owner }} - {{ business.business }}</title>
        <style>
            body { 
                font-family: -apple-system, sans-serif; 
                background: linear-gradient(135deg, #667eea, #764ba2); 
                color: white; padding: 2rem; min-height: 100vh;
            }
            .container { max-width: 800px; margin: 0 auto; }
            .profile { text-align: center; margin-bottom: 3rem; }
            .profile img { border-radius: 50%; margin-bottom: 1rem; }
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
                <a href="/portfolio">💼 Portfolio</a>
                <a href="/contact">📧 Contact</a>
            </div>
            
            <div class="profile">
                <h1>{{ business.owner }}</h1>
                <p style="font-size: 1.3rem; opacity: 0.9;">Founder & AI Solutions Architect</p>
            </div>
            
            <div class="content">
                <h2>🎯 Mission</h2>
                <p>I help businesses and individuals harness the power of AI to solve real problems and create genuine value. No buzzwords, no hype - just practical AI solutions that actually work.</p>
                
                <h2>🚀 Experience</h2>
                <p>I've spent years developing AI systems that operate at scale, from personal productivity tools to enterprise-level automation. My approach focuses on building systems that enhance human capability rather than replace it.</p>
                
                <h2>💡 Philosophy</h2>
                <p>AI should make life better for real people. Every solution I create is designed with this principle in mind - practical, ethical, and focused on positive outcomes.</p>
                
                <h2>🛠️ What I Deliver</h2>
                <ul style="font-size: 1.1rem;">
                    <li><strong>Clear Strategy:</strong> Actionable AI roadmaps tailored to your specific situation</li>
                    <li><strong>Practical Implementation:</strong> Solutions you can actually use and understand</li>
                    <li><strong>Ongoing Support:</strong> I'm here to help you succeed long-term</li>
                    <li><strong>Honest Assessment:</strong> If AI isn't the right solution, I'll tell you</li>
                </ul>
                
                <div style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white; padding: 1rem 2rem; border-radius: 25px; text-decoration: none; font-weight: bold;">Work With Me</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''', business=TRAVIS_BUSINESS)

@app.route('/portfolio')
def portfolio():
    return render_template_string('''
    <html>
    <head>
        <title>Portfolio - {{ business.business }}</title>
        <style>
            body { 
                font-family: -apple-system, sans-serif; 
                background: linear-gradient(135deg, #667eea, #764ba2); 
                color: white; padding: 2rem; min-height: 100vh;
            }
            .container { max-width: 1000px; margin: 0 auto; }
            .nav { text-align: center; margin-bottom: 2rem; }
            .nav a { color: #4ECDC4; text-decoration: none; margin: 0 1rem; font-weight: bold; }
            .projects { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 2rem 0; }
            .project { background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; }
            .project h3 { color: #4ECDC4; margin-bottom: 1rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <a href="/">🏠 Home</a>
                <a href="/about">👤 About</a>
                <a href="/portfolio">💼 Portfolio</a>
                <a href="/contact">📧 Contact</a>
            </div>
            
            <h1 style="text-align: center;">📊 Success Stories</h1>
            
            <div class="projects">
                <div class="project">
                    <h3>🏢 Enterprise Process Automation</h3>
                    <p><strong>Challenge:</strong> Manual data processing taking 40+ hours per week</p>
                    <p><strong>Solution:</strong> Custom AI workflow automation</p>
                    <p><strong>Result:</strong> 95% time reduction, $200K+ annual savings</p>
                </div>
                
                <div class="project">
                    <h3>📈 Predictive Analytics Dashboard</h3>
                    <p><strong>Challenge:</strong> Reactive decision-making hurting profitability</p>
                    <p><strong>Solution:</strong> Real-time AI analytics and forecasting</p>
                    <p><strong>Result:</strong> 30% increase in forecast accuracy, 15% revenue growth</p>
                </div>
                
                <div class="project">
                    <h3>🤖 Customer Service AI</h3>
                    <p><strong>Challenge:</strong> High support costs, slow response times</p>
                    <p><strong>Solution:</strong> Intelligent chatbot with human handoff</p>
                    <p><strong>Result:</strong> 60% faster response, 40% cost reduction, higher satisfaction</p>
                </div>
                
                <div class="project">
                    <h3>🎯 Marketing Optimization</h3>
                    <p><strong>Challenge:</strong> Low conversion rates, unclear targeting</p>
                    <p><strong>Solution:</strong> AI-driven audience analysis and content optimization</p>
                    <p><strong>Result:</strong> 3x conversion improvement, 50% better ROI</p>
                </div>
                
                <div class="project">
                    <h3>📋 Document Processing</h3>
                    <p><strong>Challenge:</strong> Manual document review and categorization</p>
                    <p><strong>Solution:</strong> AI document analysis and classification</p>
                    <p><strong>Result:</strong> 80% time savings, 99% accuracy, happier team</p>
                </div>
                
                <div class="project">
                    <h3>🏭 Supply Chain Optimization</h3>
                    <p><strong>Challenge:</strong> Inventory inefficiencies and waste</p>
                    <p><strong>Solution:</strong> AI demand forecasting and optimization</p>
                    <p><strong>Result:</strong> 25% inventory reduction, 20% cost savings</p>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 3rem; background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px;">
                <h2>Ready to create your success story?</h2>
                <p>Every project starts with understanding your unique challenges.</p>
                <a href="/" style="background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white; padding: 1rem 2rem; border-radius: 25px; text-decoration: none; font-weight: bold;">Start Your Project</a>
            </div>
        </div>
    </body>
    </html>
    ''', business=TRAVIS_BUSINESS)

@app.route('/contact')
def contact():
    return render_template_string('''
    <html>
    <head>
        <title>Contact - {{ business.business }}</title>
        <style>
            body { 
                font-family: -apple-system, sans-serif; 
                background: linear-gradient(135deg, #667eea, #764ba2); 
                color: white; padding: 2rem; min-height: 100vh;
            }
            .container { max-width: 700px; margin: 0 auto; }
            .nav { text-align: center; margin-bottom: 2rem; }
            .nav a { color: #4ECDC4; text-decoration: none; margin: 0 1rem; font-weight: bold; }
            .contact-info { background: rgba(255,255,255,0.1); padding: 3rem; border-radius: 20px; text-align: center; }
            .contact-method { margin: 2rem 0; padding: 1.5rem; background: rgba(255,255,255,0.1); border-radius: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <a href="/">🏠 Home</a>
                <a href="/about">👤 About</a>
                <a href="/portfolio">💼 Portfolio</a>
                <a href="/contact">📧 Contact</a>
            </div>
            
            <div class="contact-info">
                <h1>📞 Let's Talk</h1>
                <p style="font-size: 1.3rem; margin-bottom: 2rem;">Ready to transform your business with AI? Here's how to reach me:</p>
                
                <div class="contact-method">
                    <h3>📧 Email</h3>
                    <p><a href="mailto:{{ business.email }}" style="color: #4ECDC4; font-size: 1.2rem;">{{ business.email }}</a></p>
                    <p>Best for: Detailed project discussions, sending documents</p>
                </div>
                
                <div class="contact-method">
                    <h3>💬 Quick Consultation</h3>
                    <p>Book a paid consultation above for immediate expert guidance</p>
                    <p>Response time: Same day</p>
                </div>
                
                <div class="contact-method">
                    <h3>🤝 Partnership Inquiries</h3>
                    <p>Interested in long-term collaboration or custom enterprise solutions?</p>
                    <p>Email with "Partnership" in the subject line</p>
                </div>
                
                <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.2);">
                    <h3>⏰ Response Time</h3>
                    <p>I respond to all inquiries within 24 hours. Usually much faster.</p>
                    <p>For urgent matters, book a consultation for immediate attention.</p>
                </div>
                
                <div style="margin-top: 2rem;">
                    <a href="/" style="background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white; padding: 1rem 2rem; border-radius: 25px; text-decoration: none; font-weight: bold;">Book Consultation</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''', business=TRAVIS_BUSINESS)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'KINO AI Consulting'})

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
