import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_simple():
    """Simple test for Gemini API with new models"""
    
    # Check if API key exists
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"🔑 API Key: {'✅ Found' if api_key else '❌ Missing'}")
    
    if not api_key:
        print("❌ Please set GEMINI_API_KEY in your .env file")
        return False
    
    try:
        import google.generativeai as genai
        
        # Configure with API key
        genai.configure(api_key=api_key)
        print("✅ Google Generative AI configured")
        
        # Test with the new Gemini 2.0 Flash model
        try:
            print("🤖 Testing gemini-2.0-flash...")
            model = genai.GenerativeModel('models/gemini-2.0-flash')
            response = model.generate_content("Say 'Hello World' in one word.")
            print(f"✅ gemini-2.0-flash: {response.text}")
            return True
        except Exception as e:
            print(f"❌ gemini-2.0-flash failed: {e}")
        
        # Test with gemini-pro-latest as fallback
        try:
            print("🤖 Testing gemini-pro-latest...")
            model = genai.GenerativeModel('models/gemini-pro-latest')
            response = model.generate_content("Say 'Hello World' in one word.")
            print(f"✅ gemini-pro-latest: {response.text}")
            return True
        except Exception as e:
            print(f"❌ gemini-pro-latest failed: {e}")
            
        return False
        
    except ImportError:
        print("❌ google-generativeai not installed")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Gemini 2.0 API...")
    success = test_gemini_simple()
    if success:
        print("🎉 Gemini 2.0 API is working!")
    else:
        print("❌ Gemini API configuration issue")