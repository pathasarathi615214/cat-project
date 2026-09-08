"""Pydantic schema for recommendations returned by the API."""

from pydantic import BaseModel
from typing import Dict, Any

class RecommendationSchema(BaseModel):
    id: int
    build_id: str
    recommendation_type: str
    priority: str
    priority_score: float
    confidence_score: float
    estimated_saving_seconds: float
    title: str
    description: str
    evidence_json: Dict[str, Any] | None = None
    created_at: str | None = None

    class Config:
        orm_mode = True
