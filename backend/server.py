from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone


from backend.nlp_engine.api.app import nlp_router
from backend.nlp_engine.model.sentiment_model import get_sentiment_model


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')


mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# main app without a prefix
app = FastAPI(
    title="NeuroLens NLP Microservice",
    description="Production-ready NLP microservice for temporal sentiment drift detection",
    version="1.0.0"
)


api_router = APIRouter(prefix="/api")




class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str



@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks


app.include_router(api_router)
app.include_router(nlp_router, prefix="/api")  

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    """Load ML models on startup."""
    logger.info("Starting NLP microservice...")
    try:
        
        model = get_sentiment_model()
        logger.info(f"Sentiment model loaded: {model.is_loaded()}")
    except Exception as e:
        logger.error(f"Failed to load sentiment model on startup: {str(e)}")


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    logger.info("NLP microservice shutdown complete")