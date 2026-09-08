"""SQLAlchemy model for recommendations."""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from ..database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    build_id = Column(String, index=True, nullable=False)
    recommendation_type = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    priority_score = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    estimated_saving_seconds = Column(Float, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    evidence_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=True)
