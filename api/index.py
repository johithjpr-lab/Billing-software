"""
Billing System - SMS Gateway Backend (Python + Flask)
Vercel Serverless Function Entry Point

This file exports the Flask app as a WSGI application for Vercel.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": os.getenv('CORS_ORIGIN', '*'),
        "methods": ["POST", "GET", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration
FAST2SMS_API_KEY = os.getenv('FAST2SMS_API_KEY')
FAST2SMS_URL = 'https://www.fast2sms.com/dev/bulkV2'

# Before request logging
@app.before_request
def log_request():
    timestamp = datetime.now().isoformat()
    logger.info(f'[{timestamp}] {request.method} {request.path}')

# ============================================================================
# SMS GATEWAY ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'Billing System SMS Gateway',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/send-sms', methods=['POST'])
def send_sms():
    """
    Send SMS via Fast2SMS
    Request body:
    {
        "phone": "919876543210",
        "message": "Your message here"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'phone' not in data or 'message' not in data:
            return jsonify({'error': 'Missing phone or message'}), 400
        
        phone = data.get('phone')
        message = data.get('message')
        
        if not FAST2SMS_API_KEY:
            return jsonify({'error': 'SMS API key not configured'}), 500
        
        # Send SMS via Fast2SMS
        headers = {
            'authorization': FAST2SMS_API_KEY
        }
        
        payload = {
            'route': 'q',
            'message': message,
            'numbers': phone
        }
        
        response = requests.post(FAST2SMS_URL, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            logger.info(f'SMS sent successfully to {phone}')
            return jsonify({
                'success': True,
                'message': 'SMS sent successfully',
                'phone': phone,
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            logger.error(f'Failed to send SMS: {response.text}')
            return jsonify({'error': 'Failed to send SMS'}), response.status_code
            
    except requests.exceptions.RequestException as e:
        logger.error(f'Request error: {str(e)}')
        return jsonify({'error': 'Network error'}), 500
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-batch-sms', methods=['POST'])
def send_batch_sms():
    """
    Send batch SMS
    Request body:
    {
        "numbers": ["919876543210", "919987654321"],
        "message": "Your message here"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'numbers' not in data or 'message' not in data:
            return jsonify({'error': 'Missing numbers or message'}), 400
        
        numbers = data.get('numbers', [])
        message = data.get('message')
        
        if not isinstance(numbers, list) or len(numbers) == 0:
            return jsonify({'error': 'Invalid numbers list'}), 400
        
        if not FAST2SMS_API_KEY:
            return jsonify({'error': 'SMS API key not configured'}), 500
        
        headers = {
            'authorization': FAST2SMS_API_KEY
        }
        
        # Join numbers with comma
        phone_numbers = ','.join(numbers)
        
        payload = {
            'route': 'q',
            'message': message,
            'numbers': phone_numbers
        }
        
        response = requests.post(FAST2SMS_URL, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            logger.info(f'Batch SMS sent to {len(numbers)} recipients')
            return jsonify({
                'success': True,
                'message': 'Batch SMS sent successfully',
                'count': len(numbers),
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            logger.error(f'Failed to send batch SMS: {response.text}')
            return jsonify({'error': 'Failed to send batch SMS'}), response.status_code
            
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/billing-notification', methods=['POST'])
def billing_notification():
    """
    Send billing notification SMS
    Request body:
    {
        "phone": "919876543210",
        "customer_name": "John Doe",
        "amount": "500",
        "invoice_id": "INV-001"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'phone' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        phone = data.get('phone')
        customer_name = data.get('customer_name', 'Customer')
        amount = data.get('amount', '0')
        invoice_id = data.get('invoice_id', 'N/A')
        
        # Create message
        message = f"Hi {customer_name}, Your billing amount is Rs. {amount}. Invoice ID: {invoice_id}. Thank you!"
        
        if not FAST2SMS_API_KEY:
            return jsonify({'error': 'SMS API key not configured'}), 500
        
        headers = {
            'authorization': FAST2SMS_API_KEY
        }
        
        payload = {
            'route': 'q',
            'message': message,
            'numbers': phone
        }
        
        response = requests.post(FAST2SMS_URL, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            logger.info(f'Billing notification sent to {phone}')
            return jsonify({
                'success': True,
                'message': 'Billing notification sent',
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            logger.error(f'Failed to send notification: {response.text}')
            return jsonify({'error': 'Failed to send notification'}), response.status_code
            
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get API status and configuration info"""
    return jsonify({
        'status': 'active',
        'service': 'Billing System SMS Gateway',
        'version': '1.0.0',
        'environment': os.getenv('FLASK_ENV', 'production'),
        'endpoints': [
            '/api/health',
            '/api/send-sms',
            '/api/send-batch-sms',
            '/api/billing-notification',
            '/api/status'
        ],
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Billing System SMS Gateway API',
        'documentation': 'Visit /api/status for available endpoints',
        'version': '1.0.0'
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Internal error: {str(error)}')
    return jsonify({'error': 'Internal server error'}), 500

# Export app for WSGI servers and Vercel
if __name__ != '__main__':
    # This is used by gunicorn and Vercel
    wsgi_app = app
