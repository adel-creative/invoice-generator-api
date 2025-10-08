# 🧾 Arabic Invoice Generator API - MVP

## 📁 Project Structure

```
invoice-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration & environment variables
│   ├── database.py             # Database connection
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # User database model
│   │   └── invoice.py         # Invoice database model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py            # User Pydantic schemas
│   │   ├── invoice.py         # Invoice Pydantic schemas
│   │   └── auth.py            # Authentication schemas
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── invoices.py        # Invoice CRUD endpoints
│   │   └── users.py           # User management endpoints
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py    # JWT & password handling
│   │   ├── pdf_service.py     # PDF generation
│   │   ├── qr_service.py      # QR code generation
│   │   └── email_service.py   # Email sending
│   │
│   ├── templates/
│   │   ├── invoice_ar.html    # Arabic invoice template
│   │   └── invoice_en.html    # English invoice template
│   │
│   └── utils/
│       ├── __init__.py
│       ├── dependencies.py    # FastAPI dependencies
│       └── helpers.py         # Helper functions
│
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_invoices.py
│   └── test_services.py
│
├── alembic/                   # Database migrations
│   ├── versions/
│   └── env.py
│
├── static/                    # Generated PDFs & QR codes
│   ├── invoices/
│   └── qr_codes/
│
├── .env.example              # Environment variables template
├── .gitignore
├── requirements.txt
├── alembic.ini
├── README.md
└── docker-compose.yml        # Optional: for deployment
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd invoice-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env
```

### 3. Database Setup

```bash
# Initialize database
alembic upgrade head
```

### 4. Run the API

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Environment Variables

```env
# Database
DATABASE_URL=sqlite:///./invoices.db
# For PostgreSQL: postgresql://user:password@localhost/dbname

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (SendGrid example)
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USERNAME=apikey
EMAIL_PASSWORD=your-sendgrid-api-key
EMAIL_FROM=noreply@yourdomain.com

# App Settings
APP_NAME=Invoice Generator API
APP_VERSION=1.0.0
DEBUG=true
```

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/refresh` - Refresh access token

### Invoices
- `POST /invoices/generate` - Create new invoice
- `GET /invoices/{invoice_id}` - Get invoice by ID
- `GET /invoices/` - List all user invoices
- `GET /invoices/{invoice_id}/download` - Download PDF
- `POST /invoices/{invoice_id}/send-email` - Send invoice via email

### Users
- `GET /users/me` - Get current user info
- `PUT /users/me` - Update user profile

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_invoices.py -v
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📖 Features

✅ **MVP Features (Stage 1)**
- [x] Bilingual PDF generation (Arabic + English)
- [x] JWT Authentication
- [x] Invoice CRUD operations
- [x] QR Code generation
- [x] Unique payment links
- [x] Email sending capability
- [x] PDF download
- [x] RapidAPI ready

🔮 **Future Features**
- [ ] Payment gateway integration (Stripe, PayPal)
- [ ] Multi-language support
- [ ] Subscription tiers
- [ ] Advanced analytics
- [ ] Webhook notifications

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

MIT License - feel free to use for commercial projects

## 💬 Support

- Documentation: `/docs`
- Email: support@yourdomain.com
- Issues: GitHub Issues

---

**Made with ❤️ for freelancers and small businesses in MENA**