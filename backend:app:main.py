from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.api.v1.endpoints import router as api_router
from app.database import init_db, engine, Base
from app.core.rate_limiter import limiter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting OMEGA-RED v2.0...")
    init_db()
    logger.info("✅ Database initialized")
    yield
    # Shutdown
    logger.info("🛑 Shutting down OMEGA-RED...")

# Initialize FastAPI
app = FastAPI(
    title="OMEGA-RED v2.0",
    description="Harvard/MIT Grade Red Team Operations Platform",
    version="2.0.0",
    lifespan=lifespan
)

# Rate limiter handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "name": "OMEGA-RED",
        "version": "2.0.0",
        "status": "operational",
        "message": "Harvard/MIT Red Team Platform Online"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": ["api", "database", "celery"]}