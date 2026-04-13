from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# CHANGE THESE - use absolute imports
from app.api.v1.endpoints import router as api_router
from app.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting OMEGA-RED v2.0...")
    init_db()
    logger.info("✅ Database initialized")
    yield
    logger.info("🛑 Shutting down OMEGA-RED...")

app = FastAPI(
    title="OMEGA-RED v2.0",
    description="Harvard/MIT Grade Red Team Operations Platform",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"name": "OMEGA-RED", "version": "2.0.0", "status": "operational"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": ["api", "database"]}
