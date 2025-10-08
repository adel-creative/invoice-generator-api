"""
Invoice Schemas
Pydantic models for invoice requests/responses with full validation
"""

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class LanguageEnum(str, Enum):
    """Supported languages for invoices"""
    ARABIC = "ar"
    ENGLISH = "en"


class CurrencyEnum(str, Enum):
    """Supported currencies"""
    MAD = "MAD"  # Moroccan Dirham
    USD = "USD"  # US Dollar
    EUR = "EUR"  # Euro
    SAR = "SAR"  # Saudi Riyal
    AED = "AED"  # UAE Dirham
    GBP = "GBP"  # British Pound
    EGP = "EGP"  # Egyptian Pound


class InvoiceStatusEnum(str, Enum):
    """Invoice status options"""
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"


class InvoiceItem(BaseModel):
    """Single item in invoice with validation"""
    name: str = Field(..., min_length=1, max_length=200, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    quantity: float = Field(..., gt=0, description="Quantity (must be > 0)")
    price: float = Field(..., ge=0, description="Unit price (must be >= 0)")
    
    @property
    def total(self) -> float:
        """Calculate item total"""
        return round(self.quantity * self.price, 2)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Web Development",
                "description": "E-commerce website development",
                "quantity": 1,
                "price": 15000
            }
        }


class InvoiceCreate(BaseModel):
    """Schema for creating new invoice with comprehensive validation"""
    
    # Client Information (Required)
    client_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Client's full name or company name"
    )
    client_email: EmailStr = Field(..., description="Client's email address")
    client_phone: Optional[str] = Field(
        None,
        max_length=50,
        description="Client's phone number"
    )
    client_address: Optional[str] = Field(
        None,
        max_length=500,
        description="Client's address"
    )
    client_tax_id: Optional[str] = Field(
        None,
        max_length=50,
        description="Client's tax/VAT ID"
    )
    
    # Invoice Settings
    language: LanguageEnum = Field(
        default=LanguageEnum.ARABIC,
        description="Invoice language (ar or en)"
    )
    currency: CurrencyEnum = Field(
        default=CurrencyEnum.MAD,
        description="Currency code"
    )
    
    # Items (At least 1 required)
    items: List[InvoiceItem] = Field(
        ...,
        min_length=1,
        description="List of invoice items (minimum 1)"
    )
    
    # Financial Settings
    tax_rate: float = Field(
        default=0.0,
        ge=0,
        le=100,
        description="Tax percentage (0-100)"
    )
    discount_rate: float = Field(
        default=0.0,
        ge=0,
        le=100,
        description="Discount percentage (0-100)"
    )
    
    # Dates
    issue_date: Optional[datetime] = Field(
        default=None,
        description="Issue date (defaults to now)"
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Payment due date"
    )
    
    # Additional Information
    notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="Notes visible to client"
    )
    internal_notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="Internal notes (not shown to client)"
    )
    
    @field_validator('items')
    @classmethod
    def validate_items(cls, v):
        """Validate that at least one item is provided"""
        if not v or len(v) == 0:
            raise ValueError('At least one item is required')
        return v
    
    @field_validator('client_phone')
    @classmethod
    def validate_phone(cls, v):
        """Basic phone validation"""
        if v:
            # Remove spaces and common separators
            cleaned = v.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            if not cleaned.replace("+", "").isdigit():
                raise ValueError('Phone number must contain only digits, spaces, dashes, and + sign')
        return v
    
    @model_validator(mode='after')
    def validate_dates(self):
        """Validate that due date is after issue date"""
        if self.issue_date and self.due_date:
            if self.due_date < self.issue_date:
                raise ValueError('Due date must be after issue date')
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "client_name": "ACME Corporation",
                "client_email": "billing@acme.com",
                "client_phone": "+212 600 123 456",
                "client_address": "123 Business Ave, Casablanca, Morocco",
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
                        "description": "3-month SEO package",
                        "quantity": 3,
                        "price": 2000
                    }
                ],
                "tax_rate": 20,
                "discount_rate": 10,
                "due_date": "2025-11-01T00:00:00",
                "notes": "Payment due within 30 days"
            }
        }


class InvoiceUpdate(BaseModel):
    """Schema for updating invoice (partial update)"""
    client_name: Optional[str] = Field(None, min_length=1, max_length=200)
    client_email: Optional[EmailStr] = None
    client_phone: Optional[str] = Field(None, max_length=50)
    client_address: Optional[str] = Field(None, max_length=500)
    status: Optional[InvoiceStatusEnum] = None
    notes: Optional[str] = Field(None, max_length=1000)
    internal_notes: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "paid",
                "notes": "Payment received via bank transfer"
            }
        }


class InvoiceResponse(BaseModel):
    """Schema for invoice response with all details"""
    id: int
    invoice_number: str
    user_id: int
    
    # Client Information
    client_name: str
    client_email: str
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    
    # Settings
    language: str
    currency: str
    
    # Items
    items: List[dict]
    
    # Financial
    subtotal: float
    tax_rate: float
    tax_amount: float
    discount_rate: float
    discount_amount: float
    total: float
    
    # Dates
    issue_date: datetime
    due_date: Optional[datetime] = None
    
    # Files & Links
    pdf_path: Optional[str] = None
    qr_code_path: Optional[str] = None
    payment_link: Optional[str] = None
    
    # Status
    status: str
    is_sent_email: bool
    email_sent_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    
    # Notes
    notes: Optional[str] = None
    internal_notes: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "invoice_number": "INV-20251002-1234",
                "user_id": 1,
                "client_name": "ACME Corporation",
                "client_email": "billing@acme.com",
                "client_phone": "+212 600 123 456",
                "client_address": "123 Business Avenue, Casablanca, Morocco",
                "language": "ar",
                "currency": "MAD",
                "items": [
                    {
                        "name": "تطوير موقع ويب",
                        "description": "موقع تجارة إلكترونية متكامل",
                        "quantity": 1,
                        "price": 15000,
                        "total": 15000
                    },
                    {
                        "name": "استضافة سنوية",
                        "description": "استضافة VPS مع SSL",
                        "quantity": 1,
                        "price": 1200,
                        "total": 1200
                    }
                ],
                "subtotal": 16200,
                "tax_rate": 20,
                "tax_amount": 2916,
                "discount_rate": 10,
                "discount_amount": 1620,
                "total": 17496,
                "issue_date": "2025-10-02T10:30:00",
                "due_date": "2025-11-01T00:00:00",
                "pdf_path": "./static/invoices/invoice_INV-20251002-1234.pdf",
                "qr_code_path": "./static/qr_codes/invoice_INV-20251002-1234_qr.png",
                "payment_link": "https://pay.yourdomain.com/pay/johndoe-1?invoice=INV-20251002-1234",
                "status": "draft",
                "is_sent_email": False,
                "email_sent_at": None,
                "paid_at": None,
                "notes": "الدفع خلال 30 يوماً من تاريخ الفاتورة. طرق الدفع المقبولة: تحويل بنكي، نقداً",
                "internal_notes": "عميل VIP - أولوية في الدعم",
                "created_at": "2025-10-02T10:30:00",
                "updated_at": "2025-10-02T10:30:00"
            }
        }


class InvoiceListResponse(BaseModel):
    """Schema for paginated invoice list"""
    invoices: List[InvoiceResponse]
    total: int = Field(..., description="Total number of invoices")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    
    @staticmethod
    def calculate_total_pages(total: int, page_size: int) -> int:
        """Calculate total pages"""
        return (total + page_size - 1) // page_size


class EmailInvoice(BaseModel):
    """Schema for sending invoice via email"""
    to_email: Optional[EmailStr] = Field(
        None,
        description="Override recipient email (uses client_email if not provided)"
    )
    subject: Optional[str] = Field(
        None,
        max_length=200,
        description="Custom email subject"
    )
    message: Optional[str] = Field(
        None,
        max_length=1000,
        description="Custom message to include in email"
    )
    cc: Optional[List[EmailStr]] = Field(
        None,
        max_length=5,
        description="CC recipients (max 5)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Thank you for your business! Payment is due within 30 days."
            }
        }


class InvoiceStats(BaseModel):
    """Schema for invoice statistics"""
    total_invoices: int
    total_amount: float
    paid_amount: float
    pending_amount: float
    overdue_amount: float
    status_breakdown: dict
    currency_breakdown: dict
    recent_invoices: List[InvoiceResponse]


class BulkInvoiceCreate(BaseModel):
    """Schema for creating multiple invoices at once"""
    invoices: List[InvoiceCreate] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="List of invoices to create (max 50)"
    )
    send_emails: bool = Field(
        default=False,
        description="Whether to send emails for all invoices"
    )


class InvoiceUpdate(BaseModel):
    """Schema for updating invoice"""
    client_name: Optional[str] = None
    client_email: Optional[EmailStr] = None
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    status: Optional[InvoiceStatusEnum] = None
    notes: Optional[str] = None
    due_date: Optional[datetime] = None


class InvoiceResponse(BaseModel):
    """Schema for invoice response"""
    id: int
    invoice_number: str
    user_id: int
    
    # Client
    client_name: str
    client_email: str
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    
    # Settings
    language: str
    currency: str
    
    # Items
    items: List[dict]
    
    # Financial
    subtotal: float
    tax_rate: float
    tax_amount: float
    discount_rate: float
    discount_amount: float
    total: float
    
    # Dates
    issue_date: datetime
    due_date: Optional[datetime] = None
    
    # Files
    pdf_path: Optional[str] = None
    qr_code_path: Optional[str] = None
    payment_link: Optional[str] = None
    
    # Status
    status: str
    is_sent_email: bool
    email_sent_at: Optional[datetime] = None
    
    # Notes
    notes: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InvoiceListResponse(BaseModel):
    """Schema for listing invoices"""
    invoices: List[InvoiceResponse]
    total: int
    page: int
    page_size: int


class EmailInvoice(BaseModel):
    """Schema for sending invoice via email"""
    to_email: Optional[EmailStr] = None  # If None, use client_email
    subject: Optional[str] = None
    message: Optional[str] = None