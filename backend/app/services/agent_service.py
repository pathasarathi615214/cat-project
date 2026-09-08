"""Service for agent registration and lookup.

Provides functions to add new CI agents and retrieve agent info.
"""

from sqlalchemy.orm import Session
from ..models.agent import Agent
from ..schemas.agent import AgentSchema
from typing import Optional

def register_agent(db: Session, name: str, version: str) -> Agent:
    """Create and persist a new Agent entry."""
    agent = Agent(name=name, version=version)
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

def get_agent(db: Session, agent_id: int) -> Optional[Agent]:
    """Retrieve an Agent by its primary key."""
    return db.query(Agent).filter(Agent.id == agent_id).first()
