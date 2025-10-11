# 🚀 Quick Start Guide - Invoice Generator API

Get your invoice API up and running in 10 minutes!

---

## 📋 Prerequisites

- Python 3.11+
- pip
- Git (optional)

---

## ⚡ Installation (5 minutes)

### Step 1: Clone or Download

```bash
# Option A: Clone from Git
git clone https://github.com/yourusername/invoice-api.git
cd invoice-api

# Option B: Download and extract ZIP
# Then cd into the directory
```

### Step 2: Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate venv
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
# Minimum required:
# - SECRET_KEY (generate a random string)
# - EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 5: Initialize Database

```bash
# Create database tables
python -c "from app.database import init_db; init_db()"
```

---

## 🎯 Run the API (1 minute)

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**API is now running at:** http://localhost:8000

---

## 📚 Test the API (4 minutes)

### Option 1: Using Swagger UI (Easiest)

1. Open http://localhost:8000/docs in your browser
2. Click on **POST /auth/register**
3. Click "Try it out"
4. Enter your details and click "Execute"
5. Copy the response
6. Now try **POST /auth/login** to get your token
7. Click the "Authorize" button at the top
8. Paste your token and authorize
9. Now you can test all endpoints!

### Option 2: Using cURL

#### 1. Register a User

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "john_doe",
    "password": "securepass123",
    "full_name": "John Doe",
    "company_name": "Freelance Pro"
  }'
```

**Response:**
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "john_doe",
  "payment_link": "https://pay.yourdomain.com/pay/john_doe-1",
  ...
}
```

#### 2. Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**💡 Save your token!** You'll need it for all other requests.

#### 3. Create Your First Invoice

```bash
TOKEN="your_token_here"

curl -X POST http://localhost:8000/invoices/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "ACME Corporation",
    "client_email": "billing@acme.com",
    "client_phone": "+212600123456",
    "language": "ar",
    "currency": "MAD",
    "items": [
      {
        "name": "Web Development",
        "description": "E-commerce website",
        "quantity": 1,
        "price": 15000
      },
      {
        "name": "SEO Services",
        "quantity": 3,
        "price": 2000
      }
    ],
    "tax_rate": 20,
    "discount_rate": 10,
    "notes": "Payment within 30 days"
  }'
```

**Response:**
```json
{
  "id": 1,
  "invoice_number": "INV-20251002-1234",
  "total": 22680,
  "pdf_path": "./static/invoices/invoice_INV-20251002-1234.pdf",
  "payment_link": "https://pay.yourdomain.com/pay/john_doe-1?invoice=INV-20251002-1234",
  ...
}
```

#### 4. Download the PDF

```bash
curl -X GET http://localhost:8000/invoices/1/download \
  -H "Authorization: Bearer $TOKEN" \
  --output my_invoice.pdf
```

Open `my_invoice.pdf` - you'll see a beautiful bilingual invoice! 🎉

#### 5. Send Invoice by Email

```bash
curl -X POST http://localhost:8000/invoices/1/send-email \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Thank you for your business!"
  }'
```

---

## 🎨 What You Can Do Now

✅ **Create unlimited invoices**
✅ **Generate professional PDFs**
✅ **Send invoices via email**
✅ **Track invoice status**
✅ **Get payment links with QR codes**
✅ **Support both Arabic and English**
✅ **Multiple currencies**

---

## 📊 View Your Dashboard

```bash
curl -X GET http://localhost:8000/users/me/stats \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "total_invoices": 1,
  "status_breakdown": {
    "draft": 1,
    "sent": 0,
    "paid": 0,
    "cancelled": 0
  },
  "total_revenue": 0,
  "pending_amount": 0
}
```

---

## 🐳 Docker Deployment (Optional)

### Quick Deploy with Docker

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔧 Email Configuration

### Using Gmail (Free)

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Update your `.env`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-specific-password
EMAIL_FROM=your-email@gmail.com
```

### Using SendGrid (Recommended for Production)

1. Sign up at https://sendgrid.com (Free tier: 100 emails/day)
2. Get your API key
3. Update your `.env`:

```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USERNAME=apikey
EMAIL_PASSWORD=your-sendgrid-api-key
EMAIL_FROM=noreply@yourdomain.com
```

---

## 🚨 Troubleshooting

### Issue: "Module not found"
```bash
# Make sure venv is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Database error"
```bash
# Delete old database and recreate
rm invoices.db
python -c "from app.database import init_db; init_db()"
```

### Issue: "Email not sending"
- Check your email credentials in `.env`
- For Gmail, make sure you're using an App Password, not your regular password
- Check spam folder

### Issue: "PDF generation failed"
```bash
# Install system dependencies (Linux)
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0

# On Mac
brew install pango

# On Windows, WeasyPrint should work out of the box
```

---

## 📖 Next Steps

1. **Read Full Documentation**: See `API_DOCUMENTATION.md`
2. **Customize Templates**: Edit files in `app/templates/`
3. **Deploy to Production**: Use Railway, Render, or your own server
4. **Publish on RapidAPI**: Share your API with the world
5. **Add Payment Gateway**: Integrate Stripe/PayPal (coming soon)

---

## 💡 Pro Tips

- **Save your JWT token** - it's valid for 30 minutes
- **Use environment variables** - never commit `.env` to Git
- **Test with Swagger UI** - it's the fastest way to test endpoints
- **Enable HTTPS in production** - security first!
- **Backup your database** - regularly backup `invoices.db`

---

## 🎉 Congratulations!

You now have a fully functional invoice API running! 🚀

Need help? Check the docs or open an issue on GitHub.

**Happy invoicing! 💼**