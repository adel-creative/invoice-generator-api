cat > test_register.py << 'EOF'
import requests
import json

def test_register():
    """اختبر عملية التسجيل"""
    url = "http://localhost:8000/auth/register"
    
    # بيانات بسيطة للتسجيل
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Test User"
    }
    
    print("🔄 Testing user registration...")
    print(f"📤 Sending data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, timeout=10)
        
        print(f"📥 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 201:
            print("🎉 SUCCESS! User registered successfully!")
            result = response.json()
            print(f"👤 User created with ID: {result.get('id', 'N/A')}")
        elif response.status_code == 500:
            print("❌ Internal Server Error - Check server logs")
        elif response.status_code == 422:
            print("❌ Validation Error - Check input data")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("🚫 Connection Error - Is the server running?")
    except requests.exceptions.Timeout:
        print("⏰ Request Timeout - Server took too long to respond")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")

if __name__ == "__main__":
    test_register()
EOF