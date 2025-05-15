from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database import engine, Base
from backend.routes import tasks, categories

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow API",
    description="A FastAPI backend for the TaskFlow application",
    version="0.1.0",
)

# Setup CORS middleware using settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])

# Simple health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

# Run the app with uvicorn when executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", host="127.0.0.1", port=8000, reload=True)
