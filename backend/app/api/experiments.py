"""API endpoints for experiment management.

Provides routes to create a new experiment, record recommendations, and fetch experiment results.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.experiment_service import create_experiment, record_recommendation, get_experiment_results
from ..schemas.experiment import ExperimentCreateSchema, ExperimentResultSchema

router = APIRouter()

@router.post("/", response_model=ExperimentResultSchema, status_code=status.HTTP_201_CREATED)
def start_experiment(exp: ExperimentCreateSchema, db: Session = Depends(get_db)):
    try:
        return create_experiment(db, exp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{build_id}/recommendations", status_code=status.HTTP_204_NO_CONTENT)
def add_recommendation(build_id: str, recommendation: dict, db: Session = Depends(get_db)):
    # Expect recommendation dict with fields matching Recommendation model
    from ..models.recommendation import Recommendation
    rec = Recommendation(**recommendation, build_id=build_id)
    try:
        record_recommendation(db, build_id, rec)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{build_id}", response_model=dict)
def get_experiment(build_id: str, db: Session = Depends(get_db)):
    result = get_experiment_results(db, build_id)
    if not result:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return result
