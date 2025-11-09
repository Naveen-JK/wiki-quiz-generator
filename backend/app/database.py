from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use your Neon connection string - with fallback
DATABASE_URL = os.getenv("DATABASE_URL")

# If DATABASE_URL is not found in .env, use the direct connection string
if not DATABASE_URL:
    DATABASE_URL = "postgresql://neondb_owner:npg_Lp2aPZHN3eSo@ep-delicate-union-ahepec23-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
    print("⚠️  Using direct database URL (environment variable not loaded)")

print(f"🔗 Database URL: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'Loading...'}")

# Create engine with pool settings for serverless PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Important for serverless connections
    pool_recycle=300,    # Recycle connections every 5 minutes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Test the database connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print("✅ Connected to Neon PostgreSQL successfully!")
        print(f"📊 Database: {db_version[0]}")
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False