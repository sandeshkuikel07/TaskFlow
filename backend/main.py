from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging

# Fix these imports
from backend.database import engine, Base, get_db
from backend.routes import tasks, categories
from backend.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow API",
    description="A FastAPI backend for the TaskFlow application",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add this middleware before your other middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url.path} {request.scope.get('http_version', '')}")
    response = await call_next(request)
    return response

# Include routers
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])

@app.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint to verify API is running and database is connected"""
    return {"status": "healthy", "database": "connected"}