"""Service that analyses builds and detects bottlenecks.

Implements rule‑based detection using thresholds defined in
`backend/app/rules/thresholds.py`.
"""

from sqlalchemy.orm import Session
from ..models.build import Build
from ..models.task import Task
from ..models.agent import Agent
from ..models.recommendation import Recommendation
from ..schemas.analysis import AnalysisResultSchema, BottleneckDetail
from ..rules.thresholds import (
    QUEUE_TIME_THRESHOLD,
    EXECUTION_TIME_THRESHOLD,
    CACHE_HIT_RATE_THRESHOLD,
    AGENT_UTILISATION_THRESHOLD,
    PARALLELISATION_EFFICIENCY_THRESHOLD,
)
from datetime import datetime

def analyze_builds(db: Session) -> AnalysisResultSchema:
    """Run analysis on all builds and store recommendations.

    Returns a summary for the most recent build (or the first if none).
    """
    builds = db.query(Build).all()
    if not builds:
        raise ValueError("No builds available for analysis")

    # For simplicity, analyse the latest build by creation time
    latest_build = max(builds, key=lambda b: b.created_at or datetime.min)
    bottlenecks = []

    # Queue time bottleneck
    if latest_build.queue_time_seconds and latest_build.queue_time_seconds > QUEUE_TIME_THRESHOLD:
        bottlenecks.append(
            BottleneckDetail(
                type="Queue Time",
                description=f"Build spent {latest_build.queue_time_seconds:.1f}s in queue",
                severity="high",
                suggestion="Investigate upstream resource contention or increase parallel agents.",
                evidence={"queue_time_seconds": latest_build.queue_time_seconds},
            )
        )

    # Execution time bottleneck – check tasks associated with this build
    tasks = db.query(Task).filter(Task.build_id == latest_build.build_id).all()
    slow_tasks = [t for t in tasks if t.duration_seconds and t.duration_seconds > EXECUTION_TIME_THRESHOLD]
    for t in slow_tasks:
        bottlenecks.append(
            BottleneckDetail(
                type="Slow Task",
                description=f"Task {t.task_name} took {t.duration_seconds:.1f}s",
                severity="medium",
                suggestion="Profile the task; consider caching or parallelisation.",
                evidence={"task_id": t.task_id, "duration_seconds": t.duration_seconds},
            )
        )

    # Cache utilisation bottleneck – compute hit rate per build (simplified)
    cache_hits = sum(1 for t in tasks if t.cache_hit)
    cache_total = len(tasks)
    if cache_total > 0:
        hit_rate = cache_hits / cache_total
        if hit_rate < CACHE_HIT_RATE_THRESHOLD:
            bottlenecks.append(
                BottleneckDetail(
                    type="Cache Utilisation",
                    description=f"Cache hit rate {hit_rate:.2%} is below threshold",
                    severity="medium",
                    suggestion="Enable more aggressive caching for repeated steps.",
                    evidence={"hit_rate": hit_rate, "threshold": CACHE_HIT_RATE_THRESHOLD},
                )
            )

    # Agent utilisation bottleneck
    agents = db.query(Agent).all()
    if agents:
        avg_util = sum(a.cpu_utilisation or 0 for a in agents) / len(agents)
        if avg_util < AGENT_UTILISATION_THRESHOLD:
            bottlenecks.append(
                BottleneckDetail(
                    type="Agent Utilisation",
                    description=f"Average agent CPU utilisation {avg_util:.2%}",
                    severity="low",
                    suggestion="Add more agents or increase parallelism.",
                    evidence={"average_cpu_util": avg_util},
                )
            )

    # Parallelisation inefficiency – very simple heuristic: many tasks sequentially with same start time
    # (Placeholder for real analysis)
    # ... omitted for brevity ...

    # Store recommendations based on detected bottlenecks
    for b in bottlenecks:
        rec = Recommendation(
            build_id=latest_build.build_id,
            recommendation_type=b.type,
            priority=b.severity,
            priority_score=1.0,  # placeholder
            confidence_score=0.9,
            estimated_saving_seconds=0.0,
            title=b.description,
            description=b.suggestion,
            evidence_json=b.evidence,
            created_at=datetime.utcnow(),
        )
        db.add(rec)
    db.commit()

    result = AnalysisResultSchema(
        build_id=latest_build.build_id,
        bottlenecks=bottlenecks,
        overall_score=0.0,  # placeholder
        generated_at=datetime.utcnow().isoformat(),
    )
    return result
