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
    
    # Test with Alan Turing content (similar to your app)
    test_content = """
    Alan Turing was a British mathematician, computer scientist, and cryptanalyst. 
    He is considered the father of theoretical computer science and artificial intelligence.
    During World War II, Turing worked at Bletchley Park and developed the bombe machine to decrypt German Enigma messages.
    Turing introduced the concept of the Turing machine in 1936, which formalized the concepts of algorithm and computation.
    He also proposed the Turing test in 1950 to measure machine intelligence.
    """
    
    prompt = f"""
    Generate a quiz based on the following content about Alan Turing:
    
    {test_content}
    
    Create 5 multiple choice questions with 4 options each. Format as JSON:
    
    {{
      "quiz_title": "Alan Turing Quiz",
      "questions": [
        {{
          "question": "Question text here?",
          "options": {{
            "A": "Option A",
            "B": "Option B", 
            "C": "Option C",
            "D": "Option D"
          }},
          "correct_answer": "A"
        }}
      ]
    }}
    
    Return ONLY the JSON, no other text.
    """
    
    try:
        print("📤 Generating quiz...")
        response = model.generate_content(prompt)
        print("✅ Quiz generated successfully!")
        print("📝 Response:")
        print(response.text)
        
        # Try to parse as JSON to verify structure
        import json
        quiz_data = json.loads(response.text.strip())
        print("🎉 JSON parsed successfully!")
        print(f"📊 Generated {len(quiz_data['questions'])} questions")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔍 Response content:")
        print(response.text if 'response' in locals() else "No response")

if __name__ == "__main__":
    test_quiz_generation()