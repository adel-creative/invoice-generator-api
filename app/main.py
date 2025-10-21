"""
Main FastAPI Application
Entry point for the Invoice Generator API
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from .config import settings
from .database import init_db, SessionLocal
from .api import auth, invoices, users

# Setup comprehensive logging
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Create formatters
detailed_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
simple_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)

# Setup root logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(simple_formatter)

# File Handler - Rotating (10MB per file, keep 5 backups)
file_handler = RotatingFileHandler(
    logs_dir / "app.log",
    maxBytes=10_000_000,  # 10MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(detailed_formatter)

# Error File Handler - Rotating
error_handler = RotatingFileHandler(
    logs_dir / "errors.log",
    maxBytes=10_000_000,
    backupCount=5,
    encoding='utf-8'
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(detailed_formatter)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(error_handler)

# Build description without .format() to avoid KeyError
BASE_URL = settings.BASE_URL
API_DESCRIPTION = """
🧾 **Arabic Invoice Generator API**

Professional bilingual invoice generator for freelancers and businesses in the MENA region.

## 🚀 Quick Start Guide

### Step 1: Register Your Account
POST /auth/register - Create your account with email, username, and password.

### Step 2: Login & Get Token
POST /auth/login - Get your JWT access token (valid for 30 minutes).

### Step 3: Authorize
Click the 🔓 **Authorize** button above and paste your token.

### Step 4: Create Invoice
POST /invoices/generate - Generate your first invoice with PDF and QR code!

### Step 5: Send to Client
POST /invoices/[invoice_id]/send-email - Send the invoice via email with PDF attachment.

---

## 📚 Key Features

### 📄 Bilingual PDF Generation
- **Arabic (RTL)**: Native right-to-left support with Cairo font
- **English (LTR)**: Professional left-to-right layout
- Modern gradient design with company branding
- Print-ready A4 format

### 📧 Email Integration
- Send invoices directly to clients
- Professional HTML email templates
- PDF attachments included
- Rate limited: 5 emails/hour per user

### 💳 Payment Features
- Unique payment links per user
- QR codes for easy scanning
- Multiple currency support
- Ready for payment gateway integration

### 🔐 Security
- JWT-based authentication
- Password hashing with bcrypt
- Input validation with Pydantic
- CORS protection
- SQL injection prevention
- Security headers (HSTS, CSP, X-Frame-Options)

### 💰 Multi-Currency Support
Supported currencies: MAD, USD, EUR, SAR, AED, GBP, EGP

---

## 🔑 Authentication

All endpoints (except /auth/*, /health, /) require authentication.

**Header Format:**
Authorization: Bearer YOUR_JWT_TOKEN

**Token Lifetime:** 30 minutes

**To get a token:**
1. Register at /auth/register
2. Login at /auth/login
3. Copy the access_token from response
4. Click 🔓 Authorize button
5. Paste token and click Authorize

---

## ⚠️ Rate Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| Email Sending | 5 requests | per hour per user |
| Other Endpoints | No limit | (MVP) |

**429 Error**: If you exceed rate limits, wait 1 hour before retrying.

---

## 💰 Pricing Tiers (Suggested)

| Tier | Invoices/Month | Price/Month | Email Limit |
|------|----------------|-------------|-------------|
| **Free** | 10 | $0 | 5/day |
| **Starter** | 100 | $9.99 | 50/day |
| **Professional** | 500 | $29.99 | 200/day |
| **Business** | 2,000 | $79.99 | Unlimited |
| **Enterprise** | Unlimited | Custom | Unlimited |

---

## 🐛 Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| **401** | Unauthorized | Check your token, login again if expired |
| **403** | Forbidden | Your account might be inactive |
| **404** | Not Found | Invoice/resource doesn't exist |
| **422** | Validation Error | Check your request body format |
| **429** | Too Many Requests | Wait before sending more emails |
| **500** | Server Error | Contact support if persists |
| **503** | Service Unavailable | Database connection issue |

---

## 📖 Additional Resources

- **Full API Documentation**: See endpoints below
- **Support Email**: support@yourdomain.com

---

**Made with ❤️ for freelancers and small businesses**

*Happy invoicing! 🚀*
"""

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=API_DESCRIPTION,
    summary="Professional Invoice Generator API",
    contact={
        "name": "Invoice Generator API Support Team",
        "email": "support@yourdomain.com",
        "url": "https://yourdomain.com/contact"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    servers=[
        {
            "url": BASE_URL,
            "description": "Production Server"
        },
        {
            "url": "http://localhost:8000",
            "description": "Local Development Server"
        }
    ],
    terms_of_service="https://yourdomain.com/terms",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User registration and login operations. No authentication required for these endpoints.",
        },
        {
            "name": "Invoices",
            "description": "Complete invoice management system. Authentication required (JWT Bearer token). Email Rate Limit: 5 emails/hour per user.",
        },
        {
            "name": "Users",
            "description": "User profile and settings management. Authentication required (JWT Bearer token).",
        },
        {
            "name": "Root",
            "description": "API information and metadata. No authentication required.",
        },
        {
            "name": "Health",
            "description": "Health check and monitoring. No authentication required.",
        }
    ],
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    return response

# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = datetime.utcnow()
    
    # Log request
    logger.info(f"➡️  {request.method} {request.url.path} - Client: {request.client.host}")
    
    response = await call_next(request)
    
    # Calculate process time
    process_time = (datetime.utcnow() - start_time).total_seconds()
    
    # Log response
    logger.info(
        f"⬅️  {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# Global exception handler for unhandled errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"❌ Unhandled exception on {request.method} {request.url.path}: {str(exc)}",
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error. Please try again later.",
            "error_type": type(exc).__name__,
            "path": str(request.url.path)
        }
    )

# Validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"⚠️  Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body if hasattr(exc, 'body') else None
        }
    )

# CORS Configuration
try:
    origins = settings.ALLOWED_ORIGINS.split(",")
    logger.info(f"🌐 CORS enabled for origins: {origins}")
except Exception as e:
    logger.warning(f"⚠️  CORS configuration error, allowing all origins: {e}")
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for serving PDFs and QR codes)
try:
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.QR_DIR).mkdir(parents=True, exist_ok=True)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.info("📁 Static files mounted successfully")
except Exception as e:
    logger.warning(f"⚠️  Could not mount static files: {e}")

# Include routers
try:
    app.include_router(auth.router)
    app.include_router(invoices.router)
    app.include_router(users.router)
    logger.info("🔌 All routers included successfully")
except Exception as e:
    logger.error(f"❌ Error including routers: {e}")


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    try:
        init_db()
        logger.info("="*70)
        logger.info(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} started successfully!")
        logger.info(f"🌐 Base URL: {settings.BASE_URL}")
        logger.info(f"📚 API Documentation: {settings.BASE_URL}/docs")
        logger.info(f"📖 Alternative Docs: {settings.BASE_URL}/redoc")
        logger.info(f"🔍 OpenAPI Schema: {settings.BASE_URL}/openapi.json")
        logger.info(f"📊 Health Check: {settings.BASE_URL}/health")
        logger.info(f"📝 Logs Directory: {logs_dir.absolute()}")
        logger.info("="*70)
    except Exception as e:
        logger.error(f"❌ Startup error: {e}", exc_info=True)
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("🛑 Application shutting down...")


@app.get("/", tags=["Root"], summary="API Information")
async def root():
    """
    Root endpoint - Get API information and available resources
    
    **No authentication required**
    """
    return {
        "message": "Welcome to Invoice Generator API! 🧾",
        "version": settings.APP_VERSION,
        "status": "operational",
        "base_url": settings.BASE_URL,
        "documentation": {
            "swagger": f"{settings.BASE_URL}/docs",
            "redoc": f"{settings.BASE_URL}/redoc",
            "openapi": f"{settings.BASE_URL}/openapi.json"
        },
        "endpoints": {
            "health": f"{settings.BASE_URL}/health",
            "auth": f"{settings.BASE_URL}/auth/*",
            "invoices": f"{settings.BASE_URL}/invoices/*",
            "users": f"{settings.BASE_URL}/users/*"
        },
        "features": [
            "Bilingual PDF invoices (Arabic + English)",
            "Email sending with attachments",
            "QR code generation",
            "Multi-currency support",
            "JWT authentication",
            "Security headers (HSTS, CSP, etc.)",
            "Request/Error logging"
        ],
        "support": {
            "email": "support@yourdomain.com",
            "docs": "https://docs.yourdomain.com"
        }
    }


@app.get("/health", tags=["Health"], summary="Health Check")
async def health_check():
    """
    Comprehensive health check endpoint for monitoring and load balancers
    
    **No authentication required**
    """
    health_status = {
        "status": "healthy",
        "service": "invoice-generator-api",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    # Check Database Connection
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
        logger.error(f"❌ Database health check failed: {e}")
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}"
        }
    
    # Check File System
    try:
        test_file = Path(settings.UPLOAD_DIR) / ".health_check"
        test_file.write_text("OK")
        test_file.unlink()
        health_status["checks"]["filesystem"] = {
            "status": "healthy",
            "message": "File system access successful"
        }
    except Exception as e:
        logger.error(f"❌ Filesystem health check failed: {e}")
        health_status["checks"]["filesystem"] = {
            "status": "unhealthy",
            "message": f"File system access failed: {str(e)}"
        }
    
    # Check Email Configuration
    if settings.SMTP_HOST and settings.SMTP_PORT:
        health_status["checks"]["email"] = {
            "status": "configured",
            "message": f"Email service configured (SMTP: {settings.SMTP_HOST}:{settings.SMTP_PORT})"
        }
    else:
        health_status["checks"]["email"] = {
            "status": "not_configured",
            "message": "Email service not configured"
        }
    
    # Set appropriate HTTP status code
    status_code = 200 if health_status["status"] == "healthy" else 503
    
    return JSONResponse(content=health_status, status_code=status_code)


@app.get("/changelog", tags=["Root"], summary="API Changelog")
async def get_changelog():
    """
    Get API version history and changelog
    
    **No authentication required**
    """
    return {
        "current_version": settings.APP_VERSION,
        "versions": [
            {
                "version": "1.0.0",
                "release_date": "2025-10-02",
                "status": "stable",
                "changes": [
                    "✅ Initial MVP release",
                    "✅ Bilingual PDF generation (Arabic + English)",
                    "✅ JWT authentication system",
                    "✅ Email sending capability",
                    "✅ QR code generation",
                    "✅ Multi-currency support (7 currencies)",
                    "✅ Complete CRUD operations",
                    "✅ Rate limiting on emails",
                    "✅ Security headers (HSTS, CSP, X-Frame-Options)",
                    "✅ Comprehensive logging (file + console)",
                    "✅ Real database health checks",
                    "✅ Request/Response logging middleware"
                ],
                "breaking_changes": []
            }
        ],
        "upcoming": {
            "version": "1.1.0",
            "estimated_date": "2025-11-01",
            "planned_features": [
                "🔜 Payment gateway integration (Stripe)",
                "🔜 Webhook notifications",
                "🔜 Recurring invoices",
                "🔜 Invoice templates customization",
                "🔜 Redis caching layer",
                "🔜 API rate limiting (global)",
                "🔜 Prometheus metrics endpoint"
            ]
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 7860)),  # ✅ تغيير من 8000 لـ 7860
        reload=settings.DEBUG,
        log_config=None
    )
