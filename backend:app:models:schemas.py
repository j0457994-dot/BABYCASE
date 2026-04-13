from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Float, Boolean, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Target(Base):
    __tablename__ = "targets"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    company_name = Column(String(255), nullable=False)
    domain = Column(String(255), nullable=False, index=True)
    industry = Column(String(100))
    employee_count = Column(Integer)
    revenue_range = Column(String(50))
    
    # C-Suite Intelligence
    ceo_name = Column(String(255))
    ceo_email = Column(String(255))
    cfo_name = Column(String(255))
    cfo_email = Column(String(255))
    cto_name = Column(String(255))
    cto_email = Column(String(255))
    cisos = Column(JSON, default=list)  # Multiple security contacts
    
    # OSINT Data
    email_pattern = Column(String(100))
    social_links = Column(JSON, default=dict)
    tech_stack = Column(JSON, default=list)
    recent_news = Column(JSON, default=list)
    
    # Risk Scoring
    risk_score = Column(Float, default=0.0)
    email_confidence = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    campaigns = relationship("Campaign", back_populates="target")
    
    __table_args__ = (
        Index('idx_target_domain', 'domain'),
        Index('idx_target_risk', 'risk_score'),
    )

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    target_id = Column(Integer, ForeignKey("targets.id", ondelete="CASCADE"))
    
    # Campaign Configuration
    pretext_type = Column(String(50))  # invoice, security, hr, vendor, ceo_fraud
    difficulty_level = Column(String(20), default="medium")  # easy, medium, hard, expert
    language = Column(String(10), default="en")
    
    # Status Tracking
    status = Column(String(50), default="draft")
    phase = Column(String(50), default="planning")
    
    # Generated Content
    email_subject = Column(Text)
    email_body = Column(Text)
    email_html = Column(Text)
    attachment_url = Column(String(500))
    
    # Delivery Results
    emails_sent = Column(JSON, default=list)
    open_tracking = Column(JSON, default=dict)
    click_tracking = Column(JSON, default=dict)
    reply_tracking = Column(JSON, default=dict)
    
    # Metrics
    success_metrics = Column(JSON, default=dict)
    detection_score = Column(Float, default=0.0)
    
    # Timeline
    scheduled_time = Column(DateTime)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    target = relationship("Target", back_populates="campaigns")
    events = relationship("CampaignEvent", back_populates="campaign")
    
    __table_args__ = (
        Index('idx_campaign_status', 'status'),
        Index('idx_campaign_target', 'target_id'),
    )

class CampaignEvent(Base):
    __tablename__ = "campaign_events"
    
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"))
    event_type = Column(String(50))  # email_sent, email_opened, link_clicked, reply_received
    recipient_email = Column(String(255))
    user_agent = Column(String(500))
    ip_address = Column(String(45))
    location = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, default=dict)
    
    campaign = relationship("Campaign", back_populates="events")

class IntelligenceReport(Base):
    __tablename__ = "intelligence_reports"
    
    id = Column(Integer, primary_key=True)
    target_id = Column(Integer, ForeignKey("targets.id"))
    report_type = Column(String(50))  # osint, darkweb, social
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)