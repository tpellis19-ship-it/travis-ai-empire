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
    ''', business=TRAVIS_BUSINESS)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'KINO AI Consulting'})

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
