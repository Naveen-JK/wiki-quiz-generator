from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class WikipediaArticle(Base):
    __tablename__ = "wikipedia_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), unique=True, index=True)
    title = Column(String(255))
    summary = Column(Text)
    key_entities = Column(JSON)
    sections = Column(JSON)
    quiz_data = Column(JSON)
    related_topics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    raw_html = Column(Text)

    def to_dict(self):
        """Convert SQLAlchemy object to dictionary"""
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "summary": self.summary,
            "key_entities": self.key_entities if self.key_entities else {},
            "sections": self.sections if self.sections else [],
            "quiz": self.quiz_data if self.quiz_data else [],
            "related_topics": self.related_topics if self.related_topics else [],
            "created_at": self.created_at
        }