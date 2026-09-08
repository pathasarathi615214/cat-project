"""Pydantic schema for analysis results."""

from pydantic import BaseModel
from typing import List, Dict, Any

class BottleneckDetail(BaseModel):
    type: str
    description: str
    severity: str
    suggestion: str
    evidence: Dict[str, Any]

class AnalysisResultSchema(BaseModel):
    build_id: str
    bottlenecks: List[BottleneckDetail]
    overall_score: float
    generated_at: str

    class Config:
        orm_mode = True
