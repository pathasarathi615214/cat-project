"""Service for exposing performance metrics.

Provides functions to compute cache hit rate and parallelisation efficiency.
"""

from sqlalchemy.orm import Session
from ..models.build import Build
from typing import Dict

def cache_hit_rate(db: Session) -> float:
    """Calculate cache hit rate across all builds/tasks.

    Returns a value between 0 and 1.
    """
    if hasattr(Build, "cache_hits"):
        total = db.query(Build).count()
        if total == 0:
            return 0.0
        hits = db.query(Build).filter(getattr(Build, "cache_hits") > 0).count()
        return hits / total
    else:
        from ..models.task import Task
        total = db.query(Task).count()
        if total == 0:
            return 0.0
        hits = db.query(Task).filter(Task.cache_hit == True).count()
        return hits / total

def parallel_efficiency(db: Session) -> float:
    """Compute average parallelisation efficiency.

    Efficiency is defined as (actual_parallel_time / theoretical_parallel_time).
    Returns a value between 0 and 1 where higher is better.
    """
    if hasattr(Build, "parallel_tasks"):
        builds = db.query(Build).filter(getattr(Build, "parallel_tasks") > 0).all()
        if not builds:
            return 0.0
        efficiencies = []
        for b in builds:
            pt = getattr(b, "parallel_tasks", None)
            td = getattr(b, "total_duration_seconds", None)
            ps = getattr(b, "parallel_time_seconds", None)
            if pt and td:
                theoretical = td / pt
                actual = ps or td
                if theoretical > 0:
                    efficiencies.append(min(actual / theoretical, 1.0))
        if not efficiencies:
            return 0.0
        return sum(efficiencies) / len(efficiencies)
    else:
        return 0.0

def overall_metrics(db: Session) -> Dict[str, float]:
    """Return a dictionary of key performance metrics."""
    return {
        "cache_hit_rate": cache_hit_rate(db),
        "parallel_efficiency": parallel_efficiency(db),
    }
