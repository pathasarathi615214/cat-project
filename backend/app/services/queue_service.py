"""Service for queue and concurrency metrics.

Provides functions to compute average queue time per build and overall queue length.
"""

from sqlalchemy.orm import Session
from ..models.build import Build
from ..models.task import Task
from typing import Dict

def compute_queue_metrics(db: Session) -> Dict[str, float]:
    """Calculate average queue time and total queued builds.

    Returns a dict with keys:
        - avg_queue_time_seconds
        - total_queued_builds
    """
    builds = db.query(Build).filter(Build.queue_time_seconds != None).all()
    if not builds:
        return {"avg_queue_time_seconds": 0.0, "total_queued_builds": 0}
    total_time = sum(b.queue_time_seconds for b in builds if b.queue_time_seconds)
    avg_time = total_time / len(builds)
    return {"avg_queue_time_seconds": avg_time, "total_queued_builds": len(builds)}
