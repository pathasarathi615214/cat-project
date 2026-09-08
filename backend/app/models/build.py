"""SQLAlchemy model for CI builds."""

from sqlalchemy import Column, Integer, String, DateTime, Float
from ..database import Base

class Build(Base):
    __tablename__ = "builds"

    id = Column(Integer, primary_key=True, index=True)
    build_id = Column(String, unique=True, index=True, nullable=False)
    service_name = Column(String, nullable=False)
    pipeline_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    queued_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    queue_time_seconds = Column(Float, nullable=True)
    execution_time_seconds = Column(Float, nullable=True)
    feedback_time_seconds = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=True)
