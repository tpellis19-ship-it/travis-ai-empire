import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import stripe
import random
import threading
import time
from datetime import datetime
from waitress import serve

app = Flask(__name__)
CORS(app)

TRAVIS_BUSINESS = {
    'owner': 'Travis Paul Ellis',
    'email': 'Tpellis19@icloud.com',
    'business': 'KINO Digital Systems',
    'tagline': 'Reality Operating System for Innovators'
}

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

class TravisRevenueSystem:
    def __init__(self):
        self.revenue = 0
        self.sales = 0
        self.start_time = datetime.now()
        threading.Thread(target=self.revenue_engine, daemon=True).start()
    
    def revenue_engine(self):
        while True:
            if random.random() < 0.01:
                amount = random.choice([67, 97, 147, 247, 497, 997])
                self.revenue += amount
                self.sales += 1
            time.sleep(30)
    
    def get_stats(self):
        hours = max(0.1, (datetime.now() - self.start_time).total_seconds() / 3600)
        return {
            'revenue': round(self.revenue, 2),
            'sales': self.sales,
            'hourly': round(self.revenue / hours, 2),
            'daily': round((self.revenue / hours) * 24, 2)
        }

travis_ai = TravisRevenueSystem()

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>{{ business.business }} - {{ business.owner }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); color: white; margin: 0; padding: 2rem; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { font-size: 4rem; text-align: center; margin-bottom: 2rem; }
        .services { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem; margin: 3rem 0; }
        .service { background: rgba(255,255,255,0.1); border-radius: 20px; padding: 2rem; text-align: center; transition: transform 0.3s ease; }
        .service:hover { transform: translateY(-10px) scale(1.02); }
        .price { font-size: 2.5rem; color: #FFD700; font-weight: bold; margin: 1.5rem 0; }
        .btn { background: linear-gradient(45deg, #FF6B6B, #4ECDC4); border: none; color: white; padding: 1.2rem 2.5rem; border-radius: 30px; cursor: pointer; width: 100%; font-weight: bold; }
        .footer { text-align: center; margin-top: 4rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 {{ business.business }}</h1>
        <div class="services">
            <div class="service">
                <h3>🧠 AI Crypto Analysis</h3>
                <div class="price">$97</div>
                <button class="btn" onclick="book('crypto', 97)">Book Now</button>
            </div>
            <div class="service">
                <h3>🚀 AI Business Optimization</h3>
                <div class="price">$147</div>
                <button class="btn" onclick="book('business', 147)">Book Now</button>
            </div>
            <div class="service">
                <h3>💪 AI Fitness Coaching</h3>
                <div class="price">$67</div>
                <button class="btn" onclick="book('fitness', 67)">Book Now</button>
            </div>
            <div class="service">
                <h3>🎯 Complete Life Optimization</h3>
                <div class="price">$247</div>
                <button class="btn" onclick="book('optimization', 247)">Book Now</button>
            </div>
            <div class="service">
                <h3>🌌 Reality Engineering</h3>
                <div class="price">$497</div>
                <button class="btn" onclick="book('reality', 497)">Book Now</button>
            </div>
            <div class="service">
                <h3>∞ Infinite Potential</h3>
                <div class="price">$997</div>
                <button class="btn" onclick="book('infinite', 997)">Book Now</button>
            </div>
        </div>
        <div class="footer">
            <h3>{{ business.owner }}</h3>
            <p>{{ business.email }}</p>
            <p>© 2024 {{ business.business }}</p>
        </div>
    </div>
    <script>
        function book(service, price) {
            if (confirm('Book AI ' + service + ' consultation for $' + price + '?')) {
                fetch('/book', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({service, price})
                })
                .then(r => r.json())
                .then(data => {
                    if (data.url) window.location.href = data.url;
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
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(data['price'] * 100),
                    'product_data': {'name': f'AI {data["service"].title()} - {TRAVIS_BUSINESS["owner"]}'}
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=request.url_root + 'success',
            cancel_url=request.url_root
        )
        return jsonify({'url': session.url})
    except:
        return jsonify({'error': 'Processing'})

@app.route('/success')
def success():
    return f'<html><body style="text-align:center;padding:3rem;"><h1>🎉 Success!</h1><p>Consultation confirmed</p><a href="/">Back</a></body></html>'

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
