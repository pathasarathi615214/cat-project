"""Placeholder for parallelisation analysis service.

Detects tasks that could be run in parallel but are currently sequential.
"""

from sqlalchemy.orm import Session
from ..models.task import Task
from typing import List

def detect_parallelisation_issues(db: Session, build_id: str) -> List[dict]:
    """Return a list of dicts describing parallelisation opportunities.
    Currently a stub – always returns empty list.
    """
    # Real implementation would examine task dependencies and start times.
    return []
