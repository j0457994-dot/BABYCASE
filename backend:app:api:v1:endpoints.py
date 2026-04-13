from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# CHANGE THESE - use absolute imports
from app.database import get_db
from app.models import schemas
from app.tasks.worker import run_campaign, enrich_target_async
from app.services.osint_service import OSINTService
from app.services.analytics_service import AnalyticsService
from app.core.rate_limiter import limiter
from app.core.security import require_api_key, generate_api_key

import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class EnrichRequest(BaseModel):
    target_id: int
    deep_scan: bool = False
    include_darkweb: bool = False

class CampaignLaunchRequest(BaseModel):
    campaign_id: int
    scheduled_time: Optional[str] = None
    test_mode: bool = False

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/auth/login")
async def login(request: LoginRequest):
    """Simple login endpoint - returns API key"""
    # In production, validate against database
    if request.username == "admin" and request.password == "redteam2024":
        api_key = generate_api_key(request.username)
        return {"api_key": api_key, "message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/targets/enrich")
async def start_enrichment(
    request: EnrichRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: dict = Depends(require_api_key)
):
    """MIT-Level: Multi-source OSINT enrichment with background processing"""
    target = db.query(schemas.Target).filter(schemas.Target.id == request.target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    
    # Start async enrichment
    enrich_target_async.delay(request.target_id, request.deep_scan, request.include_darkweb)
    
    return {
        "status": "enrichment_started",
        "target_id": request.target_id,
        "estimated_completion": "30-60 seconds",
        "task_type": "deep_scan" if request.deep_scan else "standard"
    }

@router.post("/campaigns/launch/{campaign_id}")
async def launch_campaign(
    campaign_id: int,
    request: Optional[CampaignLaunchRequest] = None,
    db: Session = Depends(get_db),
    user: dict = Depends(require_api_key)
):
    """Harvard-Grade: Multi-vector campaign deployment"""
    campaign = db.query(schemas.Campaign).filter(schemas.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    if campaign.status not in ["draft", "paused"]:
        raise HTTPException(status_code=400, detail=f"Cannot launch campaign in {campaign.status} status")
    
    # Update campaign status
    campaign.status = "scheduled"
    campaign.started_at = datetime.utcnow()
    db.commit()
    
    # Deploy to Celery cluster
    test_mode = request.test_mode if request else False
    task = run_campaign.delay(campaign_id, test_mode=test_mode)
    
    logger.info(f"Campaign {campaign_id} launched with task ID: {task.id}")
    
    return {
        "status": "campaign_deployed",
        "campaign_id": campaign_id,
        "task_id": task.id,
        "celery_queue": "priority",
        "estimated_execution": "immediate"
    }

@router.get("/campaigns/{campaign_id}/metrics")
async def get_campaign_metrics(
    campaign_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_api_key)
):
    """Real-time campaign analytics"""
    analytics = AnalyticsService(db)
    metrics = analytics.get_campaign_metrics(campaign_id)
    
    return {
        "campaign_id": campaign_id,
        "metrics": metrics,
        "live_tracking": True
    }

@router.get("/targets/{target_id}/intelligence")
async def get_target_intelligence(
    target_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_api_key)
):
    """Complete OSINT dossier on target"""
    target = db.query(schemas.Target).filter(schemas.Target.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    
    osint_service = OSINTService(db)
    intelligence = await osint_service.get_complete_dossier(target)
    
    return intelligence
