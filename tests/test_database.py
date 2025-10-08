cat > test_database.py << 'EOF'
import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_database():
    """اختبر اتصال قاعدة البيانات وإنشاء الجداول"""
    print("🔍 Testing database connection...")
    
    try:
        from app.database import engine, Base
        from app.models.user import User
        from app.models.invoice import Invoice
        
        # تحقق من اتصال قاعدة البيانات
        with engine.connect() as conn:
            print("✅ Database connection successful")
        
        # تحقق من الجداول
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"📊 Database tables: {tables}")
        
        if 'users' in tables and 'invoices' in tables:
            print("✅ All required tables exist")
        else:
            print("❌ Missing tables. Recreating...")
            Base.metadata.drop_all(bind=engine)
            Base.metadata.create_all(bind=engine)
            print("✅ Tables recreated")
            
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_database()
EOF