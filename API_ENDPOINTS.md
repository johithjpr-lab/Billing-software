# Billing System - Server Endpoints Documentation

## Server Configuration

### Frontend Server
- **URL**: http://localhost:8000
- **Port**: 8000
- **Type**: Static HTTP Server
- **Status**: ✅ Running

### Backend Server (Node.js + Flask)
- **URL**: http://localhost:3000
- **Port**: 3000
- **Type**: SMS Gateway API
- **Status**: ✅ Running

---

## Frontend Endpoints

### Main Page
```
GET http://localhost:8000/index.html
```
- Serves the billing system frontend
- Static HTML/CSS/JavaScript application
- Thermal printer integration

---

## Backend Health & Status Endpoints

### Health Check
```
GET http://localhost:3000/api/health
```
**Response:**
```json
{
  "status": "ok",
  "service": "Billing System SMS Gateway",
  "timestamp": "2026-01-31T15:05:34.747000"
}
```

### API Status
```
GET http://localhost:3000/api/status
```
**Response:**
```json
{
  "status": "active",
  "service": "Billing System SMS Gateway",
  "version": "1.0.0",
  "environment": "development",
  "endpoints": [
    "/api/health",
    "/api/send-sms",
    "/api/send-batch-sms",
    "/api/billing-notification",
    "/api/status"
  ],
  "timestamp": "2026-01-31T15:05:34.747000"
}
```

---

## SMS Gateway Endpoints

### Send Single SMS
```
POST http://localhost:3000/api/send-sms
Content-Type: application/json
```

**Request Body:**
```json
{
  "phone": "919876543210",
  "message": "Your billing amount is Rs. 500"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "SMS sent successfully",
  "phone": "919876543210",
  "timestamp": "2026-01-31T15:05:34.747000"
}
```

**Response (Error):**
```json
{
  "error": "Missing phone or message"
}
```

---

### Send Batch SMS
```
POST http://localhost:3000/api/send-batch-sms
Content-Type: application/json
```

**Request Body:**
```json
{
  "numbers": ["919876543210", "919987654321", "919876543212"],
  "message": "Your invoice is ready. Please collect from counter."
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Batch SMS sent successfully",
  "count": 3,
  "timestamp": "2026-01-31T15:05:34.747000"
}
```

**Response (Error):**
```json
{
  "error": "Invalid numbers list"
}
```

---

### Send Billing Notification
```
POST http://localhost:3000/api/billing-notification
Content-Type: application/json
```

**Request Body:**
```json
{
  "phone": "919876543210",
  "customer_name": "John Doe",
  "amount": "500",
  "invoice_id": "INV-001"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Billing notification sent",
  "timestamp": "2026-01-31T15:05:34.747000"
}
```

**Response (Error):**
```json
{
  "error": "Missing required fields"
}
```

---

## Testing the Endpoints

### Using cURL

**Test Health Check:**
```bash
curl http://localhost:3000/api/health
```

**Test Status:**
```bash
curl http://localhost:3000/api/status
```

**Test Send SMS:**
```bash
curl -X POST http://localhost:3000/api/send-sms \
  -H "Content-Type: application/json" \
  -d '{"phone":"919876543210","message":"Test SMS"}'
```

**Test Batch SMS:**
```bash
curl -X POST http://localhost:3000/api/send-batch-sms \
  -H "Content-Type: application/json" \
  -d '{"numbers":["919876543210","919987654321"],"message":"Batch test"}'
```

**Test Billing Notification:**
```bash
curl -X POST http://localhost:3000/api/billing-notification \
  -H "Content-Type: application/json" \
  -d '{"phone":"919876543210","customer_name":"John","amount":"500","invoice_id":"INV-001"}'
```

### Using Postman

1. Import these endpoints into Postman
2. Create requests for each endpoint
3. Test with sample data
4. Monitor responses

### Using JavaScript/Fetch

```javascript
// Send SMS
fetch('http://localhost:3000/api/send-sms', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phone: '919876543210',
    message: 'Your billing amount is Rs. 500'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Configuration

### Environment Variables (.env)
```
FAST2SMS_API_KEY=your_api_key_here
CORS_ORIGIN=http://localhost
PORT=3000
FLASK_ENV=development
NODE_ENV=development
```

### CORS Settings
- **Origin**: http://localhost
- **Methods**: POST, GET, OPTIONS
- **Headers**: Content-Type

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (Missing parameters) |
| 404 | Endpoint not found |
| 500 | Internal Server Error |

---

## Running Servers

### Frontend (Port 8000)
```bash
python -m http.server 8000
```

### Backend - Node.js (Port 3000)
```bash
npm run dev
```

### Backend - Python Flask (Port 3000)
```bash
python python-flask-backend.py
```

---

## Quick Links

- **Frontend**: http://localhost:8000/index.html
- **Health Check**: http://localhost:3000/api/health
- **Status**: http://localhost:3000/api/status
- **Documentation**: This file

---

**Last Updated**: January 31, 2026
**Version**: 1.0.0
