"""
Helper Utilities
Common utility functions used across the application
"""

import random
import string
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from decimal import Decimal, ROUND_HALF_UP


def generate_invoice_number(prefix: str = "INV", user_id: Optional[int] = None) -> str:
    """
    Generate unique invoice number
    Format: INV-YYYYMMDD-XXXX or INV-YYYYMMDD-UID-XXXX
    """
    date_str = datetime.now().strftime("%Y%m%d")
    random_str = ''.join(random.choices(string.digits, k=4))

    if user_id:
        return f"{prefix}-{date_str}-{user_id}-{random_str}"
    return f"{prefix}-{date_str}-{random_str}"


def format_currency(amount: float, currency: str, include_symbol: bool = True) -> str:
    """
    Format amount with currency symbol
    """
    symbols = {
        "MAD": "DH",
        "USD": "$",
        "EUR": "€",
        "SAR": "SAR",
        "AED": "AED",
        "GBP": "£",
        "JPY": "¥"
    }

    # Format with thousand separators
    formatted_amount = f"{amount:,.2f}"

    if include_symbol:
        symbol = symbols.get(currency, currency)
        # Dollar and Euro before amount, others after
        if currency in ["USD", "EUR", "GBP"]:
            return f"{symbol}{formatted_amount}"
        return f"{formatted_amount} {symbol}"

    return f"{formatted_amount} {currency}"


def validate_email_rate_limit(user_id: int, db_session, hours: int = 1, limit: int = None) -> Dict[str, Any]:
    """
    Check if user has exceeded email rate limit
    """
    from ..models.invoice import Invoice
    from ..config import settings

    if limit is None:
        limit = settings.EMAIL_RATE_LIMIT

    # Calculate time threshold
    time_threshold = datetime.utcnow() - timedelta(hours=hours)

    # Count emails sent in time window
    count = db_session.query(Invoice).filter(
        Invoice.user_id == user_id,
        Invoice.is_sent_email == True,
        Invoice.email_sent_at >= time_threshold
    ).count()

    remaining = max(0, limit - count)
    allowed = count < limit

    return {
        "allowed": allowed,
        "remaining": remaining,
        "limit": limit,
        "count": count,
        "reset_in_minutes": 60 * hours
    }


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Remove unsafe characters from filename
    """
    # Define safe characters
    safe_chars = string.ascii_letters + string.digits + "-_."

    # Replace unsafe characters with underscore
    sanitized = ''.join(c if c in safe_chars else '_' for c in filename)

    # Remove multiple consecutive underscores
    sanitized = re.sub(r'_+', '_', sanitized)

    # Trim to max length
    if len(sanitized) > max_length:
        name, ext = sanitized.rsplit(
            '.', 1) if '.' in sanitized else (sanitized, '')
        max_name_length = max_length - len(ext) - 1
        sanitized = f"{name[:max_name_length]}.{ext}" if ext else name[:max_length]

    return sanitized


def calculate_invoice_totals(
    items: list,
    tax_rate: float = 0.0,
    discount_rate: float = 0.0
) -> Dict[str, float]:
    """
    Calculate invoice totals with tax and discount
    """
    # Calculate subtotal
    subtotal = sum(
        Decimal(str(item.get('quantity', 0))) *
        Decimal(str(item.get('price', 0)))
        for item in items
    )

    # Calculate discount
    discount_amount = (subtotal * Decimal(str(discount_rate)) / Decimal('100')).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )

    # Subtotal after discount
    subtotal_after_discount = subtotal - discount_amount

    # Calculate tax on discounted amount
    tax_amount = (subtotal_after_discount * Decimal(str(tax_rate)) / Decimal('100')).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )

    # Calculate total
    total = subtotal_after_discount + tax_amount

    return {
        "subtotal": float(subtotal),
        "discount_amount": float(discount_amount),
        "tax_amount": float(tax_amount),
        "total": float(total)
    }


def format_date(
    date: datetime,
    format_type: str = "short",
    language: str = "en"
) -> str:
    """
    Format date according to language and format type
    """
    if format_type == "iso":
        return date.strftime("%Y-%m-%d")

    if language == "ar":
        # Arabic format: DD/MM/YYYY
        if format_type == "short":
            return date.strftime("%d/%m/%Y")
        else:  # long
            months_ar = [
                "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
                "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
            ]
            return f"{date.day} {months_ar[date.month - 1]} {date.year}"
    else:  # English
        if format_type == "short":
            return date.strftime("%m/%d/%Y")
        else:  # long
            return date.strftime("%B %d, %Y")


def generate_random_string(length: int = 10, include_numbers: bool = True) -> str:
    """
    Generate random string
    """
    chars = string.ascii_letters
    if include_numbers:
        chars += string.digits
    return ''.join(random.choices(chars, k=length))
