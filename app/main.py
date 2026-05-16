from fastapi import FastAPI
from app.routes.chat import router as chat_router

app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0.0"
)

# Root Route
@app.get("/")
def root():
    return {
        "message": "SHL Assessment Recommendation API is running"
    }

# Health Check
@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# Chat Routes
app.include_router(chat_router)