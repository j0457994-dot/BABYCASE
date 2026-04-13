from celery import Celery
from ..core.config import settings
from ..database import SessionLocal
from ..models import schemas
import logging

celery_app = Celery(
    "omega_red",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,
)

logger = logging.getLogger(__name__)

@celery_app.task(name="run_campaign")
def run_campaign(campaign_id: int, test_mode: bool = False):
    """Execute a full campaign with all phases"""
    db = SessionLocal()
    try:
        campaign = db.query(schemas.Campaign).filter(schemas.Campaign.id == campaign_id).first()
        if not campaign:
            logger.error(f"Campaign {campaign_id} not found")
            return {"error": "Campaign not found"}
        
        logger.info(f"Starting campaign {campaign_id} in {'test' if test_mode else 'production'} mode")
        
        # Update status
        campaign.status = "running"
        db.commit()
        
        # TODO: Implement actual email sending logic here
        # This is where your AI generation and email delivery would go
        
        campaign.status = "completed"
        campaign.completed_at = datetime.utcnow()
        db.commit()
        
        return {"status": "completed", "campaign_id": campaign_id}
        
    except Exception as e:
        logger.error(f"Campaign {campaign_id} failed: {e}")
        if campaign:
            campaign.status = "failed"
            db.commit()
        return {"error": str(e)}
    finally:
        db.close()

@celery_app.task(name="enrich_target_async")
def enrich_target_async(target_id: int, deep_scan: bool = False, include_darkweb: bool = False):
    """Background OSINT enrichment"""
    db = SessionLocal()
    try:
        target = db.query(schemas.Target).filter(schemas.Target.id == target_id).first()
        if not target:
            logger.error(f"Target {target_id} not found")
            return {"error": "Target not found"}
        
        logger.info(f"Enriching target {target_id} (deep_scan={deep_scan})")
        
        # TODO: Implement actual OSINT logic here
        # This would call Hunter.io, Clearbit, etc.
        
        target.risk_score = 0.5  # Placeholder
        db.commit()
        
        return {"status": "completed", "target_id": target_id}
        
    except Exception as e:
        logger.error(f"Enrichment failed for target {target_id}: {e}")
        return {"error": str(e)}
    finally:
        db.close()