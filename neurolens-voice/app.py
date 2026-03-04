"""
NeuroLens — Voice & Paralinguistic Analysis Engine
Member 3: Voice stress, cognitive load, and emotional tone from audio.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes.analyze import router as analyze_router
from routes.health import router as health_router

app = FastAPI(
    title="NeuroLens Voice API",
    description="Paralinguistic stress and cognitive load analysis from audio input.",
    version="1.0.0"
)

# Allow frontend (React) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # In production: restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(analyze_router, prefix="/api/voice")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8003, reload=True)
