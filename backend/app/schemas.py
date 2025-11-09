from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class QuizRequest(BaseModel):
    url: str

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: str
    difficulty: str

class QuizResponse(BaseModel):
    id: int
    url: str
    title: str
    summary: str
    key_entities: Dict
    sections: List[str]
    quiz: List[QuizQuestion]
    related_topics: List[str]
    created_at: datetime

class QuizListResponse(BaseModel):
    id: int
    url: str
    title: str
    created_at: datetime