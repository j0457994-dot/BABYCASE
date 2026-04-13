from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import schemas
from typing import Dict, Any

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_campaign_metrics(self, campaign_id: int) -> Dict[str, Any]:
        """Get comprehensive campaign metrics"""
        campaign = self.db.query(schemas.Campaign).filter(schemas.Campaign.id == campaign_id).first()
        
        if not campaign:
            return {}
        
        # Count events
        events = self.db.query(schemas.CampaignEvent).filter(
            schemas.CampaignEvent.campaign_id == campaign_id
        ).all()
        
        opens = [e for e in events if e.event_type == "email_opened"]
        clicks = [e for e in events if e.event_type == "link_clicked"]
        replies = [e for e in events if e.event_type == "reply_received"]
        
        return {
            "campaign_id": campaign_id,
            "status": campaign.status,
            "emails_sent": len(campaign.emails_sent) if campaign.emails_sent else 0,
            "open_rate": len(opens) / len(campaign.emails_sent) * 100 if campaign.emails_sent else 0,
            "click_rate": len(clicks) / len(campaign.emails_sent) * 100 if campaign.emails_sent else 0,
            "reply_rate": len(replies) / len(campaign.emails_sent) * 100 if campaign.emails_sent else 0,
            "detection_score": campaign.detection_score,
            "total_events": len(events),
            "unique_opens": len(set(e.recipient_email for e in opens)),
            "unique_clicks": len(set(e.recipient_email for e in clicks))
        }