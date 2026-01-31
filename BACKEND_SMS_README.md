# SMS Gateway Backend Implementation Examples

This folder contains backend implementations for SMS sending functionality.

## Quick Start

Choose your preferred backend framework and SMS gateway:

### 1. Node.js + Express + Fast2SMS (Recommended)

**File:** `nodejs-fast2sms-backend.js`

**Setup:**
```bash
npm install express axios dotenv cors
npm install -g nodemon  # For development

# Create .env file
echo "FAST2SMS_API_KEY=your_api_key_here" > .env
echo "PORT=3000" >> .env

# Run server
nodemon nodejs-fast2sms-backend.js
```

### 2. Python + Flask + Fast2SMS

**File:** `python-flask-backend.py`

**Setup:**
```bash
pip install flask requests python-dotenv

# Create .env file
echo "FAST2SMS_API_KEY=your_api_key_here" > .env
echo "PORT=5000" >> .env

# Run server
python python-flask-backend.py
```

### 3. PHP + Fast2SMS

**File:** `php-backend.php`

**Setup:**
```bash
# Set environment variable or edit .env.php
# Place file in web server directory
# Access via: http://localhost/php-backend.php
```

## SMS Gateway Comparison

| Feature | Fast2SMS | MSG91 | Twilio | AWS SNS | Exotel |
|---------|----------|-------|--------|---------|--------|
| **Region** | India | India | Global | Global | India |
| **Setup** | Easy | Easy | Moderate | Complex | Easy |
| **Cost** | Low | Low | Moderate | Low | Low |
| **Speed** | Fast | Fast | Fast | Fast | Fast |
| **Reliability** | 95%+ | 95%+ | 99%+ | 99%+ | 95%+ |
| **DLT** | Yes | Yes | No | No | Yes |
| **Free Trial** | Yes (500) | Yes (100) | Yes ($15) | Yes | No |

## Environment Variables Needed

All backends require these environment variables:

```env
# SMS Gateway Credentials
SMS_GATEWAY=fast2sms           # Options: fast2sms, msg91, twilio, aws-sns, exotel
FAST2SMS_API_KEY=your_key      # Fast2SMS API Key
MSG91_AUTH_KEY=your_key        # MSG91 Auth Key
TWILIO_ACCOUNT_SID=your_sid    # Twilio Account SID
TWILIO_AUTH_TOKEN=your_token   # Twilio Auth Token
TWILIO_FROM_NUMBER=+1234567890 # Twilio Sender Number
AWS_ACCESS_KEY_ID=your_key     # AWS Access Key
AWS_SECRET_ACCESS_KEY=your_key # AWS Secret Key
AWS_SNS_REGION=us-east-1       # AWS Region

# Server Config
PORT=3000                       # Port to run server
NODE_ENV=development            # development or production
CORS_ORIGIN=http://localhost   # CORS origin for billing system
```

## API Endpoint

All backends expose this endpoint:

```
POST /api/send-sms

Headers:
  Content-Type: application/json

Body:
{
  "phone": "919876543210",
  "message": "Your bill message here"
}

Success Response:
{
  "success": true,
  "message": "SMS sent successfully",
  "data": { ... gateway response ... }
}

Error Response:
{
  "success": false,
  "error": "Error message here"
}
```

## Testing Endpoint

```bash
# Using curl
curl -X POST http://localhost:3000/api/send-sms \
  -H "Content-Type: application/json" \
  -d '{"phone":"919876543210","message":"Test message"}'

# Using Python
python -c "
import requests
requests.post('http://localhost:3000/api/send-sms', json={
  'phone': '919876543210',
  'message': 'Test message'
})
"

# Using JavaScript
fetch('/api/send-sms', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phone: '919876543210',
    message: 'Test message'
  })
})
.then(r => r.json())
.then(console.log)
```

## Production Deployment

### Using Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set FAST2SMS_API_KEY=your_key
heroku config:set CORS_ORIGIN=https://yourdomain.com

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Using AWS Lambda

See `aws-lambda-backend.js` for AWS Lambda implementation.

### Using Docker

```dockerfile
# Dockerfile
FROM node:16-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 3000
CMD ["node", "nodejs-fast2sms-backend.js"]
```

```bash
# Build and run
docker build -t billing-sms-backend .
docker run -p 3000:3000 -e FAST2SMS_API_KEY=your_key billing-sms-backend
```

## Frontend Configuration

Update the frontend code to use your backend:

In `index.html`, uncomment the fetch call in `sendViaSMSGateway()`:

```javascript
fetch('/api/send-sms', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phone: finalMobile,
    message: message
  })
})
.then(r => r.json())
.then(d => {
  if(d.success){
    showSMSNotification(phoneNumber, 'sent');
  } else {
    showSMSNotification(phoneNumber, 'failed');
  }
})
.catch(e => {
  console.error("SMS Error:", e);
  showSMSNotification(phoneNumber, 'failed');
});
```

## Troubleshooting

### Backend not running?
- Check PORT environment variable
- Verify no other service using same port
- Check console for error messages

### SMS not sending?
- Verify API credentials are correct
- Check SMS gateway account has credits
- Verify phone number format
- Check gateway API documentation

### CORS errors?
- Update CORS_ORIGIN environment variable
- Add your domain to CORS whitelist
- Check browser console for error details

### Slow response?
- Consider using async queues for bulk SMS
- Use caching for repeated messages
- Optimize gateway selection logic

## Next Steps

1. Choose your preferred backend and gateway
2. Install required dependencies
3. Set up environment variables
4. Test with provided examples
5. Deploy to your server
6. Update frontend CORS_ORIGIN
7. Test end-to-end SMS sending

For more details, check individual backend files.
