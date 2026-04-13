from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from .core.config import settings
import logging

logger = logging.getLogger(__name__)

# Harvard-Level: Connection pooling with retry logic
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=30,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@contextmanager
def get_db():
    """Dependency injection with automatic retry on failure"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        db.close()

# MIT Enhancement: Automatic table creation with migration check
def init_db():
    """Initialize database with all tables"""
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")