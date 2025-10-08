"""
QR Code Generation Service
"""

import qrcode
import os
from pathlib import Path
from ..config import settings


def generate_qr_code(data: str, filename: str) -> str:
    """
    Generate QR code image
    
    Args:
        data: Data to encode (usually payment link)
        filename: Output filename (without extension)
        
    Returns:
        Path to generated QR code image
    """
    # Ensure QR directory exists
    qr_dir = Path(settings.QR_DIR)
    qr_dir.mkdir(parents=True, exist_ok=True)
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    # Generate image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save image
    output_path = qr_dir / f"{filename}.png"
    img.save(str(output_path))
    
    return str(output_path)


def generate_invoice_qr(invoice_number: str, payment_link: str, total: float, currency: str) -> str:
    """
    Generate QR code for invoice with payment information
    
    Args:
        invoice_number: Invoice number for filename
        payment_link: Payment URL to encode
        total: Invoice total amount
        currency: Currency code
        
    Returns:
        Path to generated QR code
    """
    # Create QR data with payment info
    qr_data = f"{payment_link}?invoice={invoice_number}&amount={total}&currency={currency}"
    
    filename = f"invoice_{invoice_number}_qr"
    return generate_qr_code(qr_data, filename)