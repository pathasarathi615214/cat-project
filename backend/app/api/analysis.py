"""API endpoints for analysis of CI data and bottleneck detection.

Provides routes to trigger analysis and retrieve results.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.bottleneck_service import analyze_builds
from ..schemas.analysis import AnalysisResultSchema

router = APIRouter()

@router.post("/run", response_model=AnalysisResultSchema, status_code=status.HTTP_202_ACCEPTED)
def run_analysis(db: Session = Depends(get_db)):
    try:
        result = analyze_builds(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
