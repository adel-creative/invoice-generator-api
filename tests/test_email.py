# test_email.py
import asyncio
from app.services.email_service import send_email

async def test():
    result = await send_email(
        to_email="your-test-email@example.com",
        subject="Test Email",
        body="<h1>Test successful!</h1>",
        is_html=True
    )
    print("✅ Email sent!" if result else "❌ Email failed")

asyncio.run(test())