from pydantic_settings import BaseSettings
from typing import List, Optional
import secrets

class Settings(BaseSettings):
    # API Keys
    OPENROUTER_API_KEY: str
    HUNTER_API_KEY: str
    CLEARBIT_API_KEY: Optional[str] = ""
    OPENAI_API_KEY: Optional[str] = ""
    ANTHROPIC_API_KEY: Optional[str] = ""
    
    # Infrastructure
    DATABASE_URL: str = "postgresql://redteam:supersecurepass@postgres:5432/redteam"
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"
    
    # Email Relay (Multi-provider)
    SMTP_SERVERS: List[dict] = [
        {"server": "smtp.sendgrid.net", "port": 587, "user": "", "pass": ""},
        {"server": "smtp.mailgun.org", "port": 587, "user": "", "pass": ""},
        {"server": "smtp.office365.com", "port": 587, "user": "", "pass": ""}
    ]
    
    # Security & Limits
    MAX_WIRE_AMOUNT: float = 1.00
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60
    JWT_SECRET: str = secrets.token_urlsafe(32)
    ENCRYPTION_KEY: str = secrets.token_urlsafe(32)
    
    # Evasion Settings
    PROXY_ROTATION_URL: Optional[str] = None
    USER_AGENT_ROTATION: bool = True
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    SENTRY_DSN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()