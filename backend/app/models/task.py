"""SQLAlchemy model for CI tasks."""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, JSON
from ..database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True, nullable=False)
    build_id = Column(String, index=True, nullable=False)
    task_name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    cache_hit = Column(Boolean, nullable=True)
    dependencies = Column(JSON, nullable=True)  # list of dependent task_ids
    status = Column(String, nullable=False)
