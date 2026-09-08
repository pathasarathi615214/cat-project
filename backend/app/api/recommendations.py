"""API endpoints for recommendations based on analysis.

Provides routes to fetch recommendations for a specific build.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.recommendation import Recommendation
from ..schemas.recommendation import RecommendationSchema

router = APIRouter()

@router.get("/{build_id}", response_model=list[RecommendationSchema])
def get_recommendations(build_id: str, db: Session = Depends(get_db)):
    recs = db.query(Recommendation).filter(Recommendation.build_id == build_id).all()
    if not recs:
        raise HTTPException(status_code=404, detail="No recommendations found for this build")
    return recs
