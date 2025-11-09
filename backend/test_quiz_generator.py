import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

def test_quiz_generation():
    print("🧪 Testing Full Quiz Generation...")
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Test with Alan Turing content
    test_content = """
    Alan Turing was a British mathematician, computer scientist, and cryptanalyst. 
    He is considered the father of theoretical computer science and artificial intelligence.
    During World War II, Turing worked at Bletchley Park and developed the bombe machine to decrypt German Enigma messages.
    Turing introduced the concept of the Turing machine in 1936.
    """
    
    prompt = f"""
    Generate a short quiz based on this content:

    {test_content}

    Create 2 multiple choice questions. Format as:

    Q1: What was Alan Turing known for?
    A) Inventing the telephone
    B) Developing computer science and AI
    C) Discovering electricity
    D) Writing Shakespeare's plays
    Correct: B

    Q2: Where did Turing work during WWII?
    A) NASA
    B) Bletchley Park
    C) Harvard University
    D) The White House
    Correct: B
    """
    
    try:
        print("📤 Generating quiz...")
        response = model.generate_content(prompt)
        print("✅ Quiz generated successfully!")
        print("=" * 50)
        print(response.text)
        print("=" * 50)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_quiz_generation()