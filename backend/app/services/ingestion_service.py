"""Service to ingest a Build record into the database.

Receives a Pydantic BuildSchema, creates a SQLAlchemy Build instance,
adds it to the session and commits.
"""

from sqlalchemy.orm import Session
from ..models.build import Build
from ..schemas.build import BuildSchema

from datetime import datetime

def ingest_build(db: Session, build_data: BuildSchema) -> Build:
    db_build = Build(
        build_id=build_data.build_id,
        service_name=build_data.service_name,
        pipeline_name=build_data.pipeline_name,
        status=build_data.status,
        queued_at=build_data.queued_at,
        started_at=build_data.started_at,
        finished_at=build_data.finished_at,
        queue_time_seconds=build_data.queue_time_seconds,
        execution_time_seconds=build_data.execution_time_seconds,
        feedback_time_seconds=build_data.feedback_time_seconds,
        created_at=build_data.created_at or datetime.utcnow(),
    )
    db.add(db_build)
    db.commit()
    db.refresh(db_build)
    return db_build
