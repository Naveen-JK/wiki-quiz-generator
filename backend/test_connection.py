import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import test_connection

if __name__ == "__main__":
    test_connection()