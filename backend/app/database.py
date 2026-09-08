"""Database connection and session handling for the CI Bottleneck Analyser.

Uses SQLAlchemy 2.x style ``create_engine`` and ``sessionmaker``.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DB_URL

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """Yield a SQLAlchemy session. To be used with FastAPI ``Depends``.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
