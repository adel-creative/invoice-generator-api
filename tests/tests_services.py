"""
Service Tests
"""

import pytest
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    generate_payment_link
)
from app.services.qr_service import generate_qr_code
from app.utils.helpers import (
    generate_invoice_number,
    format_currency,
    sanitize_filename
)


def test_password_hashing():
    """Test password hashing and verification"""
    password = "mysecurepassword"
    hashed = hash_password(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_jwt_token_creation():
    """Test JWT token creation and decoding"""
    data = {"sub": "testuser", "user_id": 1}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded.username == "testuser"
    assert decoded.user_id == 1


def test_invalid_jwt_token():
    """Test decoding invalid JWT token"""
    invalid_token = "invalid.token.here"
    decoded = decode_access_token(invalid_token)
    
    assert decoded is None


def test_payment_link_generation():
    """Test payment link generation"""
    link = generate_payment_link(1, "testuser")
    
    assert "testuser" in link
    assert "1" in link
    assert link.startswith("http")


def test_qr_code_generation():
    """Test QR code generation"""
    import os
    
    data = "https://example.com/payment"
    filename = "test_qr"
    
    qr_path = generate_qr_code(data, filename)
    
    assert qr_path is not None
    assert os.path.exists(qr_path)
    assert filename in qr_path
    
    # Cleanup
    if os.path.exists(qr_path):
        os.remove(qr_path)


def test_invoice_number_generation():
    """Test invoice number generation"""
    invoice_num = generate_invoice_number()
    
    assert invoice_num.startswith("INV-")
    assert len(invoice_num) > 10
    
    # Generate another and ensure it's different
    invoice_num2 = generate_invoice_number()
    assert invoice_num != invoice_num2


def test_currency_formatting():
    """Test currency formatting"""
    assert format_currency(100, "USD") == "100.00 $"
    assert format_currency(50.5, "MAD") == "50.50 DH"
    assert format_currency(200.99, "EUR") == "200.99 €"


def test_filename_sanitization():
    """Test filename sanitization"""
    assert sanitize_filename("test file.pdf") == "test_file.pdf"
    assert sanitize_filename("invoice#123@.pdf") == "invoice_123_.pdf"
    assert sanitize_filename("../../../etc/passwd") == ".._.._.._etc_passwd"