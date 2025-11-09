import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, test_connection
from app.models import Base

def setup_database():
    """Create tables directly"""
    try:
        print("🔍 Testing database connection to Neon PostgreSQL...")
        
        # Test connection first
        if not test_connection():
            print("❌ Cannot proceed without database connection!")
            return False
        
        # Create tables
        print("📦 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

if __name__ == "__main__":
    setup_database()