"""SQLAlchemy model for CI agents (CI runners)."""

from sqlalchemy import Column, Integer, String, DateTime, Float
from ..database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, unique=True, index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    cpu_utilisation = Column(Float, nullable=True)
    memory_utilisation = Column(Float, nullable=True)
    active_jobs = Column(Integer, nullable=True)
    queue_length = Column(Integer, nullable=True)
    availability_status = Column(String, nullable=True)
