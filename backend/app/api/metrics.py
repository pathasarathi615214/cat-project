"""Metrics API endpoints for CI Bottleneck Analyzer.

Provides both simple count endpoints (existing) and an aggregated overall metrics endpoint
that returns cache hit rate, parallel efficiency, average queue time and total queued builds.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Import models for count endpoints
from ..models.build import Build
from ..models.task import Task
from ..models.agent import Agent
from ..models.recommendation import Recommendation

from ..database import get_db
from ..services.metrics_service import overall_metrics

router = APIRouter()

# Existing count endpoints (preserved)
@router.get("/builds/count")
def count_builds(db: Session = Depends(get_db)):
    total = db.query(Build).count()
    return {"total_builds": total}

@router.get("/tasks/count")
def count_tasks(db: Session = Depends(get_db)):
    total = db.query(Task).count()
    return {"total_tasks": total}

@router.get("/agents/count")
def count_agents(db: Session = Depends(get_db)):
    total = db.query(Agent).count()
    return {"total_agents": total}

@router.get("/recommendations/count")
def count_recommendations(db: Session = Depends(get_db)):
    total = db.query(Recommendation).count()
    return {"total_recommendations": total}

# New aggregated metrics endpoint
@router.get("/", response_model=dict)
@router.get("/overall", response_model=dict)
def get_overall_metrics(db: Session = Depends(get_db)):
    """Return a dictionary with key performance indicators.

    Uses the metrics_service functions to compute cache hit rate, parallelisation
    efficiency, average queue time and total queued builds.
    """
    try:
        overall = overall_metrics(db)
        from ..services.queue_service import compute_queue_metrics
        overall.update(compute_queue_metrics(db))
        return overall
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
