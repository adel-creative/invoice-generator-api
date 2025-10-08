"""
PDF Generation Service
Creates professional invoices using WeasyPrint and Jinja2
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from datetime import datetime
from typing import List, Dict, Optional
from ..config import settings


class PDFGenerator:
    """PDF Generator for invoices"""
    
    def __init__(self):
        # Setup Jinja2 environment
        template_dir = Path(__file__).parent.parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))
        
        # Ensure output directory exists
        self.output_dir = Path(settings.UPLOAD_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def calculate_totals(
        self,
        items: List[Dict],
        tax_rate: float = 0.0,
        discount_rate: float = 0.0
    ) -> Dict[str, float]:
        """
        Calculate invoice totals
        
        Args:
            items: List of invoice items
            tax_rate: Tax percentage (0-100)
            discount_rate: Discount percentage (0-100)
            
        Returns:
            Dictionary with subtotal, tax, discount, and total
        """
        subtotal = sum(item.get("total", 0) for item in items)
        
        discount_amount = round(subtotal * (discount_rate / 100), 2)
        subtotal_after_discount = subtotal - discount_amount
        
        tax_amount = round(subtotal_after_discount * (tax_rate / 100), 2)
        
        total = round(subtotal_after_discount + tax_amount, 2)
        
        return {
            "subtotal": subtotal,
            "discount_amount": discount_amount,
            "tax_amount": tax_amount,
            "total": total
        }
    
    def format_date(self, date: datetime, language: str = "en") -> str:
        """Format date based on language"""
        if language == "ar":
            return date.strftime("%d/%m/%Y")
        return date.strftime("%B %d, %Y")
    
    def generate_invoice_pdf(
    self,
    # المعاملات المطلوبة أولاً
    invoice_number: str,
    language: str,
    seller_name: str,
    seller_email: str,
    client_name: str,
    client_email: str,
    items: List[Dict],
    currency: str,
    issue_date: datetime,
    # ثم المعاملات الاختيارية
    seller_phone: Optional[str] = None,
    seller_address: Optional[str] = None,
    client_phone: Optional[str] = None,
    client_address: Optional[str] = None,
    tax_rate: float = 0.0,
    discount_rate: float = 0.0,
    due_date: Optional[datetime] = None,
    notes: Optional[str] = None,
    qr_code_path: Optional[str] = None,
    payment_link: Optional[str] = None
) -> str:
        """
        Generate invoice PDF
        
        Returns:
            Path to generated PDF file
        """
        # Calculate totals
        totals = self.calculate_totals(items, tax_rate, discount_rate)
        
        # Select template based on language
        template_name = f"invoice_{language}.html"
        template = self.env.get_template(template_name)
        
        # Prepare template context
        context = {
            # Invoice info
            "invoice_number": invoice_number,
            "issue_date": self.format_date(issue_date, language),
            "due_date": self.format_date(due_date, language) if due_date else None,
            
            # Seller
            "seller_name": seller_name,
            "seller_email": seller_email,
            "seller_phone": seller_phone,
            "seller_address": seller_address,
            
            # Client
            "client_name": client_name,
            "client_email": client_email,
            "client_phone": client_phone,
            "client_address": client_address,
            
            # Items
            "items": items,
            
            # Financial
            "currency": currency,
            "subtotal": totals["subtotal"],
            "tax_rate": tax_rate,
            "tax_amount": totals["tax_amount"],
            "discount_rate": discount_rate,
            "discount_amount": totals["discount_amount"],
            "total": totals["total"],
            
            # Additional
            "notes": notes,
            "qr_code_path": qr_code_path,
            "payment_link": payment_link,
            
            # Current date
            "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        
        # Render HTML
        html_content = template.render(context)
        
        # Generate PDF
        output_filename = f"invoice_{invoice_number}.pdf"
        output_path = self.output_dir / output_filename
        
        HTML(string=html_content, base_url=str(Path.cwd())).write_pdf(
            str(output_path)
        )
        
        return str(output_path)


# Global instance
pdf_generator = PDFGenerator()