from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import employees, attendance

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HRMS Lite API",
    description="Human Resource Management System API",
    version="1.0.0"
)

# Configure CORS
import os
from dotenv import load_dotenv

load_dotenv()

# Get allowed origins from environment or use defaults
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(employees.router, prefix="/api", tags=["employees"])
app.include_router(attendance.router, prefix="/api", tags=["attendance"])


@app.get("/")
async def root():
    return {"message": "HRMS Lite API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

