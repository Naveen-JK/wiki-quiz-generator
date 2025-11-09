import os
import sys
sys.path.append(os.path.dirname(__file__))

from app.llm_service import test_gemini_connection

if __name__ == "__main__":
    print("🧪 Testing Gemini API Connection...")
    success = test_gemini_connection()
    if success:
        print("🎉 Gemini API is working correctly!")
    else:
        print("❌ Gemini API configuration issue detected")