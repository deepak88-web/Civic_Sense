
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.prediction import router as prediction_router


app = FastAPI(
    title="CivicSense API",
    description="Multilingual Civic Complaint Classification System",
    version="1.0.0"
)

# Allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to CivicSense API",
        "status": "running"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
