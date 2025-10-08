"""
Invoice API Endpoints
Handles invoice creation, retrieval, PDF generation, and email sending
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..models.user import User
from ..models.invoice import Invoice
from ..schemas.invoice import (
    InvoiceCreate,
    InvoiceResponse,
    InvoiceListResponse,
    InvoiceUpdate,
    EmailInvoice
)
from ..utils.dependencies import get_current_user
from ..utils.helpers import generate_invoice_number, validate_email_rate_limit
from ..services.pdf_service import pdf_generator
from ..services.qr_service import generate_invoice_qr
from ..services.email_service import send_invoice_email

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/generate", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    invoice_data: InvoiceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create and generate new invoice
    
    Creates invoice, generates PDF with QR code, and saves to database.
    
    **Request Body:**
    - **client_name**: Client's full name (required)
    - **client_email**: Client's email address (required)
    - **client_phone**: Client's phone number (optional)
    - **client_address**: Client's address (optional)
    - **language**: Invoice language - "ar" or "en" (default: "ar")
    - **currency**: Currency code - MAD, USD, EUR, SAR, AED (default: "MAD")
    - **items**: List of invoice items (min 1 item required)
      - name: Item name
      - description: Item description (optional)
      - quantity: Quantity (must be > 0)
      - price: Unit price (must be >= 0)
    - **tax_rate**: Tax percentage 0-100 (default: 0)
    - **discount_rate**: Discount percentage 0-100 (default: 0)
    - **due_date**: Payment due date (optional)
    - **notes**: Additional notes (optional)
    
    **Returns:**
    Complete invoice object with PDF path and QR code
    """
    # Generate unique invoice number
    invoice_number = generate_invoice_number()
    
    # Prepare items for database (convert Pydantic to dict)
    items_list = []
    for item in invoice_data.items:
        items_list.append({
            "name": item.name,
            "description": item.description,
            "quantity": item.quantity,
            "price": item.price,
            "total": item.total
        })
    
    # Calculate totals
    subtotal = sum(item["total"] for item in items_list)
    discount_amount = round(subtotal * (invoice_data.discount_rate / 100), 2)
    subtotal_after_discount = subtotal - discount_amount
    tax_amount = round(subtotal_after_discount * (invoice_data.tax_rate / 100), 2)
    total = round(subtotal_after_discount + tax_amount, 2)
    
    # Generate payment link (user's unique link + invoice reference)
    payment_link = f"{current_user.payment_link}?invoice={invoice_number}"
    
    # Generate QR code
    qr_code_path = generate_invoice_qr(
        invoice_number=invoice_number,
        payment_link=payment_link,
        total=total,
        currency=invoice_data.currency
    )
    
    # Generate PDF
    pdf_path = pdf_generator.generate_invoice_pdf(
        invoice_number=invoice_number,
        language=invoice_data.language,
        # Seller info (from current user)
        seller_name=current_user.company_name or current_user.full_name or current_user.username,
        seller_email=current_user.email,
        seller_phone=current_user.phone,
        seller_address=current_user.address,
        # Client info
        client_name=invoice_data.client_name,
        client_email=invoice_data.client_email,
        client_phone=invoice_data.client_phone,
        client_address=invoice_data.client_address,
        # Items
        items=items_list,
        # Financial
        currency=invoice_data.currency,
        tax_rate=invoice_data.tax_rate,
        discount_rate=invoice_data.discount_rate,
        # Dates
        issue_date=datetime.now(),
        due_date=invoice_data.due_date,
        # Additional
        notes=invoice_data.notes,
        qr_code_path=qr_code_path,
        payment_link=payment_link,
    )
    
    # Create invoice record
    new_invoice = Invoice(
        invoice_number=invoice_number,
        user_id=current_user.id,
        # Client
        client_name=invoice_data.client_name,
        client_email=invoice_data.client_email,
        client_phone=invoice_data.client_phone,
        client_address=invoice_data.client_address,
        # Settings
        language=invoice_data.language,
        currency=invoice_data.currency,
        # Items
        items=items_list,
        # Financial
        subtotal=subtotal,
        tax_rate=invoice_data.tax_rate,
        tax_amount=tax_amount,
        discount_rate=invoice_data.discount_rate,
        discount_amount=discount_amount,
        total=total,
        # Dates
        issue_date=datetime.now(),
        due_date=invoice_data.due_date,
        # Files
        pdf_path=pdf_path,
        qr_code_path=qr_code_path,
        payment_link=payment_link,
        # Additional
        notes=invoice_data.notes,
        status="draft"
    )
    
    # Save to database
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    
    return new_invoice
    # Add these endpoints to the same router in invoices.py


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get invoice by ID
    
    Returns complete invoice details including PDF path and QR code.
    Users can only access their own invoices.
    """
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.user_id == current_user.id
    ).first()
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    return invoice


@router.get("/", response_model=InvoiceListResponse)
async def list_invoices(
    page: int = 1,
    page_size: int = 10,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all user's invoices with pagination
    
    **Query Parameters:**
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 100)
    - **status**: Filter by status - draft, sent, paid, cancelled (optional)
    
    **Returns:**
    - List of invoices
    - Total count
    - Current page
    - Page size
    """
    # Validate pagination
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 10
    
    # Build query
    query = db.query(Invoice).filter(Invoice.user_id == current_user.id)
    
    # Filter by status if provided
    if status:
        query = query.filter(Invoice.status == status)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    invoices = query.order_by(Invoice.created_at.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    return {
        "invoices": invoices,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{invoice_id}/download")
async def download_invoice(
    invoice_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Download invoice PDF
    
    Returns the PDF file for download. File is named "invoice_{number}.pdf"
    """
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.user_id == current_user.id
    ).first()
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    if not invoice.pdf_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF not generated yet"
        )
    
    return FileResponse(
        path=invoice.pdf_path,
        filename=f"invoice_{invoice.invoice_number}.pdf",
        media_type="application/pdf"
    )


@router.post("/{invoice_id}/send-email", status_code=status.HTTP_200_OK)
async def send_invoice_by_email(
    invoice_id: int,
    email_data: EmailInvoice,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send invoice via email
    
    Sends the invoice PDF to the client's email address.
    Rate limited to 5 emails per hour per user.
    
    **Request Body:**
    - **to_email**: Override recipient email (optional, uses client_email by default)
    - **subject**: Custom email subject (optional)
    - **message**: Custom message to include (optional)
    
    **Rate Limit:** 5 emails per hour per user
    """
    # Check rate limit
    if not validate_email_rate_limit(current_user.id, db):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Email rate limit exceeded. Maximum 5 emails per hour."
        )
    
    # Get invoice
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.user_id == current_user.id
    ).first()
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    if not invoice.pdf_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF not generated"
        )
    
    # Determine recipient email
    recipient_email = email_data.to_email or invoice.client_email
    
    # Send email in background
    background_tasks.add_task(
        send_invoice_email,
        to_email=recipient_email,
        client_name=invoice.client_name,
        invoice_number=invoice.invoice_number,
        total=invoice.total,
        currency=invoice.currency,
        pdf_path=invoice.pdf_path,
        payment_link=invoice.payment_link,
        custom_message=email_data.message
    )
    
    # Update invoice status
    invoice.is_sent_email = True
    invoice.email_sent_at = datetime.now()
    if invoice.status == "draft":
        invoice.status = "sent"
    
    db.commit()
    
    return {
        "message": "Email is being sent",
        "recipient": recipient_email,
        "invoice_number": invoice.invoice_number
    }


@router.put("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: int,
    update_data: InvoiceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update invoice details
    
    Allows updating client information, status, notes, and due date.
    Cannot update items or financial details after creation.
    """
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.user_id == current_user.id
    ).first()
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    # Update fields if provided
    if update_data.client_name is not None:
        invoice.client_name = update_data.client_name
    if update_data.client_email is not None:
        invoice.client_email = update_data.client_email
    if update_data.client_phone is not None:
        invoice.client_phone = update_data.client_phone
    if update_data.client_address is not None:
        invoice.client_address = update_data.client_address
    if update_data.status is not None:
        invoice.status = update_data.status
    if update_data.notes is not None:
        invoice.notes = update_data.notes
    if update_data.due_date is not None:
        invoice.due_date = update_data.due_date
    
    db.commit()
    db.refresh(invoice)
    
    return invoice


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice(
    invoice_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete invoice
    
    Permanently deletes the invoice and associated files.
    """
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.user_id == current_user.id
    ).first()
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    # Delete files
    from pathlib import Path
    if invoice.pdf_path and Path(invoice.pdf_path).exists():
        Path(invoice.pdf_path).unlink()
    if invoice.qr_code_path and Path(invoice.qr_code_path).exists():
        Path(invoice.qr_code_path).unlink()
    
    # Delete from database
    db.delete(invoice)
    db.commit()
    
    return None
