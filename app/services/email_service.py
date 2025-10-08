"""
Email Service
Handles sending emails with attachments using aiosmtplib
Supports HTML emails with professional templates
"""

import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Optional, List
import logging
from ..config import settings

# Setup logging
logger = logging.getLogger(__name__)


async def send_email(
    to_email: str,
    subject: str,
    body: str,
    attachments: Optional[List[str]] = None,
    is_html: bool = True,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None
) -> bool:
    """
    Send email with optional attachments
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        body: Email body content (HTML or plain text)
        attachments: List of file paths to attach
        is_html: Whether body is HTML (default: True)
        cc: Optional CC recipients
        bcc: Optional BCC recipients
        
    Returns:
        True if sent successfully, False otherwise
        
    Raises:
        Exception: If email sending fails critically
    """
    # Validate email format
    if not to_email or "@" not in to_email:
        logger.error(f"Invalid email address: {to_email}")
        return False
    
    try:
        # Create message container
        message = MIMEMultipart("mixed")
        message["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>"
        message["To"] = to_email
        message["Subject"] = subject
        
        # Add CC and BCC if provided
        if cc:
            message["Cc"] = ", ".join(cc)
        if bcc:
            message["Bcc"] = ", ".join(bcc)
        
        # Attach body
        mime_type = "html" if is_html else "plain"
        body_part = MIMEText(body, mime_type, "utf-8")
        message.attach(body_part)
        
        # Attach files if provided
        if attachments:
            for file_path in attachments:
                path = Path(file_path)
                if not path.exists():
                    logger.warning(f"Attachment not found: {file_path}")
                    continue
                
                # Check file size (e.g., max 10MB)
                file_size_mb = path.stat().st_size / (1024 * 1024)
                if file_size_mb > 10:
                    logger.warning(f"Attachment too large ({file_size_mb:.2f}MB): {file_path}")
                    continue
                
                try:
                    with open(file_path, "rb") as f:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        
                        # Add header with filename
                        filename = path.name
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename={filename}"
                        )
                        message.attach(part)
                        logger.info(f"Attached file: {filename} ({file_size_mb:.2f}MB)")
                        
                except Exception as e:
                    logger.error(f"Failed to attach {file_path}: {str(e)}")
                    continue
        
        # Send email via SMTP
        await aiosmtplib.send(
            message,
            hostname=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_USERNAME,
            password=settings.EMAIL_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            timeout=30
        )
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except aiosmtplib.SMTPException as e:
        logger.error(f"SMTP error sending email to {to_email}: {str(e)}")
        return False
        
    except Exception as e:
        logger.error(f"Unexpected error sending email to {to_email}: {str(e)}")
        return False


async def send_invoice_email(
    to_email: str,
    client_name: str,
    invoice_number: str,
    total: float,
    currency: str,
    pdf_path: str,
    payment_link: Optional[str] = None,
    custom_message: Optional[str] = None,
    due_date: Optional[str] = None
) -> bool:
    """
    Send invoice email with professional template
    
    Args:
        to_email: Client email address
        client_name: Client's name
        invoice_number: Invoice number
        total: Total amount
        currency: Currency code
        pdf_path: Path to PDF file
        payment_link: Optional payment URL
        custom_message: Optional custom message
        due_date: Optional due date string
        
    Returns:
        True if sent successfully
    """
    subject = f"Invoice {invoice_number} from {settings.EMAIL_FROM_NAME}"
    
    # Build payment section
    payment_section = ""
    if payment_link:
        payment_section = f"""
        <div style="margin: 30px 0; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px;">
            <p style="color: white; font-size: 18px; margin-bottom: 15px; font-weight: 600;">Ready to pay?</p>
            <a href="{payment_link}" 
               style="background-color: white; color: #667eea; padding: 15px 40px; 
                      text-decoration: none; border-radius: 25px; display: inline-block;
                      font-weight: bold; font-size: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                💳 Pay Invoice Now
            </a>
            <p style="color: white; font-size: 12px; margin-top: 15px; opacity: 0.9;">
                Secure payment powered by {settings.APP_NAME}
            </p>
        </div>
        """
    
    # Build custom message section (with HTML escaping for security)
    custom_msg_section = ""
    if custom_message:
        # Basic HTML escaping to prevent injection
        safe_message = (custom_message
                       .replace("&", "&amp;")
                       .replace("<", "&lt;")
                       .replace(">", "&gt;")
                       .replace('"', "&quot;")
                       .replace("'", "&#x27;"))
        custom_msg_section = f"""
        <div style="background-color: #f8f9fa; padding: 20px; border-left: 4px solid #667eea; 
                    margin: 25px 0; border-radius: 5px;">
            <p style="margin: 0; color: #495057; line-height: 1.6; font-size: 15px;">
                💬 <strong>Message from us:</strong><br>
                {safe_message}
            </p>
        </div>
        """
    
    # Build due date section
    due_date_section = ""
    if due_date:
        due_date_section = f"""
        <p style="background-color: #fff3cd; padding: 12px; border-radius: 5px; 
                  border-left: 4px solid #ffc107; margin: 20px 0;">
            ⏰ <strong>Due Date:</strong> {due_date}
        </p>
        """
    
    # Create HTML email body
    body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Invoice {invoice_number}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                 background-color: #f4f4f4;">
        <div style="max-width: 600px; margin: 20px auto; background-color: #ffffff; 
                    border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 40px 30px; text-align: center;">
                <h1 style="margin: 0 0 10px 0; font-size: 32px; font-weight: 700;">
                    📄 New Invoice
                </h1>
                <p style="margin: 0; font-size: 16px; opacity: 0.9;">
                    Invoice #{invoice_number}
                </p>
            </div>
            
            <!-- Content -->
            <div style="padding: 40px 30px;">
                <p style="font-size: 16px; color: #333; margin-top: 0;">
                    Dear <strong>{client_name}</strong>,
                </p>
                
                <p style="font-size: 15px; color: #666; line-height: 1.6;">
                    Thank you for your business! Please find attached your invoice.
                </p>
                
                {custom_msg_section}
                
                <!-- Invoice Details Box -->
                <div style="background-color: #f8f9fa; padding: 25px; border-radius: 8px; 
                            margin: 25px 0; border: 2px solid #e9ecef;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 10px 0; color: #666; font-size: 14px;">
                                <strong>Invoice Number:</strong>
                            </td>
                            <td style="padding: 10px 0; text-align: right; color: #333; font-size: 14px;">
                                {invoice_number}
                            </td>
                        </tr>
                        <tr style="border-top: 1px solid #dee2e6;">
                            <td style="padding: 10px 0; color: #666; font-size: 14px;">
                                <strong>Total Amount:</strong>
                            </td>
                            <td style="padding: 10px 0; text-align: right; font-size: 20px; 
                                       font-weight: bold; color: #667eea;">
                                {total:.2f} {currency}
                            </td>
                        </tr>
                    </table>
                </div>
                
                {due_date_section}
                
                {payment_section}
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #e9ecef;">
                    <p style="font-size: 14px; color: #666; margin-bottom: 10px;">
                        🔍 Your invoice is attached as a PDF file.
                    </p>
                    <p style="font-size: 14px; color: #666; margin: 0;">
                        If you have any questions, please don't hesitate to contact us.
                    </p>
                </div>
                
                <p style="font-size: 15px; color: #333; margin-top: 30px;">
                    Best regards,<br>
                    <strong style="color: #667eea;">{settings.EMAIL_FROM_NAME}</strong>
                </p>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f8f9fa; padding: 25px 30px; text-align: center; 
                        border-top: 1px solid #e9ecef;">
                <p style="margin: 0 0 5px 0; color: #999; font-size: 12px;">
                    This is an automated email from {settings.APP_NAME}
                </p>
                <p style="margin: 0; color: #999; font-size: 12px;">
                    Please do not reply directly to this email.
                </p>
            </div>
            
        </div>
    </body>
    </html>
    """
    
    return await send_email(
        to_email=to_email,
        subject=subject,
        body=body,
        attachments=[pdf_path] if pdf_path and Path(pdf_path).exists() else None,
        is_html=True
    )


async def send_welcome_email(to_email: str, username: str, full_name: Optional[str] = None) -> bool:
    """
    Send welcome email to new user
    
    Args:
        to_email: User email
        username: Username
        full_name: User's full name
        
    Returns:
        True if sent successfully
    """
    display_name = full_name or username
    subject = f"Welcome to {settings.APP_NAME}! 🎉"
    
    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #667eea;">Welcome to {settings.APP_NAME}!</h1>
            
            <p>Hi {display_name},</p>
            
            <p>Thank you for signing up! Your account has been created successfully.</p>
            
            <p><strong>Your username:</strong> {username}</p>
            
            <p>You can now start creating professional invoices in just a few clicks!</p>
            
            <div style="margin: 30px 0; padding: 20px; background-color: #f8f9fa; border-radius: 5px;">
                <h3 style="margin-top: 0;">Quick Start:</h3>
                <ol>
                    <li>Login to your account</li>
                    <li>Create your first invoice</li>
                    <li>Send it to your client via email</li>
                    <li>Get paid!</li>
                </ol>
            </div>
            
            <p>If you have any questions, feel free to contact us.</p>
            
            <p>Best regards,<br>
            <strong>{settings.APP_NAME} Team</strong></p>
        </div>
    </body>
    </html>
    """
    
    return await send_email(
        to_email=to_email,
        subject=subject,
        body=body,
        is_html=True
    )
