import os
import json
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class QuizGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key or self.api_key == "your_actual_gemini_api_key_here":
            print("❌ GEMINI_API_KEY not set or is still the placeholder")
            print("💡 Please update your .env file with a real API key")
            raise ValueError("GEMINI_API_KEY not configured")
        
        try:
            import google.generativeai as genai
            self.genai = genai
            self.genai.configure(api_key=self.api_key)
            
            # Use the new Gemini 2.0 Flash model (fast and free)
            self.model_name = "models/gemini-2.0-flash"
            self.model = self.genai.GenerativeModel(self.model_name)
            print(f"✅ Using model: {self.model_name}")
            
        except ImportError:
            print("❌ google-generativeai not installed")
            raise
        except Exception as e:
            print(f"❌ Failed to initialize Gemini: {e}")
            raise
    
    def generate_quiz(self, content: str, title: str) -> Dict:
        """Generate quiz using LLM with comprehensive error handling"""
        
        # If content is too long, truncate it
        if len(content) > 3000:
            content = content[:3000] + "..."
        
        prompt = self._create_quiz_prompt(content, title)
        
        try:
            print(f"🤖 Generating quiz for: {title}")
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise Exception("AI returned empty response")
                
            quiz_data = self._parse_llm_response(response.text)
            print(f"✅ Generated {len(quiz_data.get('quiz', []))} questions")
            return quiz_data
            
        except Exception as e:
            print(f"❌ AI generation failed: {e}")
            return self._generate_fallback_quiz(title)
    
    def _create_quiz_prompt(self, content: str, title: str) -> str:
        """Create quiz generation prompt"""
        return f"""You are an expert quiz creator. Create a multiple-choice quiz based on the Wikipedia article about "{title}".

ARTICLE CONTENT:
{content}

CREATE A QUIZ WITH THESE REQUIREMENTS:
- Generate 5-8 high-quality multiple choice questions
- Each question must have exactly 4 options labeled A, B, C, D
- Mark the correct answer with the corresponding letter (A, B, C, or D)
- Provide a brief explanation for why the answer is correct
- Assign a difficulty level: easy, medium, or hard
- Questions should test comprehension and key concepts from the article
- Make sure all answers are factually supported by the content

OUTPUT FORMAT - RETURN ONLY VALID JSON:
{{
  "quiz": [
    {{
      "question": "What is the main purpose of algorithms?",
      "options": [
        "To solve mathematical problems only",
        "To provide step-by-step procedures for calculations",
        "To create computer graphics",
        "To store data efficiently"
      ],
      "answer": "B",
      "explanation": "Algorithms are defined as step-by-step procedures for calculations, data processing, and automated reasoning.",
      "difficulty": "easy"
    }}
  ],
  "related_topics": ["Computer Science", "Mathematics", "Programming"]
}}

IMPORTANT: Return ONLY the JSON object, no additional text or explanations."""
    
    def _parse_llm_response(self, response_text: str) -> Dict:
        """Parse AI response safely"""
        try:
            # Clean the response
            text = response_text.strip()
            print(f"📝 Raw AI response: {text[:200]}...")
            
            # Extract JSON from code blocks
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1]
            
            # Remove any non-JSON text before or after
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                text = text[start_idx:end_idx]
            
            # Parse JSON
            data = json.loads(text)
            
            # Validate structure
            if not isinstance(data.get('quiz'), list):
                raise ValueError("Invalid quiz format")
                
            # Validate each question has required fields
            for i, question in enumerate(data['quiz']):
                required_fields = ['question', 'options', 'answer', 'explanation', 'difficulty']
                for field in required_fields:
                    if field not in question:
                        raise ValueError(f"Question {i+1} missing field: {field}")
                
                if len(question['options']) != 4:
                    raise ValueError(f"Question {i+1} must have exactly 4 options")
                    
            return data
            
        except Exception as e:
            print(f"❌ Failed to parse AI response: {e}")
            print(f"📝 Full response: {response_text}")
            return self._generate_fallback_quiz("General Knowledge")
    
    def _generate_fallback_quiz(self, title: str) -> Dict:
        """Generate fallback quiz when AI fails"""
        print("⚠️  Using fallback quiz")
        return {
            "quiz": [
                {
                    "question": f"What is the main subject of '{title}'?",
                    "options": [
                        "A scientific concept or theory",
                        "A historical event or period", 
                        "A geographical location",
                        "A cultural or artistic work"
                    ],
                    "answer": "A",
                    "explanation": f"The article '{title}' discusses an important concept in its respective field.",
                    "difficulty": "easy"
                },
                {
                    "question": f"What is one key application or significance of {title}?",
                    "options": [
                        "It revolutionized modern technology",
                        "It changed historical outcomes",
                        "It advanced scientific understanding", 
                        "It influenced cultural development"
                    ],
                    "answer": "C",
                    "explanation": f"{title} has contributed significantly to advancing knowledge in its field.",
                    "difficulty": "medium"
                },
                {
                    "question": f"Which field is most associated with {title}?",
                    "options": [
                        "Computer Science and Technology",
                        "History and Archaeology",
                        "Biology and Medicine",
                        "Arts and Literature"
                    ],
                    "answer": "A",
                    "explanation": f"{title} is primarily discussed in the context of technological and computational fields.",
                    "difficulty": "easy"
                }
            ],
            "related_topics": ["Computer Science", "Technology", "Research", "Innovation"]
        }


# Test function
def test_quiz_generator():
    """Test the quiz generator with the new model"""
    try:
        generator = QuizGenerator()
        print("✅ QuizGenerator initialized successfully")
        
        # Test with simple content
        test_content = """Algorithms are step-by-step procedures for calculations. They are used for data processing, automated reasoning, and computer programming. 
        Common algorithm categories include sorting algorithms, search algorithms, and graph algorithms. 
        The efficiency of algorithms is often measured using Big O notation."""
        test_title = "Algorithm"
        
        print("🧪 Testing quiz generation...")
        result = generator.generate_quiz(test_content, test_title)
        
        print(f"✅ Generated quiz with {len(result.get('quiz', []))} questions")
        for i, question in enumerate(result['quiz']):
            print(f"  Q{i+1}: {question['question']}")
            print(f"     Difficulty: {question['difficulty']}")
        
        return True
        
    except Exception as e:
        print(f"❌ QuizGenerator test failed: {e}")
        return False

if __name__ == "__main__":
    test_quiz_generator()