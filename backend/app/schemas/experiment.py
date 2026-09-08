"""Pydantic schemas for experiment management.

ExperimentCreateSchema: input data for creating an experiment.
ExperimentResultSchema: output representation of an experiment (mirrors Build model fields).
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExperimentCreateSchema(BaseModel):
    """Input schema for creating an experiment.

    Attributes:
        build_id: Identifier for the associated build.
        description: Optional description of the experiment.
    """
    build_id: str
    description: Optional[str] = None

class ExperimentResultSchema(BaseModel):
    """Result schema for an experiment.

    Mirrors the Build model fields (subset).
    """
    id: int
    build_id: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
