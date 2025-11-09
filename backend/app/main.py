from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
import sys
from datetime import datetime

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

# Now import the modules
try:
    # Try absolute import first
    from app import models, schemas
    from app.database import get_db, engine, test_connection
    from app.scraper import WikipediaScraper
    from app.llm_service import QuizGenerator
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback to direct imports
    import models, schemas
    from database import get_db, engine, test_connection
    from scraper import WikipediaScraper
    from llm_service import QuizGenerator

# Create tables
try:
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
except Exception as e:
    print(f"❌ Table creation failed: {e}")

app = FastAPI(title="Wikipedia Quiz Generator", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
scraper = WikipediaScraper()
quiz_gen = QuizGenerator()

@app.on_event("startup")
def startup_event():
    """Test database connection on startup"""
    if test_connection():
        print("🚀 Application started successfully with Neon PostgreSQL")
    else:
        print("⚠️  Application started but database connection failed")

@app.post("/generate-quiz", response_model=schemas.QuizResponse)
async def generate_quiz(
    request: schemas.QuizRequest, 
    db: Session = Depends(get_db)
):
    """Generate quiz from Wikipedia URL"""
    
    try:
        # Check if URL already exists
        existing = db.query(models.WikipediaArticle).filter(
            models.WikipediaArticle.url == request.url
        ).first()
        
        if existing:
            return schemas.QuizResponse(**existing.to_dict())
        
        # Scrape article
        scraped_data = scraper.scrape_article(request.url)
        
        # Generate quiz
        quiz_data = quiz_gen.generate_quiz(
            scraped_data["content"], 
            scraped_data["title"]
        )
        
        # Create database entry
        db_article = models.WikipediaArticle(
            url=request.url,
            title=scraped_data["title"],
            summary=scraped_data["summary"],
            key_entities=scraped_data["key_entities"],
            sections=scraped_data["sections"],
            quiz_data=quiz_data.get("quiz", []),
            related_topics=quiz_data.get("related_topics", []),
            raw_html=scraped_data.get("raw_html", ""),
            created_at=datetime.utcnow()
        )
        
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        
        return schemas.QuizResponse(**db_article.to_dict())
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/quizzes", response_model=List[schemas.QuizListResponse])
async def get_quizzes(db: Session = Depends(get_db)):
    """Get list of all generated quizzes"""
    quizzes = db.query(models.WikipediaArticle).order_by(
        models.WikipediaArticle.created_at.desc()
    ).all()
    
    return [schemas.QuizListResponse(
        id=quiz.id,
        url=quiz.url,
        title=quiz.title,
        created_at=quiz.created_at
    ) for quiz in quizzes]

@app.get("/quizzes/{quiz_id}", response_model=schemas.QuizResponse)
async def get_quiz_details(quiz_id: int, db: Session = Depends(get_db)):
    """Get detailed quiz by ID"""
    quiz = db.query(models.WikipediaArticle).filter(
        models.WikipediaArticle.id == quiz_id
    ).first()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return schemas.QuizResponse(**quiz.to_dict())

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Wikipedia Quiz Generator API", "database": "Neon PostgreSQL"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)