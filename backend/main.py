from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.behavior import router as behavior_router
from database.db import init_db
from api.assessment import router as assessment_router

app = FastAPI(title="Cognitive Stability Backend")

# Enable CORS (so React frontend can call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(behavior_router, prefix="/api/behavior", tags=["Behavior"])
app.include_router(assessment_router, prefix="/api/assessment", tags=["Assessment"])

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Cognitive Stability Backend Running"}