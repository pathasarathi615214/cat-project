"""Pydantic schema for CI tasks."""

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TaskSchema(BaseModel):
    task_id: str
    build_id: str
    task_name: str
    task_type: str
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    cache_hit: Optional[bool] = None
    dependencies: Optional[List[str]] = None
    status: str

    class Config:
        orm_mode = True
