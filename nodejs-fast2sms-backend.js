/**
 * Billing System - SMS Gateway Backend
 * Node.js + Express + Fast2SMS Integration
 * 
 * Usage:
 * npm install express axios dotenv cors
 * node nodejs-fast2sms-backend.js
 */

require('dotenv').config();
const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:8000',
  methods: ['POST', 'GET', 'OPTIONS'],
  credentials: true,
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Request logging middleware
app.use((req, res, next) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${req.method} ${req.path}`);
  next();
});

/**
 * Main SMS Sending Endpoint
 * POST /api/send-sms
 */
app.post('/api/send-sms', async (req, res) => {
  try {
    const { phone, message } = req.body;

    // Validate input
    if (!phone || !message) {
      console.warn('⚠️  Missing required fields: phone or message');
      return res.status(400).json({
        success: false,
        error: 'Phone number and message are required',
        timestamp: new Date().toISOString()
      });
    }

    // Validate phone format
    const phoneRegex = /^[0-9]{10,12}$/;
    if (!phoneRegex.test(phone.replace(/\D/g, ''))) {
      console.warn(`⚠️  Invalid phone format: ${phone}`);
      return res.status(400).json({
        success: false,
        error: 'Invalid phone number format (10-12 digits required)',
        timestamp: new Date().toISOString()
      });
    }

    // Validate API key
    const apiKey = process.env.FAST2SMS_API_KEY;
    if (!apiKey) {
      console.error('❌ FAST2SMS_API_KEY not configured');
      return res.status(500).json({
        success: false,
        error: 'SMS service not configured',
        timestamp: new Date().toISOString()
      });
    }

    // Send SMS via Fast2SMS
    console.log(`📤 Sending SMS to ${phone}...`);
    const response = await sendViaSMSFast2SMS(phone, message, apiKey);

    // Check response status
    if (response.success) {
      console.log(`✅ SMS sent successfully to ${phone}`);
      return res.json({
        success: true,
        message: 'SMS sent successfully',
        requestId: response.request_id || response.data?.request_id,
        timestamp: new Date().toISOString(),
        data: response
      });
    } else {
      console.error(`❌ SMS sending failed: ${response.message}`);
      return res.status(400).json({
        success: false,
        error: response.message || 'Failed to send SMS',
        timestamp: new Date().toISOString()
      });
    }

  } catch (error) {
    console.error('❌ Error in /api/send-sms:', error.message);
    
    let statusCode = 500;
    let errorMessage = error.message;

    // Handle specific error types
    if (error.response) {
      statusCode = error.response.status;
      errorMessage = error.response.data?.message || error.message;
      console.error('API Response Error:', error.response.data);
    } else if (error.code === 'ECONNREFUSED') {
      errorMessage = 'Cannot connect to SMS gateway';
    } else if (error.code === 'ENOTFOUND') {
      errorMessage = 'SMS gateway URL not found';
    }

    return res.status(statusCode).json({
      success: false,
      error: errorMessage,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * Send SMS via Fast2SMS API
 */
async function sendViaSMSFast2SMS(phone, message, apiKey) {
  try {
    const url = 'https://www.fast2sms.com/dev/bulkV2';
    
    // Fast2SMS requires numbers as string (comma-separated for multiple)
    // Remove any non-digit characters and ensure proper format
    const cleanPhone = phone.replace(/\D/g, '');
    
    // Validate phone number
    if (cleanPhone.length < 10 || cleanPhone.length > 12) {
      throw new Error('Invalid phone number format');
    }

    console.log(`📤 Sending SMS to ${cleanPhone} via Fast2SMS...`);
    console.log(`📝 Message length: ${message.length} characters`);

    const response = await axios({
      method: 'POST',
      url: url,
      headers: {
        'authorization': apiKey,
        'Content-Type': 'application/json'
      },
      data: {
        route: 'q', // 'q' for quick route (transactional, no sender ID needed), 'dlt' requires registered sender ID
        message: message,
        language: 'english',
        flash: 0,
        numbers: cleanPhone // Fast2SMS expects 'numbers' field
      },
      timeout: 15000 // 15 second timeout
    });

    console.log('📨 Fast2SMS API Response:', JSON.stringify(response.data, null, 2));

    // Fast2SMS returns { return: true/false, request_id: "...", message: "..." }
    if (response.data && response.data.return === true) {
      console.log(`✅ SMS sent successfully! Request ID: ${response.data.request_id}`);
      return {
        success: true,
        message: 'SMS sent successfully',
        request_id: response.data.request_id,
        data: response.data
      };
    } else {
      const errorMsg = response.data?.message || 'API returned error';
      console.error(`❌ Fast2SMS Error: ${errorMsg}`);
      
      // Provide helpful error messages
      let userFriendlyError = errorMsg;
      if (errorMsg.includes('transaction') || errorMsg.includes('100 INR') || errorMsg.includes('complete one transaction')) {
        userFriendlyError = '⚠️ Fast2SMS Account Verification Required:\n\nYour Fast2SMS account needs to be verified before sending SMS.\n\nTo fix this:\n1. Login to https://www.fast2sms.com/\n2. Complete a transaction of ₹100 or more (recharge your account)\n3. Wait for account verification\n4. Try sending SMS again\n\nAlternatively, contact Fast2SMS support for account activation.';
      } else if (errorMsg.includes('balance') || errorMsg.includes('credit') || errorMsg.includes('insufficient')) {
        userFriendlyError = '⚠️ Insufficient Fast2SMS Balance:\n\nYour Fast2SMS account has insufficient balance.\n\nTo fix this:\n1. Login to https://www.fast2sms.com/\n2. Recharge your account with sufficient balance\n3. Try sending SMS again';
      } else if (errorMsg.includes('invalid') || errorMsg.includes('Invalid') || errorMsg.includes('Sender ID')) {
        userFriendlyError = '⚠️ Fast2SMS Configuration Issue:\n\n' + errorMsg + '\n\nTo fix this:\n1. Check your Fast2SMS API key in .env file\n2. Verify phone number format (10-12 digits)\n3. If using DLT route, register a Sender ID in Fast2SMS dashboard\n4. Try using Quick route (q) instead of DLT route';
      } else if (errorMsg.includes('unauthorized') || errorMsg.includes('Unauthorized')) {
        userFriendlyError = '⚠️ Invalid Fast2SMS API Key:\n\nYour API key is invalid or expired.\n\nTo fix this:\n1. Login to https://www.fast2sms.com/\n2. Go to Dashboard → API\n3. Generate a new API key\n4. Update the API key in .env file\n5. Restart the backend server';
      }
      
      return {
        success: false,
        message: userFriendlyError,
        originalError: errorMsg,
        data: response.data
      };
    }

  } catch (error) {
    console.error('❌ Fast2SMS API Error:', error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
      throw new Error(error.response.data?.message || error.message);
    }
    throw error;
  }
}

/**
 * Health Check Endpoint
 * GET /api/health
 */
app.get('/api/health', (req, res) => {
  res.json({
    status: 'OK',
    service: 'Billing System SMS Gateway',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    configured: !!process.env.FAST2SMS_API_KEY
  });
});

/**
 * Status Endpoint
 * GET /api/status
 */
app.get('/api/status', (req, res) => {
  res.json({
    status: 'active',
    gateway: 'Fast2SMS',
    timestamp: new Date().toISOString(),
    apiConfigured: !!process.env.FAST2SMS_API_KEY,
    corsEnabled: !!process.env.CORS_ORIGIN,
    nodeVersion: process.version,
    environment: process.env.NODE_ENV || 'development'
  });
});

/**
 * Test SMS Endpoint (Development Only)
 * GET /api/test-sms?phone=919876543210
 */
app.get('/api/test-sms', async (req, res) => {
  if (process.env.NODE_ENV === 'production') {
    return res.status(403).json({
      success: false,
      error: 'Test endpoint disabled in production'
    });
  }

  const phone = req.query.phone;
  if (!phone) {
    return res.status(400).json({
      success: false,
      error: 'phone query parameter required'
    });
  }

  try {
    const testMessage = `TEST SMS from Billing System - ${new Date().toLocaleString()}`;
    const apiKey = process.env.FAST2SMS_API_KEY;

    const response = await sendViaSMSFast2SMS(phone, testMessage, apiKey);

    res.json({
      success: true,
      message: 'Test SMS sent',
      phone: phone,
      data: response
    });

  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * Batch SMS Endpoint
 * POST /api/send-sms-batch
 * Body: { smsList: [{ phone: "...", message: "..." }, ...] }
 */
app.post('/api/send-sms-batch', async (req, res) => {
  try {
    const { smsList } = req.body;

    if (!Array.isArray(smsList) || smsList.length === 0) {
      return res.status(400).json({
        success: false,
        error: 'smsList array required with at least one item'
      });
    }

    if (smsList.length > 100) {
      return res.status(400).json({
        success: false,
        error: 'Maximum 100 SMS per batch'
      });
    }

    const results = [];
    const apiKey = process.env.FAST2SMS_API_KEY;

    console.log(`📤 Sending ${smsList.length} SMS messages...`);

    for (const sms of smsList) {
      try {
        const result = await sendViaSMSFast2SMS(sms.phone, sms.message, apiKey);
        results.push({
          phone: sms.phone,
          success: result.success,
          message: result.message
        });
      } catch (error) {
        results.push({
          phone: sms.phone,
          success: false,
          error: error.message
        });
      }
    }

    const successful = results.filter(r => r.success).length;
    console.log(`✅ Batch complete: ${successful}/${smsList.length} sent`);

    res.json({
      success: true,
      message: `Batch sent: ${successful}/${smsList.length} successful`,
      results: results,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('❌ Batch SMS Error:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * 404 Handler
 */
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Endpoint not found',
    path: req.path,
    method: req.method
  });
});

/**
 * Error Handler
 */
app.use((err, req, res, next) => {
  console.error('❌ Unhandled Error:', err);
  res.status(500).json({
    success: false,
    error: err.message || 'Internal server error',
    timestamp: new Date().toISOString()
  });
});

/**
 * Start Server
 */
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════════════╗
║  📱 Billing System SMS Gateway Backend              ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║  Gateway: Fast2SMS                                  ║
║  Port: ${PORT}                                       ║
║  Environment: ${process.env.NODE_ENV || 'development'}${' '.repeat(20 - (process.env.NODE_ENV || 'development').length)}║
║  API Configured: ${process.env.FAST2SMS_API_KEY ? '✅ YES' : '❌ NO'}${' '.repeat(26)}║
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
  `);

  // Validate configuration
  if (!process.env.FAST2SMS_API_KEY) {
    console.warn('⚠️  WARNING: FAST2SMS_API_KEY not set in environment');
    console.warn('   Set it with: export FAST2SMS_API_KEY=your_key');
    console.warn('   Or add to .env file');
  }
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('📛 SIGTERM received, shutting down gracefully...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('📛 SIGINT received, shutting down gracefully...');
  process.exit(0);
});
