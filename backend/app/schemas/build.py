"""Pydantic schema for CI builds."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BuildSchema(BaseModel):
    build_id: str
    service_name: str
    pipeline_name: str
    status: str
    queued_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    queue_time_seconds: Optional[float] = None
    execution_time_seconds: Optional[float] = None
    feedback_time_seconds: Optional[float] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
