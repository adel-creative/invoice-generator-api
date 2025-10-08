"""
Invoice API Endpoints - Part 2
Additional invoice operations: retrieve, list, download, send email
"""

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