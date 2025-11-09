# This file combines scraper and llm_service for simplicity
from .scraper import WikipediaScraper
from .llm_service import QuizGenerator

# Re-export the classes
__all__ = ['WikipediaScraper', 'QuizGenerator']