import json
import os
import subprocess

# 🔧 إعدادات عامة
OPENAPI_FILE = "openapi.json"
OUTPUT_FILE = "openapi_ready.json"
BASE_URL = "https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app"
RAPIDAPI_API_KEY = os.getenv("RAPIDAPI_API_KEY")  # ضع المفتاح هنا أو في البيئة

def inject_base_url(data):
    """إضافة x-rapidapi-base-url لكل endpoint"""
    paths = data.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            if isinstance(details, dict):
                details["x-rapidapi-base-url"] = BASE_URL
    return data

def main():
    print("🔍 قراءة ملف OpenAPI...")
    with open(OPENAPI_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 🧩 إضافة base URL في كل endpoint
    data = inject_base_url(data)

    # 💾 حفظ الملف الجديد
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ تم إنشاء الملف الجديد: {OUTPUT_FILE}")

    # 🚀 رفع الملف تلقائيًا (اختياري)
    if RAPIDAPI_API_KEY:
        print("🚀 رفع الملف إلى RapidAPI...")
        subprocess.run([
            "npx", "rapidapi", "upload",
            "--apiKey", RAPIDAPI_API_KEY,
            "--file", OUTPUT_FILE,
            "--base", BASE_URL
        ])
    else:
        print("⚠️ لم يتم العثور على RAPIDAPI_API_KEY، تم فقط إنشاء الملف دون رفعه.")

if __name__ == "__main__":
    main()
