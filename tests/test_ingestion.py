"""Tests for the ingestion service.

Ensures that a BuildSchema can be ingested and stored correctly.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database import Base
from backend.app.services.ingestion_service import ingest_build
from backend.app.schemas.build import BuildSchema

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_ingest_build(db_session):
    # Prepare a sample BuildSchema
    build_data = BuildSchema(
        build_id="build_test_001",
        service_name="auth",
        pipeline_name="dev",
        status="success",
        queued_at=None,
        started_at=None,
        finished_at=None,
        queue_time_seconds=None,
        execution_time_seconds=None,
        feedback_time_seconds=None,
        created_at=None,
    )
    result = ingest_build(db_session, build_data)
    assert result.build_id == "build_test_001"
    # Verify it's persisted
    retrieved = db_session.query(result.__class__).filter_by(build_id="build_test_001").first()
    assert retrieved is not None
    assert retrieved.service_name == "auth"
