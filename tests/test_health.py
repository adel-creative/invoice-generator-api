cat > test_health.py << 'EOF'
import requests

def test_health():
    """اختبر إذا كان الخادم يعمل"""
    url = "http://localhost:8000/health"
    
    print("🏥 Testing server health...")
    
    try:
        response = requests.get(url, timeout=5)
        print(f"✅ Health check: {response.status_code} - {response.text}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running! Start with: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    test_health()
EOF