"""Parallelisation analysis & DAG critical path calculation service.

Analyses task dependency graphs using Directed Acyclic Graph (DAG) longest-path searching
to compute theoretical minimum execution bounds and identify parallelisation opportunities.

Algorithmic Complexity & Safety:
- Time Complexity: O(V + E) with memoization over task graph vertices V and dependency edges E.
- Error Boundaries: Returns default fallback dict (efficiency = 1.0) when tasks list is empty.
"""

from sqlalchemy.orm import Session
from ..models.task import Task
from typing import List, Dict, Any

def compute_critical_path(tasks: List[Task]) -> Dict[str, Any]:
    """Compute the critical path duration and dependency sequence using DAG analysis.

    Returns a dict with:
        - critical_path_duration: Float total duration of the longest dependency path
        - critical_path_tasks: List of task IDs along the critical path
        - total_sequential_duration: Sum of all task durations
        - parallel_efficiency: Ratio of critical path duration to total sequential duration
    """
    if not tasks:
        return {
            "critical_path_duration": 0.0,
            "critical_path_tasks": [],
            "total_sequential_duration": 0.0,
            "parallel_efficiency": 1.0,
        }

    task_map = {t.task_id: t for t in tasks}
    memo_durations: Dict[str, float] = {}
    memo_paths: Dict[str, List[str]] = {}

    def get_longest_path(task_id: str) -> tuple[float, List[str]]:
        if task_id in memo_durations:
            return memo_durations[task_id], memo_paths[task_id]

        task = task_map.get(task_id)
        duration = (task.duration_seconds or 0.0) if task else 0.0
        deps = (task.dependencies or []) if task else []

        max_dep_duration = 0.0
        max_dep_path: List[str] = []

        for dep_id in deps:
            if dep_id in task_map:
                dep_duration, dep_path = get_longest_path(dep_id)
                if dep_duration > max_dep_duration:
                    max_dep_duration = dep_duration
                    max_dep_path = dep_path

        total_duration = duration + max_dep_duration
        current_path = max_dep_path + [task_id]

        memo_durations[task_id] = total_duration
        memo_paths[task_id] = current_path
        return total_duration, current_path

    max_cp_duration = 0.0
    longest_cp_path: List[str] = []

    for t in tasks:
        dur, path = get_longest_path(t.task_id)
        if dur > max_cp_duration:
            max_cp_duration = dur
            longest_cp_path = path

    total_seq = sum(t.duration_seconds or 0.0 for t in tasks)
    efficiency = max_cp_duration / total_seq if total_seq > 0 else 1.0

    return {
        "critical_path_duration": max_cp_duration,
        "critical_path_tasks": longest_cp_path,
        "total_sequential_duration": total_seq,
        "parallel_efficiency": round(efficiency, 4),
    }

def detect_parallelisation_issues(db: Session, build_id: str) -> List[Dict[str, Any]]:
    """Analyze tasks for a build and return detected parallelisation opportunities."""
    tasks = db.query(Task).filter(Task.build_id == build_id).all()
    if not tasks or len(tasks) <= 1:
        return []

    cp_info = compute_critical_path(tasks)
    opportunities = []

    # If parallel efficiency is low (< 0.70), indicate potential sequential bottleneck
    if cp_info["parallel_efficiency"] < 0.70:
        opportunities.append({
            "type": "Parallelisation Opportunity",
            "description": f"Tasks in build {build_id} show low parallel efficiency ({cp_info['parallel_efficiency']:.2%}).",
            "critical_path_duration": cp_info["critical_path_duration"],
            "total_sequential_duration": cp_info["total_sequential_duration"],
            "suggestion": "Execute independent tasks in parallel to reduce overall build time.",
            "critical_path": cp_info["critical_path_tasks"],
        })

    return opportunities
