"""
Pydantic Schemas for Request/Response Validation
Compatible with Pydantic v2
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ==========================================
# User Schemas
# ==========================================

class UserRegister(BaseModel):
    """Schema for user registration"""
    email: EmailStr = Field(..., description="Valid email address")
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=50,
        description="Username (3-50 characters)"
    )
    password: str = Field(
        ..., 
        min_length=8,
        max_length=128,  # Reasonable maximum
        description="Password (8-128 characters)"
    )
    full_name: Optional[str] = Field(None, max_length=100)
    company_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """
        Validate password requirements:
        - Min 8 characters
        - Max 128 characters (to prevent abuse)
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v) > 128:
            raise ValueError('Password cannot exceed 128 characters')
        
        # Optional: Enforce strong password policy
        # Uncomment if you want stricter rules
        # if not any(c.isalpha() for c in v):
        #     raise ValueError('Password must contain at least one letter')
        # if not any(c.isdigit() for c in v):
        #     raise ValueError('Password must contain at least one number')
        
        return v
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """Validate username (alphanumeric and underscore only)"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, underscore, and hyphen')
        return v.lower()  # Store usernames in lowercase
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "freelancer@example.com",
                "username": "freelancer",
                "password": "SecurePass123!",
                "full_name": "Ahmed Freelancer",
                "company_name": "Freelance Pro",
                "phone": "+212600000000",
                "address": "123 Street, Casablanca, Morocco"
            }
        }
    }


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="Password")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "freelancer",
                "password": "SecurePass123!"
            }
        }
    }


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = Field(None, max_length=100)
    company_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "full_name": "Ahmed Updated",
                "company_name": "New Company LLC",
                "phone": "+212611222333",
                "address": "456 New Street, Rabat, Morocco"
            }
        }
    }


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    payment_link: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}  # ✅ Fixed: was orm_mode in v1


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(default=1800, description="Token expiration time in seconds")


# ==========================================
# Invoice Schemas
# ==========================================

class InvoiceLanguage(str, Enum):
    """Supported invoice languages"""
    ENGLISH = "en"
    ARABIC = "ar"
    FRENCH = "fr"


class InvoiceCurrency(str, Enum):
    """Supported currencies"""
    MAD = "MAD"
    USD = "USD"
    EUR = "EUR"
    SAR = "SAR"
    AED = "AED"
    GBP = "GBP"
    EGP = "EGP"


class InvoiceStatus(str, Enum):
    """Invoice status options"""
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    CANCELLED = "cancelled"


class InvoiceItemCreate(BaseModel):
    """Schema for creating an invoice item"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    quantity: float = Field(..., gt=0, description="Quantity must be greater than 0")
    price: float = Field(..., ge=0, description="Price must be 0 or greater")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Web Development Service",
                "description": "Full-stack e-commerce platform",
                "quantity": 1,
                "price": 15000.00
            }
        }
    }


class InvoiceItemResponse(InvoiceItemCreate):
    """Schema for invoice item response"""
    id: int
    invoice_id: int
    total: float
    
    model_config = {"from_attributes": True}  # ✅ Fixed: was orm_mode in v1


class InvoiceCreate(BaseModel):
    """Schema for creating an invoice"""
    client_name: str = Field(..., min_length=1, max_length=200)
    client_email: EmailStr
    client_phone: Optional[str] = Field(None, max_length=20)
    client_address: Optional[str] = Field(None, max_length=500)
    language: InvoiceLanguage = Field(default=InvoiceLanguage.ENGLISH)
    currency: InvoiceCurrency = Field(default=InvoiceCurrency.USD)
    items: List[InvoiceItemCreate] = Field(..., min_length=1)
    tax_rate: float = Field(default=0, ge=0, le=100, description="Tax rate percentage (0-100)")
    discount_rate: float = Field(default=0, ge=0, le=100, description="Discount rate percentage (0-100)")
    due_date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=2000)
    
    @field_validator('items')
    @classmethod
    def validate_items(cls, v):
        """Ensure at least one item is provided"""
        if not v or len(v) == 0:
            raise ValueError('At least one item is required')
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "client_name": "ACME Corporation",
                "client_email": "billing@acme.com",
                "client_phone": "+1234567890",
                "client_address": "123 Business Ave, New York, USA",
                "language": "ar",
                "currency": "MAD",
                "items": [
                    {
                        "name": "تطوير موقع ويب",
                        "description": "موقع تجارة إلكترونية كامل",
                        "quantity": 1,
                        "price": 15000.00
                    }
                ],
                "tax_rate": 20.0,
                "discount_rate": 10.0,
                "due_date": "2025-11-10T00:00:00",
                "notes": "شكراً لتعاملكم معنا"
            }
        }
    }


class InvoiceUpdate(BaseModel):
    """Schema for updating an invoice"""
    status: Optional[InvoiceStatus] = None
    notes: Optional[str] = Field(None, max_length=2000)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "paid",
                "notes": "Payment received via bank transfer"
            }
        }
    }


class InvoiceResponse(BaseModel):
    """Schema for invoice response"""
    id: int
    invoice_number: str
    user_id: int
    client_name: str
    client_email: str
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    language: str
    currency: str
    subtotal: float
    tax_rate: float
    tax_amount: float
    discount_rate: float
    discount_amount: float
    total: float
    status: str
    due_date: Optional[datetime] = None
    notes: Optional[str] = None
    pdf_path: Optional[str] = None
    qr_code_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[InvoiceItemResponse] = []
    
    model_config = {"from_attributes": True}  # ✅ Fixed: was orm_mode in v1


class InvoiceListResponse(BaseModel):
    """Schema for paginated invoice list"""
    total: int
    page: int
    page_size: int
    invoices: List[InvoiceResponse]


class EmailInvoice(BaseModel):
    """Schema for sending invoice via email"""
    message: Optional[str] = Field(
        None, 
        max_length=1000,
        description="Custom message to include in email"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Thank you for your business! Please find your invoice attached."
            }
        }
    }


# ==========================================
# Statistics Schemas
# ==========================================

class UserStats(BaseModel):
    """Schema for user statistics"""
    total_invoices: int
    invoices_by_status: dict
    total_revenue: float
    revenue_by_currency: dict
    pending_amount: float
    paid_amount: float


# ==========================================
# Error Schemas
# ==========================================

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str
    error_type: Optional[str] = None
    path: Optional[str] = None
