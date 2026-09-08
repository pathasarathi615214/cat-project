"""Service for managing experiments and storing results.

Provides functions to create a new experiment, record metrics, and retrieve past experiments.
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any

from ..models.build import Build
from ..models.recommendation import Recommendation
from ..schemas.experiment import ExperimentCreateSchema, ExperimentResultSchema

def create_experiment(db: Session, experiment: ExperimentCreateSchema) -> ExperimentResultSchema:
    """Create a new experiment entry.

    For this simplified implementation we store experiment metadata as a Build entry
    with a special flag indicating it's an experiment.
    """
    new_build = Build(
        build_id=experiment.build_id,
        start_time=datetime.utcnow(),
        is_experiment=True,
        description=experiment.description,
    )
    db.add(new_build)
    db.commit()
    db.refresh(new_build)
    return ExperimentResultSchema.from_orm(new_build)

def record_recommendation(db: Session, build_id: str, recommendation: Recommendation) -> None:
    """Associate a recommendation with a specific build/experiment."""
    db.add(recommendation)
    db.commit()

def get_experiment_results(db: Session, build_id: str) -> Dict[str, Any]:
    """Retrieve experiment results and related recommendations."""
    build = db.query(Build).filter(Build.build_id == build_id).first()
    if not build:
        return {}
    recs = db.query(Recommendation).filter(Recommendation.build_id == build_id).all()
    return {
        "build": build,
        "recommendations": recs,
    }
