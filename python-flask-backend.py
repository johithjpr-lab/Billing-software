"""
Billing System - SMS Gateway Backend (Python + Flask)
Node.js + Fast2SMS Integration

Usage:
pip install flask requests python-dotenv
python python-flask-backend.py
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
        "origins": os.getenv('CORS_ORIGIN', 'http://localhost'),
        "methods": ["POST", "GET", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration
PORT = int(os.getenv('PORT', 5000))
FAST2SMS_API_KEY = os.getenv('FAST2SMS_API_KEY')
FAST2SMS_URL = 'https://www.fast2sms.com/dev/bulkV2'

# Before request logging
@app.before_request
def log_request():
    timestamp = datetime.now().isoformat()
    logger.info(f'[{timestamp}] {request.method} {request.path}')

# ============================================================================
# Main SMS Sending Endpoint
# ============================================================================

@app.route('/api/send-sms', methods=['POST'])
def send_sms():
    """
    Send SMS via Fast2SMS API
    
    Request:
    {
      "phone": "919876543210",
      "message": "Your bill message"
    }
    """
    try:
        data = request.json or {}
        phone = data.get('phone')
        message = data.get('message')
        
        # Validate input
        if not phone or not message:
            logger.warning('⚠️  Missing required fields: phone or message')
            return jsonify({
                'success': False,
                'error': 'Phone number and message are required',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Validate phone format
        phone_digits = ''.join(filter(str.isdigit, str(phone)))
        if len(phone_digits) < 10 or len(phone_digits) > 12:
            logger.warning(f'⚠️  Invalid phone format: {phone}')
            return jsonify({
                'success': False,
                'error': 'Invalid phone number format (10-12 digits required)',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Check API key
        if not FAST2SMS_API_KEY:
            logger.error('❌ FAST2SMS_API_KEY not configured')
            return jsonify({
                'success': False,
                'error': 'SMS service not configured',
                'timestamp': datetime.now().isoformat()
            }), 500
        
        # Send SMS
        logger.info(f'📤 Sending SMS to {phone}...')
        result = send_via_fast2sms(phone, message)
        
        if result['success']:
            logger.info(f'✅ SMS sent successfully to {phone}')
            return jsonify({
                'success': True,
                'message': 'SMS sent successfully',
                'requestId': result.get('request_id'),
                'timestamp': datetime.now().isoformat(),
                'data': result.get('data')
            }), 200
        else:
            logger.error(f'❌ SMS sending failed: {result.get("error")}')
            return jsonify({
                'success': False,
                'error': result.get('error', 'Failed to send SMS'),
                'timestamp': datetime.now().isoformat()
            }), 400
    
    except Exception as e:
        logger.error(f'❌ Error in /api/send-sms: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# ============================================================================
# Batch SMS Endpoint
# ============================================================================

@app.route('/api/send-sms-batch', methods=['POST'])
def send_sms_batch():
    """
    Send multiple SMS messages in batch
    
    Request:
    {
      "smsList": [
        {"phone": "919876543210", "message": "..."},
        {"phone": "919876543211", "message": "..."}
      ]
    }
    """
    try:
        data = request.json or {}
        sms_list = data.get('smsList', [])
        
        if not isinstance(sms_list, list) or len(sms_list) == 0:
            return jsonify({
                'success': False,
                'error': 'smsList array required with at least one item'
            }), 400
        
        if len(sms_list) > 100:
            return jsonify({
                'success': False,
                'error': 'Maximum 100 SMS per batch'
            }), 400
        
        results = []
        logger.info(f'📤 Sending {len(sms_list)} SMS messages...')
        
        for sms in sms_list:
            try:
                result = send_via_fast2sms(sms.get('phone'), sms.get('message'))
                results.append({
                    'phone': sms.get('phone'),
                    'success': result['success'],
                    'message': result.get('message')
                })
            except Exception as e:
                results.append({
                    'phone': sms.get('phone'),
                    'success': False,
                    'error': str(e)
                })
        
        successful = sum(1 for r in results if r['success'])
        logger.info(f'✅ Batch complete: {successful}/{len(sms_list)} sent')
        
        return jsonify({
            'success': True,
            'message': f'Batch sent: {successful}/{len(sms_list)} successful',
            'results': results,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f'❌ Batch SMS Error: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# Health Check Endpoints
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'service': 'Billing System SMS Gateway',
        'timestamp': datetime.now().isoformat(),
        'configured': bool(FAST2SMS_API_KEY)
    }), 200

@app.route('/api/status', methods=['GET'])
def status():
    """Service status endpoint"""
    return jsonify({
        'status': 'active',
        'gateway': 'Fast2SMS',
        'timestamp': datetime.now().isoformat(),
        'apiConfigured': bool(FAST2SMS_API_KEY),
        'corsEnabled': bool(os.getenv('CORS_ORIGIN')),
        'pythonVersion': __import__('sys').version.split()[0],
        'environment': os.getenv('FLASK_ENV', 'development')
    }), 200

# ============================================================================
# Test Endpoint (Development Only)
# ============================================================================

@app.route('/api/test-sms', methods=['GET'])
def test_sms():
    """Test SMS endpoint (development only)"""
    if os.getenv('FLASK_ENV') == 'production':
        return jsonify({
            'success': False,
            'error': 'Test endpoint disabled in production'
        }), 403
    
    phone = request.args.get('phone')
    if not phone:
        return jsonify({
            'success': False,
            'error': 'phone query parameter required'
        }), 400
    
    try:
        test_message = f'TEST SMS from Billing System - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        result = send_via_fast2sms(phone, test_message)
        
        return jsonify({
            'success': result['success'],
            'message': 'Test SMS sent',
            'phone': phone,
            'data': result.get('data')
        }), 200 if result['success'] else 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# Helper Functions
# ============================================================================

def send_via_fast2sms(phone, message):
    """
    Send SMS via Fast2SMS API
    
    Returns:
    {
        'success': bool,
        'message': str,
        'request_id': str,
        'data': dict,
        'error': str
    }
    """
    try:
        headers = {
            'authorization': FAST2SMS_API_KEY,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'phone': phone,
            'message': message,
            'route': 'dlt',
            'flash': 0
        }
        
        response = requests.post(
            FAST2SMS_URL,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        logger.info(f'📨 Fast2SMS Response Status: {response.status_code}')
        response_data = response.json()
        logger.info(f'📨 Fast2SMS Response: {response_data}')
        
        # Check if API returned success
        if response_data.get('return'):
            return {
                'success': True,
                'message': 'SMS sent',
                'request_id': response_data.get('request_id'),
                'data': response_data
            }
        else:
            error_msg = response_data.get('message', 'API returned error')
            return {
                'success': False,
                'message': error_msg,
                'error': error_msg,
                'data': response_data
            }
    
    except requests.exceptions.Timeout:
        error = 'Request timeout - SMS gateway not responding'
        logger.error(f'❌ {error}')
        return {'success': False, 'error': error}
    
    except requests.exceptions.ConnectionError:
        error = 'Connection error - Cannot reach SMS gateway'
        logger.error(f'❌ {error}')
        return {'success': False, 'error': error}
    
    except Exception as e:
        error = str(e)
        logger.error(f'❌ Fast2SMS Error: {error}')
        return {'success': False, 'error': error}

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f'❌ Internal Server Error: {str(error)}')
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    print(f"""
╔════════════════════════════════════════════════════╗
║  📱 Billing System SMS Gateway Backend              ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║  Framework: Flask + Python                          ║
║  Gateway: Fast2SMS                                  ║
║  Port: {PORT}                                       ║
║  Environment: {os.getenv('FLASK_ENV', 'development')}                                 ║
║  API Configured: {'✅ YES' if FAST2SMS_API_KEY else '❌ NO'}                              ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║  Endpoints:                                         ║
║  • POST /api/send-sms                               ║
║  • POST /api/send-sms-batch                         ║
║  • GET /api/health                                  ║
║  • GET /api/status                                  ║
║  • GET /api/test-sms (dev only)                     ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║  Ready to receive SMS requests! 🚀                  ║
╚════════════════════════════════════════════════════╝
    """)
    
    # Validate configuration
    if not FAST2SMS_API_KEY:
        logger.warning('⚠️  WARNING: FAST2SMS_API_KEY not set in environment')
        logger.warning('   Set it with: export FAST2SMS_API_KEY=your_key')
        logger.warning('   Or add to .env file')
    
    # Run server
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=os.getenv('FLASK_ENV') == 'development'
    )
