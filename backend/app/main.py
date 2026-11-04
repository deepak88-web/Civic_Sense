
from fastapi import FastAPI

from backend.app.routes.prediction import router as prediction_router


app = FastAPI(
    title="CivicSense API",
    description="Multilingual Civic Complaint Classification System",
    version="1.0.0"
)


# Register API routes
app.include_router(prediction_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to CivicSense API",
        "status": "running"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy"
    }
