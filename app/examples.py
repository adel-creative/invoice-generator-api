"""
Code Examples for API Documentation
Provides code snippets in multiple languages for easy integration
"""

# cURL Examples
CURL_EXAMPLES = {
    "register": """
# Register new user
curl -X POST https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app/auth/register \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "freelancer@example.com",
    "username": "johndoe",
    "password": "securepass123",
    "full_name": "John Doe",
    "company_name": "Freelance Pro",
    "phone": "+212600123456"
  }'
""",
    
    "login": """
# Login and get JWT token
curl -X POST https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{
    "username": "johndoe",
    "password": "securepass123"
  }'

# Response contains access_token - save it!
""",
    
    "create_invoice": """
# Create invoice (requires authentication)
TOKEN="your_jwt_token_here"

curl -X POST https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app/invoices/generate \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "client_name": "ACME Corporation",
    "client_email": "billing@acme.com",
    "client_phone": "+212600123456",
    "language": "ar",
    "currency": "MAD",
    "items": [
      {
        "name": "تطوير موقع ويب",
        "description": "موقع تجارة إلكترونية كامل",
        "quantity": 1,
        "price": 15000
      },
      {
        "name": "استضافة سنوية",
        "quantity": 1,
        "price": 1200
      }
    ],
    "tax_rate": 20,
    "discount_rate": 10,
    "notes": "الدفع خلال 30 يوماً من تاريخ الفاتورة"
  }'
""",
    
    "send_email": """
# Send invoice via email
curl -X POST https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app/invoices/1/send-email \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "شكراً لتعاملكم معنا! نتطلع للعمل معكم مجدداً."
  }'
"""
}

# Python Examples
PYTHON_EXAMPLES = {
    "complete_workflow": """
import requests

BASE_URL = "https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app"

# 1. Register user
register_data = {
    "email": "freelancer@example.com",
    "username": "johndoe",
    "password": "securepass123",
    "company_name": "Freelance Pro"
}

response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
print(f"✅ User registered: {response.json()['username']}")

# 2. Login and get token
login_data = {
    "username": "johndoe",
    "password": "securepass123"
}

response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
token = response.json()["access_token"]
print(f"✅ Token received: {token[:20]}...")

# 3. Create invoice
headers = {"Authorization": f"Bearer {token}"}
invoice_data = {
    "client_name": "ACME Corporation",
    "client_email": "billing@acme.com",
    "language": "ar",
    "currency": "MAD",
    "items": [
        {
            "name": "Web Development",
            "description": "E-commerce website",
            "quantity": 1,
            "price": 15000
        }
    ],
    "tax_rate": 20,
    "discount_rate": 10
}

response = requests.post(
    f"{BASE_URL}/invoices/generate",
    json=invoice_data,
    headers=headers
)

invoice = response.json()
print(f"✅ Invoice created: {invoice['invoice_number']}")
print(f"   Total: {invoice['total']} {invoice['currency']}")
print(f"   PDF: {invoice['pdf_path']}")

# 4. Send email
response = requests.post(
    f"{BASE_URL}/invoices/{invoice['id']}/send-email",
    json={"message": "Thank you for your business!"},
    headers=headers
)

print(f"✅ Email sent to {invoice['client_email']}")

# 5. Download PDF
response = requests.get(
    f"{BASE_URL}/invoices/{invoice['id']}/download",
    headers=headers
)

with open(f"invoice_{invoice['invoice_number']}.pdf", "wb") as f:
    f.write(response.content)
    print(f"✅ PDF downloaded")
""",
    
    "error_handling": """
import requests

BASE_URL = "https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app"
headers = {"Authorization": f"Bearer {token}"}

try:
    response = requests.post(
        f"{BASE_URL}/invoices/generate",
        json=invoice_data,
        headers=headers
    )
    response.raise_for_status()  # Raise exception for 4xx/5xx
    
    invoice = response.json()
    print(f"✅ Success: {invoice['invoice_number']}")
    
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("❌ Authentication failed - token expired or invalid")
    elif e.response.status_code == 422:
        print(f"❌ Validation error: {e.response.json()['detail']}")
    elif e.response.status_code == 429:
        print("❌ Rate limit exceeded - wait before retrying")
    else:
        print(f"❌ Error {e.response.status_code}: {e.response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to API server")
"""
}

# JavaScript/Node.js Examples
JAVASCRIPT_EXAMPLES = {
    "fetch_api": """
// Using Fetch API (Browser/Node.js 18+)

const BASE_URL = 'https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app';

// 1. Login
async function login(username, password) {
    const response = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    return data.access_token;
}

// 2. Create Invoice
async function createInvoice(token, invoiceData) {
    const response = await fetch(`${BASE_URL}/invoices/generate`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(invoiceData)
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// Usage
(async () => {
    try {
        const token = await login('johndoe', 'securepass123');
        console.log('✅ Logged in');
        
        const invoice = await createInvoice(token, {
            client_name: 'ACME Corp',
            client_email: 'billing@acme.com',
            language: 'en',
            currency: 'USD',
            items: [
                { name: 'Web Development', quantity: 1, price: 5000 }
            ],
            tax_rate: 10
        });
        
        console.log(`✅ Invoice created: ${invoice.invoice_number}`);
    } catch (error) {
        console.error('❌ Error:', error.message);
    }
})();
""",
    
    "axios": """
// Using Axios (Node.js)
const axios = require('axios');

const BASE_URL = 'https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app';

// Create axios instance with interceptors
const api = axios.create({
    baseURL: BASE_URL,
    headers: { 'Content-Type': 'application/json' }
});

// Add token to all requests
let authToken = null;

api.interceptors.request.use(config => {
    if (authToken) {
        config.headers.Authorization = `Bearer ${authToken}`;
    }
    return config;
});

// Handle errors
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response) {
            console.error(`Error ${error.response.status}:`, error.response.data);
        }
        return Promise.reject(error);
    }
);

// Usage
(async () => {
    // Login
    const loginResponse = await api.post('/auth/login', {
        username: 'johndoe',
        password: 'securepass123'
    });
    authToken = loginResponse.data.access_token;
    
    // Create Invoice
    const invoiceResponse = await api.post('/invoices/generate', {
        client_name: 'ACME Corp',
        client_email: 'billing@acme.com',
        language: 'ar',
        currency: 'MAD',
        items: [
            { name: 'خدمة استشارية', quantity: 10, price: 500 }
        ]
    });
    
    console.log('Invoice:', invoiceResponse.data);
})();
"""
}

# PHP Examples
PHP_EXAMPLES = {
    "guzzle": """
<?php
// Using Guzzle HTTP Client

require 'vendor/autoload.php';

use GuzzleHttp\\Client;

$client = new Client([
    'base_uri' => 'https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app',
    'headers' => ['Content-Type' => 'application/json']
]);

// 1. Login
$response = $client->post('/auth/login', [
    'json' => [
        'username' => 'johndoe',
        'password' => 'securepass123'
    ]
]);

$token = json_decode($response->getBody())->access_token;

// 2. Create Invoice
$response = $client->post('/invoices/generate', [
    'headers' => ['Authorization' => "Bearer $token"],
    'json' => [
        'client_name' => 'ACME Corporation',
        'client_email' => 'billing@acme.com',
        'language' => 'ar',
        'currency' => 'MAD',
        'items' => [
            [
                'name' => 'Web Development',
                'quantity' => 1,
                'price' => 15000
            ]
        ],
        'tax_rate' => 20
    ]
]);

$invoice = json_decode($response->getBody());
echo "Invoice created: {$invoice->invoice_number}\\n";
?>
"""
}

# Response Examples
RESPONSE_EXAMPLES = {
    "successful_invoice": {
        "id": 1,
        "invoice_number": "INV-20251002-1234",
        "user_id": 1,
        "client_name": "ACME Corporation",
        "client_email": "billing@acme.com",
        "language": "ar",
        "currency": "MAD",
        "items": [
            {
                "name": "تطوير موقع ويب",
                "description": "موقع تجارة إلكترونية",
                "quantity": 1,
                "price": 15000,
                "total": 15000
            }
        ],
        "subtotal": 15000,
        "tax_rate": 20,
        "tax_amount": 2700,
        "discount_rate": 10,
        "discount_amount": 1500,
        "total": 16200,
        "status": "draft",
        "pdf_path": "./static/invoices/invoice_INV-20251002-1234.pdf",
        "qr_code_path": "./static/qr_codes/invoice_INV-20251002-1234_qr.png",
        "payment_link": "https://pay.yourdomain.com/pay/johndoe-1?invoice=INV-20251002-1234"
    },
    
    "validation_error": {
        "detail": [
            {
                "loc": ["body", "client_email"],
                "msg": "value is not a valid email address",
                "type": "value_error.email"
            },
            {
                "loc": ["body", "items"],
                "msg": "ensure this value has at least 1 items",
                "type": "value_error.list.min_items"
            }
        ]
    },
    
    "authentication_error": {
        "detail": "Could not validate credentials"
    },
    
    "rate_limit_error": {
        "detail": "Email rate limit exceeded. Maximum 5 emails per hour."
    }
}

# Integration Examples
INTEGRATION_EXAMPLES = {
    "wordpress": """
// WordPress Integration Example
// Add to your theme's functions.php

function create_invoice_via_api($client_name, $client_email, $amount) {
    $api_url = 'https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app
    $token = get_option('invoice_api_token'); // Store token in WP options
    
    $invoice_data = array(
        'client_name' => $client_name,
        'client_email' => $client_email,
        'language' => 'en',
        'currency' => 'USD',
        'items' => array(
            array(
                'name' => 'Service',
                'quantity' => 1,
                'price' => $amount
            )
        )
    );
    
    $response = wp_remote_post($api_url . '/invoices/generate', array(
        'headers' => array(
            'Authorization' => 'Bearer ' . $token,
            'Content-Type' => 'application/json'
        ),
        'body' => json_encode($invoice_data)
    ));
    
    if (is_wp_error($response)) {
        return false;
    }
    
    return json_decode(wp_remote_retrieve_body($response));
}
""",
    
    "zapier": """
// Zapier Webhook Integration
// Use in Zapier "Webhooks by Zapier" action

// Step 1: Login (do this once, store token)
POST https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app/auth/login
Body: {
  "username": "your_username",
  "password": "your_password"
}

// Step 2: Create Invoice (use in Zap)
POST https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app/invoices/generate
Headers:
  Authorization: Bearer {{token}}
  Content-Type: application/json
Body: {
  "client_name": "{{client_name}}",
  "client_email": "{{client_email}}",
  "language": "en",
  "currency": "USD",
  "items": [
    {
      "name": "{{service_name}}",
      "quantity": 1,
      "price": {{amount}}
    }
  ]
}
""",
    
    "n8n": """
// n8n Workflow Integration
// HTTP Request Node Configuration

{
  "method": "POST",
  "url": "https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app/invoices/generate",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "httpHeaderAuth": {
    "name": "Authorization",
    "value": "Bearer {{$credentials.invoiceApiToken}}"
  },
  "body": {
    "client_name": "={{$json.client_name}}",
    "client_email": "={{$json.client_email}}",
    "language": "ar",
    "currency": "MAD",
    "items": [
      {
        "name": "={{$json.service}}",
        "quantity": 1,
        "price": "={{$json.amount}}"
      }
    ],
    "tax_rate": 20
  }
}
"""
}

# Best Practices
BEST_PRACTICES = {
    "token_management": """
# Token Management Best Practices

## 1. Store Tokens Securely
- Never commit tokens to version control
- Use environment variables
- Store in secure credential managers

## 2. Handle Token Expiration
- Tokens expire after 30 minutes
- Implement automatic refresh logic
- Catch 401 errors and re-authenticate

## 3. Example Implementation

import os
import time
import requests

class InvoiceAPI:
    def __init__(self):
        self.base_url = os.getenv('INVOICE_API_URL')
        self.username = os.getenv('INVOICE_API_USERNAME')
        self.password = os.getenv('INVOICE_API_PASSWORD')
        self.token = None
        self.token_expires_at = 0
    
    def get_token(self):
        # Check if token is still valid
        if self.token and time.time() < self.token_expires_at:
            return self.token
        
        # Get new token
        response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "username": self.username,
                "password": self.password
            }
        )
        
        data = response.json()
        self.token = data['access_token']
        # Token expires in 30 minutes, refresh 5 min before
        self.token_expires_at = time.time() + (25 * 60)
        
        return self.token
    
    def create_invoice(self, invoice_data):
        token = self.get_token()
        
        response = requests.post(
            f"{self.base_url}/invoices/generate",
            headers={"Authorization": f"Bearer {token}"},
            json=invoice_data
        )
        
        # Handle token expiration
        if response.status_code == 401:
            # Token expired, get new one and retry
            self.token = None
            return self.create_invoice(invoice_data)
        
        response.raise_for_status()
        return response.json()

# Usage
api = InvoiceAPI()
invoice = api.create_invoice({
    "client_name": "Client",
    "client_email": "client@example.com",
    "language": "en",
    "currency": "USD",
    "items": [{"name": "Service", "quantity": 1, "price": 100}]
})
""",
    
    "error_handling": """
# Error Handling Best Practices

## Handle All Error Types

import requests
from requests.exceptions import RequestException

def safe_api_call(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            
            if status == 401:
                print("❌ Authentication failed")
            elif status == 403:
                print("❌ Access forbidden")
            elif status == 404:
                print("❌ Resource not found")
            elif status == 422:
                errors = e.response.json().get('detail', [])
                print("❌ Validation errors:")
                for error in errors:
                    print(f"  - {error['msg']} in {error['loc']}")
            elif status == 429:
                print("❌ Rate limit exceeded")
            elif status >= 500:
                print("❌ Server error - retry later")
            
            return None
            
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to API")
            return None
            
        except requests.exceptions.Timeout:
            print("❌ Request timeout")
            return None
            
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return None
    
    return wrapper

@safe_api_call
def create_invoice(token, data):
    response = requests.post(
        "https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app/invoices/generate",
        headers={"Authorization": f"Bearer {token}"},
        json=data,
        timeout=30
    )
    response.raise_for_status()
    return response.json()
""",
    
    "rate_limiting": """
# Rate Limiting Best Practices

## Respect Rate Limits

import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests=5, window_seconds=3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = deque()
    
    def can_make_request(self):
        now = time.time()
        
        # Remove old requests outside window
        while self.requests and self.requests[0] < now - self.window_seconds:
            self.requests.popleft()
        
        return len(self.requests) < self.max_requests
    
    def record_request(self):
        self.requests.append(time.time())
    
    def wait_time(self):
        if self.can_make_request():
            return 0
        
        # Time until oldest request expires
        oldest = self.requests[0]
        return (oldest + self.window_seconds) - time.time()

# Usage for email sending (5 per hour limit)
email_limiter = RateLimiter(max_requests=5, window_seconds=3600)

def send_invoice_email(invoice_id, token):
    if not email_limiter.can_make_request():
        wait = email_limiter.wait_time()
        print(f"⏳ Rate limit reached. Wait {wait:.0f} seconds")
        return False
    
    # Make request
    response = requests.post(
        f"https://screeching-tildi-adelzidoune-ca9a7151.koyeb.appinvoices/{invoice_id}/send-email",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        email_limiter.record_request()
        return True
    
    return False
"""
}

# Quick Reference
QUICK_REFERENCE = {
    "endpoints": {
        "Authentication": {
            "POST /auth/register": "Register new user",
            "POST /auth/login": "Login and get token"
        },
        "Invoices": {
            "POST /invoices/generate": "Create new invoice",
            "GET /invoices/{id}": "Get invoice by ID",
            "GET /invoices/": "List all invoices",
            "GET /invoices/{id}/download": "Download PDF",
            "POST /invoices/{id}/send-email": "Send via email",
            "PUT /invoices/{id}": "Update invoice",
            "DELETE /invoices/{id}": "Delete invoice"
        },
        "Users": {
            "GET /users/me": "Get current user",
            "PUT /users/me": "Update profile",
            "GET /users/me/stats": "Get statistics"
        }
    },
    
    "common_fields": {
        "language": "ar (Arabic) or en (English)",
        "currency": "MAD, USD, EUR, SAR, AED, GBP, EGP",
        "status": "draft, sent, paid, cancelled, overdue",
        "tax_rate": "0-100 (percentage)",
        "discount_rate": "0-100 (percentage)"
    },
    
    "rate_limits": {
        "email_sending": "5 requests per hour per user",
        "other_endpoints": "No limit (MVP)"
    }
}
