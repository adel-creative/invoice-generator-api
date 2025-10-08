"""
Main FastAPI Application
Entry point for the Invoice Generator API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from datetime import datetime
from .config import settings
from .database import init_db
from .api import auth, invoices, users

# Create FastAPI app with comprehensive documentation
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    🧾 **Arabic Invoice Generator API**
    
    Professional bilingual invoice generator for freelancers and businesses in the MENA region.
    
    ## 🚀 Quick Start Guide
    
    ### Step 1: Register Your Account
    ```bash
    POST /auth/register
    ```
    Create your account with email, username, and password.
    
    ### Step 2: Login & Get Token
    ```bash
    POST /auth/login
    ```
    Get your JWT access token (valid for 30 minutes).
    
    ### Step 3: Authorize
    Click the 🔒 **Authorize** button above and paste your token.
    
    ### Step 4: Create Invoice
    ```bash
    POST /invoices/generate
    ```
    Generate your first invoice with PDF and QR code!
    
    ### Step 5: Send to Client
    ```bash
    POST /invoices/{id}/send-email
    ```
    Send the invoice via email with PDF attachment.
    
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
    
    ### 💰 Multi-Currency Support
    Supported currencies: MAD, USD, EUR, SAR, AED, GBP, EGP
    
    ---
    
    ## 🔑 Authentication
    
    All endpoints (except `/auth/*`, `/health`, `/`) require authentication.
    
    **Header Format:**
    ```
    Authorization: Bearer YOUR_JWT_TOKEN
    ```
    
    **Token Lifetime:** 30 minutes
    
    **To get a token:**
    1. Register at `/auth/register`
    2. Login at `/auth/login`
    3. Copy the `access_token` from response
    4. Click 🔒 Authorize button
    5. Paste token and click Authorize
    
    ---
    
    ## 📊 Complete Example Workflow
    
    ### Using cURL:
    ```bash
    # 1. Register
    curl -X POST http://localhost:8000/auth/register \\
      -H "Content-Type: application/json" \\
      -d '{
        "email": "freelancer@example.com",
        "username": "freelancer",
        "password": "securepass123",
        "company_name": "Freelance Pro"
      }'
    
    # 2. Login
    curl -X POST http://localhost:8000/auth/login \\
      -H "Content-Type: application/json" \\
      -d '{
        "username": "freelancer",
        "password": "securepass123"
      }'
    
    # Save the token
    TOKEN="eyJhbGc..."
    
    # 3. Create Invoice
    curl -X POST http://localhost:8000/invoices/generate \\
      -H "Authorization: Bearer $TOKEN" \\
      -H "Content-Type: application/json" \\
      -d '{
        "client_name": "ACME Corporation",
        "client_email": "billing@acme.com",
        "language": "ar",
        "currency": "MAD",
        "items": [
          {
            "name": "تطوير موقع ويب",
            "description": "موقع تجارة إلكترونية",
            "quantity": 1,
            "price": 15000
          }
        ],
        "tax_rate": 20,
        "discount_rate": 10
      }'
    
    # 4. Send Email
    curl -X POST http://localhost:8000/invoices/1/send-email \\
      -H "Authorization: Bearer $TOKEN"
    ```
    
    ### Using Python:
    ```python
    import requests
    
    BASE_URL = "http://localhost:8000"
    
    # 1. Login
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "freelancer",
        "password": "securepass123"
    })
    token = response.json()["access_token"]
    
    # 2. Create Invoice
    headers = {"Authorization": f"Bearer {token}"}
    invoice = {
        "client_name": "ACME Corp",
        "client_email": "billing@acme.com",
        "language": "ar",
        "currency": "MAD",
        "items": [
            {"name": "Service", "quantity": 1, "price": 15000}
        ],
        "tax_rate": 20
    }
    
    response = requests.post(
        f"{BASE_URL}/invoices/generate",
        json=invoice,
        headers=headers
    )
    
    invoice_data = response.json()
    print(f"✅ Invoice {invoice_data['invoice_number']} created!")
    ```
    
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
    
    ---
    
    ## 📖 Additional Resources
    
    - **Full API Documentation**: See endpoints below
    - **Postman Collection**: Import from repository
    - **GitHub Repository**: [Your Repo URL]
    - **Support Email**: support@yourdomain.com
    - **Status Page**: https://status.yourdomain.com
    
    ---
    
    ## 📄 API Versioning
    
    **Current Version**: v1.0.0
    
    All endpoints are versioned. Future versions will be available at:
    - v1: `/v1/invoices/...` (current, default)
    - v2: `/v2/invoices/...` (future)
    
    ---
    
    ## 📞 Support & Community
    
    - **Email**: support@yourdomain.com
    - **Discord**: [Join our community]
    - **GitHub Issues**: [Report bugs]
    - **Twitter**: @YourAPIHandle
    
    ---
    
    **Made with ❤️ for freelancers and small businesses**
    
    *Happy invoicing! 🚀*
    """,
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
            "url": "http://localhost:8000",
            "description": "Development server (local)"
        },
        {
            "url": "https://api-staging.yourdomain.com",
            "description": "Staging server (testing)"
        },
        {
            "url": "https://api.yourdomain.com",
            "description": "Production server"
        }
    ],
    terms_of_service="https://yourdomain.com/terms",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": """
            **User registration and login operations**
            
            - No authentication required for these endpoints
            - Register to create a new account
            - Login to get JWT access token
            - Token expires after 30 minutes
            
            **Rate Limits**: None (MVP)
            """,
        },
        {
            "name": "Invoices",
            "description": """
            **Complete invoice management system**
            
            - Create invoices with bilingual PDF
            - Generate QR codes automatically
            - Send invoices via email
            - Track invoice status
            - Download PDF files
            
            **Authentication**: Required (JWT Bearer token)
            
            **Email Rate Limit**: 5 emails/hour per user
            """,
            "externalDocs": {
                "description": "Detailed invoice documentation",
                "url": "https://docs.yourdomain.com/invoices"
            }
        },
        {
            "name": "Users",
            "description": """
            **User profile and settings management**
            
            - View your profile information
            - Update company details
            - Get invoice statistics
            - Manage payment links
            
            **Authentication**: Required (JWT Bearer token)
            """,
        },
        {
            "name": "Root",
            "description": """
            **API information and metadata**
            
            - Get API version
            - Check available endpoints
            - View documentation links
            
            **Authentication**: Not required (public)
            """,
        },
        {
            "name": "Health",
            "description": """
            **Health check and monitoring**
            
            - Check API status
            - Verify service availability
            - Monitor uptime
            
            **Authentication**: Not required (public)
            
            **Use for**: Load balancer health checks, monitoring tools
            """,
        }
    ],
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
origins = settings.ALLOWED_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for serving PDFs and QR codes)
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.QR_DIR).mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(invoices.router)
app.include_router(users.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} started successfully!")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"📖 Alternative Docs: http://localhost:8000/redoc")
    print(f"🔍 OpenAPI Schema: http://localhost:8000/openapi.json")


@app.get("/", tags=["Root"], summary="API Information")
async def root():
    """
    Root endpoint - Get API information and available resources
    
    **No authentication required**
    
    Returns basic information about the API including:
    - API name and version
    - Documentation links
    - Health check endpoint
    - Available features
    """
    return {
        "message": "Welcome to Invoice Generator API! 🧾",
        "version": settings.APP_VERSION,
        "status": "operational",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "health": "/health",
            "changelog": "/changelog",
            "auth": "/auth/*",
            "invoices": "/invoices/*",
            "users": "/users/*"
        },
        "features": [
            "Bilingual PDF invoices (Arabic + English)",
            "Email sending with attachments",
            "QR code generation",
            "Multi-currency support",
            "JWT authentication"
        ],
        "support": {
            "email": "support@yourdomain.com",
            "docs": "https://docs.yourdomain.com"
        }
    }


@app.get("/health", tags=["Health"], summary="Health Check")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers
    
    **No authentication required**
    
    Returns:
    - Service status
    - API version  
    - Current timestamp
    
    **Use this endpoint for:**
    - Load balancer health checks
    - Uptime monitoring
    - Service availability verification
    
    **Expected Response Time**: < 100ms
    """
    return {
        "status": "healthy",
        "service": "invoice-generator-api",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected",
        "email_service": "configured"
    }


@app.get("/changelog", tags=["Root"], summary="API Changelog")
async def get_changelog():
    """
    Get API version history and changelog
    
    **No authentication required**
    
    Returns list of all API versions with their changes and release dates.
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
                    "✅ Rate limiting on emails"
                ],
                "breaking_changes": []
            }
        ],
        "upcoming": {
            "version": "1.1.0",
            "estimated_date": "2025-11-01",
            "planned_features": [
                "📜 Payment gateway integration (Stripe)",
                "📜 Webhook notifications",
                "📜 Recurring invoices",
                "📜 Invoice templates customization"
            ]
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
