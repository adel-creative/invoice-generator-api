import sys
import os
import subprocess

print("🔧 Starting comprehensive fix...")

# 1. تحقق من التبعيات
print("📦 Checking dependencies...")
try:
    import requests
    import sqlalchemy
    import jose
    import passlib
    import pydantic
    print("✅ All dependencies are installed")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Run: pip install requests sqlalchemy python-jose[cryptography] passlib[bcrypt] pydantic")

# 2. إنشاء المجلدات
print("📁 Creating directories...")
os.makedirs("uploads", exist_ok=True)
os.makedirs("app/schemas", exist_ok=True)
print("✅ Directories created")

# 3. إعادة إنشاء قاعدة البيانات
print("🗄️ Recreating database...")
try:
    from app.database import engine, Base
    from app.models.user import User
    from app.models.invoice import Invoice
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database recreated successfully")
    
except Exception as e:
    print(f"❌ Database error: {e}")

# 4. تحقق من ملف config
print("⚙️ Checking config...")
try:
    from app.config import settings
    print(f"✅ Config loaded - SECRET_KEY: {settings.SECRET_KEY[:10]}...")
except Exception as e:
    print(f"❌ Config error: {e}")
    # أنشئ ملف config إذا لم يكن موجوداً
    config_content = '''
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./invoice.db"
    SECRET_KEY: str = "your-secret-key-change-this-in-production-12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    APP_NAME: str = "Arabic Invoice Generator"
    UPLOAD_DIR: str = "uploads"
    PAYMENT_BASE_URL: str = "http://localhost:8000"
    EMAIL_RATE_LIMIT: int = 5

    class Config:
        env_file = ".env"

settings = Settings()
'''
    with open("app/config.py", "w") as f:
        f.write(config_content)
    print("✅ Config file created")

print("🎯 Comprehensive fix completed!")
print("🚀 Now start the server: uvicorn app.main:app --reload")
EOF

python comprehensive_fix.py