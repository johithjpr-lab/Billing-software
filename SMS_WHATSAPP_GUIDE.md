# Bill Sharing via WhatsApp & SMS - Complete Guide

## Overview
The billing system now includes an enhanced **"Save & Share"** button that allows you to send bills to customers via:
- **WhatsApp** - Direct message with bill details
- **SMS** - Text message notification (requires SMS gateway setup)
- **Save Only** - Just save the bill locally

---

## Features

### 1. **Save & Share Modal**
When you click the **"Save & Share"** button, a modal appears with three options:

```
📱 Share Bill with Customer
├─ 💬 Send via WhatsApp
├─ 📧 Send via SMS
└─ 💾 Save Bill Only
```

### 2. **WhatsApp Integration**
- Opens WhatsApp Web automatically
- Sends complete bill details including:
  - Bill ID and Date
  - Customer Name & Mobile
  - All items with quantities, rates, and discounts
  - Subtotal, total discount, and grand total
  - Payment method and change amount
- Bill is automatically saved to local storage
- Receipt HTML file is automatically downloaded

**How it works:**
1. Click "Save & Share" button
2. Select "Send via WhatsApp"
3. WhatsApp Web opens with pre-filled bill message
4. Bill is saved locally
5. Receipt downloads automatically

### 3. **SMS Integration (NEW)**
- Sends bill details as SMS text message
- Supports Indian mobile numbers (with auto country code)
- Integrates with SMS gateways like:
  - **Fast2SMS** (India) - Recommended
  - **MSG91** (India)
  - **Twilio** (International)
  - **AWS SNS** (International)
  - **Exotel** (India)
- Bill is automatically saved to local storage
- Receipt HTML file is automatically downloaded

**How it works:**
1. Click "Save & Share" button
2. Select "Send via SMS"
3. SMS is sent to customer's phone
4. Bill is saved locally
5. Receipt downloads automatically

---

## Setup Instructions

### Prerequisites
- Valid customer mobile number must be entered in the "Customer Details" section
- For SMS: Backend server setup with SMS gateway API

### WhatsApp Setup (No Configuration Needed)
✅ Works out of the box!
- No API key required
- Uses WhatsApp's web.whatsapp.com service
- Customer must have WhatsApp installed/registered

### SMS Gateway Setup

#### Option 1: Fast2SMS (Recommended for India)
```javascript
// API Endpoint: https://www.fast2sms.com/dev/bulkV2
// 
// Setup Steps:
// 1. Register at https://www.fast2sms.com
// 2. Generate API key from dashboard
// 3. Create backend endpoint at /api/send-sms
// 4. Pass API key securely (never in frontend)
```

#### Option 2: MSG91
```javascript
// API Endpoint: https://api.msg91.com/apiv5/flow/
//
// Setup Steps:
// 1. Register at https://www.msg91.com
// 2. Get authentication key
// 3. Create backend endpoint
```

#### Option 3: Twilio (International)
```javascript
// API Endpoint: https://api.twilio.com/2010-04-01/Accounts/
//
// Setup Steps:
// 1. Register at https://www.twilio.com
// 2. Get Account SID and Auth Token
// 3. Create backend endpoint
```

---

## Backend Integration Example

### Node.js + Express Backend (Fast2SMS)

```javascript
// backend/routes/sms.js
const express = require('express');
const axios = require('axios');
const router = express.Router();

router.post('/api/send-sms', async (req, res) => {
  try {
    const { phone, message } = req.body;
    
    // Validate input
    if (!phone || !message) {
      return res.status(400).json({ 
        success: false, 
        error: 'Phone and message required' 
      });
    }

    // Send SMS via Fast2SMS
    const response = await axios.post(
      'https://www.fast2sms.com/dev/bulkV2',
      {
        phone: phone,
        message: message,
        route: 'dlt'
      },
      {
        headers: {
          'authorization': process.env.FAST2SMS_API_KEY,
          'Content-Type': 'application/json'
        }
      }
    );

    // Log for tracking
    console.log(`SMS sent to ${phone}:`, response.data);

    res.json({ 
      success: true, 
      message: 'SMS sent successfully',
      data: response.data 
    });

  } catch (error) {
    console.error('SMS Error:', error);
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});

module.exports = router;
```

### Python Flask Backend

```python
# backend/routes.py
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/api/send-sms', methods=['POST'])
def send_sms():
    try:
        data = request.json
        phone = data.get('phone')
        message = data.get('message')
        
        if not phone or not message:
            return jsonify({
                'success': False,
                'error': 'Phone and message required'
            }), 400
        
        # Send SMS via Fast2SMS
        headers = {
            'authorization': os.environ.get('FAST2SMS_API_KEY'),
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'https://www.fast2sms.com/dev/bulkV2',
            json={
                'phone': phone,
                'message': message,
                'route': 'dlt'
            },
            headers=headers
        )
        
        print(f"SMS sent to {phone}: {response.json()}")
        
        return jsonify({
            'success': True,
            'message': 'SMS sent successfully',
            'data': response.json()
        })
        
    except Exception as e:
        print(f"SMS Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### PHP Backend

```php
<?php
// backend/send-sms.php

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);
    $phone = $data['phone'] ?? '';
    $message = $data['message'] ?? '';
    
    if (!$phone || !$message) {
        http_response_code(400);
        echo json_encode([
            'success' => false,
            'error' => 'Phone and message required'
        ]);
        exit;
    }
    
    try {
        // Send SMS via Fast2SMS
        $url = 'https://www.fast2sms.com/dev/bulkV2';
        $apiKey = getenv('FAST2SMS_API_KEY');
        
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => $url,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => json_encode([
                'phone' => $phone,
                'message' => $message,
                'route' => 'dlt'
            ]),
            CURLOPT_HTTPHEADER => [
                'authorization: ' . $apiKey,
                'Content-Type: application/json'
            ]
        ]);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode === 200) {
            echo json_encode([
                'success' => true,
                'message' => 'SMS sent successfully',
                'data' => json_decode($response, true)
            ]);
        } else {
            http_response_code(500);
            echo json_encode([
                'success' => false,
                'error' => 'Failed to send SMS',
                'response' => json_decode($response, true)
            ]);
        }
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'error' => $e->getMessage()
        ]);
    }
}
?>
```

---

## Frontend Integration

After setting up your backend, uncomment the following code in `index.html`:

```javascript
// In sendViaSMSGateway function, line ~1050
// Uncomment this section:

/*
fetch('/api/send-sms', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload)
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
*/
```

---

## Usage Workflow

### Complete Bill Sharing Workflow:

```
1. Enter Customer Details
   ├─ Name
   └─ Mobile Number

2. Add Items to Bill
   ├─ Barcode/Item Code
   ├─ Item Name
   ├─ Quantity
   ├─ Rate
   └─ Discount (if any)

3. Review Bill Summary
   ├─ Subtotal
   ├─ Total Discount
   └─ Grand Total

4. Click "Save & Share" Button
   ├─ Modal appears with 3 options

5. Select Sharing Method
   ├─ WhatsApp: Opens WhatsApp Web
   ├─ SMS: Sends text message
   └─ Save Only: Just save locally

6. Bill is Automatically:
   ├─ Saved to browser storage
   ├─ Added to customer history
   └─ Downloaded as receipt.html
```

---

## Bill Message Format

### WhatsApp & SMS Message Includes:
```
        NOW100 SUPERMART
-----------------------------------------------
LG-05, Nirala Aspire Plaza
Greater Noida (W)
Ph: 8920903244
-----------------------------------------------
        TAX INVOICE
-----------------------------------------------
Bill No : B1704067200000
Date    : 1/1/2024, 10:30:45 AM
Customer: John Doe | Mobile: 9876543210
-----------------------------------------------
S.N Item          Qty  Rate      Disc   Amt
-----------------------------------------------
1   Milk          1    50.00     0%     50.00
2   Bread         2    40.00     10%    72.00
-----------------------------------------------
Subtotal          122.00
Discount          10.00
-----------------------------------------------
TOTAL             112.00
-----------------------------------------------
Payment : CASH  |  AMOUNT : 112.00
-----------------------------------------------
 Thank You! Visit Again 🙂
```

---

## Troubleshooting

### WhatsApp Not Opening?
- **Solution**: Check browser popup blocker settings
- **Solution**: Ensure customer has valid mobile number format
- **Solution**: Clear browser cache and try again

### SMS Not Being Sent?
- **Solution**: Check backend API endpoint is running
- **Solution**: Verify SMS gateway API key is valid
- **Solution**: Check SMS gateway account has credits
- **Solution**: Verify mobile number format (10-digit for India)
- **Solution**: Check browser console for error messages

### Customer Mobile Number Error?
- **Solution**: Ensure 10 or 12 digit number (with or without country code)
- **Solution**: Remove any special characters
- **Solution**: Format: `9876543210` or `919876543210`

### Bill Not Saving?
- **Solution**: Check browser storage space (localStorage)
- **Solution**: Try clearing browser cache
- **Solution**: Check console for error messages

---

## Customization

### Change SMS Gateway
Edit `sendViaSMSGateway()` function to use your preferred gateway:

```javascript
function sendViaSMSGateway(phoneNumber, message, gateway = 'YOUR_GATEWAY'){
  if(gateway === 'your_gateway'){
    // Your implementation
  }
}
```

### Customize Message Template
Edit `generateThermalText_NON_GST()` function to customize bill message:

```javascript
function generateThermalText_NON_GST(bill){
  let t = "";
  t += "Your custom header\n";
  // ... customize format
  return t;
}
```

### Add More Sharing Options
Add new buttons in `billShareModal`:

```html
<button class="btn primary" onclick="customFunction()">
  📤 Your Option
</button>
```

---

## Testing

### Test WhatsApp Integration:
1. Add test bill items
2. Enter customer mobile number
3. Click "Save & Share" → "Send via WhatsApp"
4. Verify WhatsApp Web opens with bill message
5. Verify bill saves to storage
6. Verify receipt downloads

### Test SMS Integration:
1. Ensure backend API is running
2. Add test bill items
3. Enter customer mobile number
4. Click "Save & Share" → "Send via SMS"
5. Check customer receives SMS
6. Verify bill saves to storage
7. Verify receipt downloads

---

## API References

- **Fast2SMS**: https://www.fast2sms.com/dev/docs
- **MSG91**: https://www.msg91.com/apidoc
- **Twilio**: https://www.twilio.com/docs/sms
- **AWS SNS**: https://docs.aws.amazon.com/sns/latest/dg/sms_publish-to-phone.html

---

## Support & Updates

For issues or feature requests, check:
- Browser Console (F12) for error messages
- Network tab for API call failures
- Local Storage for saved bills
- SMS gateway dashboard for delivery status

---

## Summary of Changes

✅ Added "Save & Share" button to replace "Save & WhatsApp"
✅ Created Bill Share Modal with three sharing options
✅ Enhanced WhatsApp integration with better message formatting
✅ Added new SMS sending functionality
✅ Created SMS notification system
✅ Added generatePrintableHTML function
✅ Supports multiple SMS gateways
✅ Backward compatible with existing bill saving
✅ Automatic receipt HTML download
✅ Customer history tracking

**Version:** 2.0
**Last Updated:** January 2026
