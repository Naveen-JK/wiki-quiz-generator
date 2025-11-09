import google.generativeai as genai
import os
from dotenv import load_dotenv

print("🔍 Loading environment variables...")
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"🔑 API Key status: {'✅ Found' if api_key else '❌ Not found'}")

if api_key:
    print(f"📝 Key length: {len(api_key)} characters")
    genai.configure(api_key=api_key)
    
    # Simple test
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Say 'Quiz test successful' in one word.")
    print(f"🤖 API Response: {response.text}")
else:
    print("❌ Please check your .env file")