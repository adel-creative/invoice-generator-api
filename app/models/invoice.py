"""
Invoice Database Model
Stores all invoice information with relationships to users
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List, Dict, Any
from ..database import Base


class Invoice(Base):
    """
    Invoice model representing a complete invoice
    
    Attributes:
        id: Primary key
        invoice_number: Unique invoice identifier
        user_id: Foreign key to user who created invoice
        client_*: Client information
        language: Invoice language (ar/en)
        currency: Currency code
        items: JSON array of invoice items
        subtotal: Sum before tax and discount
        tax_rate: Tax percentage
        tax_amount: Calculated tax
        discount_rate: Discount percentage
        discount_amount: Calculated discount
        total: Final amount to pay
        issue_date: When invoice was created
        due_date: Payment deadline
        pdf_path: Path to generated PDF
        qr_code_path: Path to QR code image
        payment_link: Unique payment URL
        status: Invoice status (draft/sent/paid/cancelled)
        is_sent_email: Whether email was sent
        email_sent_at: When email was sent
        notes: Additional notes
    """
    __tablename__ = "invoices"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), unique=True, index=True, nullable=False)
    
    # Owner
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Client Information
    client_name = Column(String(200), nullable=False)
    client_email = Column(String(200), nullable=False, index=True)
    client_phone = Column(String(50), nullable=True)
    client_address = Column(Text, nullable=True)
    
    # Invoice Settings
    language = Column(String(5), default="ar", nullable=False)  # ar or en
    currency = Column(String(10), default="MAD", nullable=False)
    
    # Items (stored as JSON array)
    # Format: [{"name": "Item", "description": "...", "quantity": 1, "price": 100, "total": 100}]
    items = Column(JSON, nullable=False)
    
    # Financial Calculations
    subtotal = Column(Float, nullable=False, default=0.0)
    tax_rate = Column(Float, default=0.0)  # Percentage (0-100)
    tax_amount = Column(Float, default=0.0)
    discount_rate = Column(Float, default=0.0)  # Percentage (0-100)
    discount_amount = Column(Float, default=0.0)
    total = Column(Float, nullable=False, default=0.0, index=True)
    
    # Important Dates
    issue_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    due_date = Column(DateTime, nullable=True, index=True)
    
    # Generated Files
    pdf_path = Column(String(500), nullable=True)
    qr_code_path = Column(String(500), nullable=True)
    payment_link = Column(String(500), nullable=True)
    
    # Status Tracking
    status = Column(
        String(20), 
        default="draft", 
        nullable=False,
        index=True
    )  # draft, sent, paid, cancelled, overdue
    is_sent_email = Column(Boolean, default=False, nullable=False)
    email_sent_at = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    # Additional Information
    notes = Column(Text, nullable=True)
    internal_notes = Column(Text, nullable=True)  # Not shown to client
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )
    
    # Relationships
    owner = relationship("User", back_populates="invoices")
    
    def __repr__(self) -> str:
        return f"<Invoice {self.invoice_number} - {self.total} {self.currency}>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert invoice to dictionary"""
        return {
            "id": self.id,
            "invoice_number": self.invoice_number,
            "client_name": self.client_name,
            "total": self.total,
            "currency": self.currency,
            "status": self.status,
            "issue_date": self.issue_date.isoformat() if self.issue_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
        }
    
    @property
    def is_overdue(self) -> bool:
        """Check if invoice is overdue"""
        if self.due_date and self.status not in ["paid", "cancelled"]:
            return datetime.utcnow() > self.due_date
        return False
    
    @property
    def days_until_due(self) -> int:
        """Calculate days until due date"""
        if self.due_date:
            delta = self.due_date - datetime.utcnow()
            return delta.days
        return 0
    
    # Client Information
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    client_phone = Column(String, nullable=True)
    client_address = Column(Text, nullable=True)
    
    # Invoice Details
    language = Column(String, default="ar")  # ar or en
    currency = Column(String, default="MAD")
    
    # Items (stored as JSON)
    items = Column(JSON, nullable=False)  # List of {name, quantity, price, total}
    
    # Financial
    subtotal = Column(Float, nullable=False)
    tax_rate = Column(Float, default=0.0)  # Percentage
    tax_amount = Column(Float, default=0.0)
    discount_rate = Column(Float, default=0.0)  # Percentage
    discount_amount = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    
    # Dates
    issue_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    
    # Files & Links
    pdf_path = Column(String, nullable=True)
    qr_code_path = Column(String, nullable=True)
    payment_link = Column(String, nullable=True)
    
    # Status
    status = Column(String, default="draft")  # draft, sent, paid, cancelled
    is_sent_email = Column(Boolean, default=False)
    email_sent_at = Column(DateTime, nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="invoices")
    
    def __repr__(self):
        return f"<Invoice {self.invoice_number}>"