# api/main.py
import sys
import os

# Add project root to Python path (so backend imports work)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.main import app  # Reuse your existing FastAPI app
