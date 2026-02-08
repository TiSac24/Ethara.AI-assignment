"""
Vercel serverless function entry point
This file is used when deploying to Vercel
"""
import sys
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Import the FastAPI app
from main import app

# Vercel expects the handler to be named 'handler'
# FastAPI app works directly with Vercel's Python runtime
handler = app

