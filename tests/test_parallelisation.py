"""Unit tests for DAG critical path solver and parallelisation analysis."""

from backend.app.models.task import Task
from backend.app.services.parallelisation_service import compute_critical_path

def test_critical_path_linear():
    t1 = Task(task_id="t1", build_id="b1", task_name="checkout", task_type="build", duration_seconds=10.0, status="success", dependencies=[])
    t2 = Task(task_id="t2", build_id="b1", task_name="compile", task_type="build", duration_seconds=20.0, status="success", dependencies=["t1"])
    t3 = Task(task_id="t3", build_id="b1", task_name="test", task_type="test", duration_seconds=30.0, status="success", dependencies=["t2"])

    res = compute_critical_path([t1, t2, t3])
    assert res["critical_path_duration"] == 60.0
    assert res["critical_path_tasks"] == ["t1", "t2", "t3"]
    assert res["parallel_efficiency"] == 1.0

def test_critical_path_branching():
    # t1 -> t2 -> t4 (10 + 20 + 5 = 35)
    # t1 -> t3 -> t4 (10 + 40 + 5 = 55) <- Critical Path
    t1 = Task(task_id="t1", build_id="b2", task_name="setup", task_type="build", duration_seconds=10.0, status="success", dependencies=[])
    t2 = Task(task_id="t2", build_id="b2", task_name="unit-tests", task_type="test", duration_seconds=20.0, status="success", dependencies=["t1"])
    t3 = Task(task_id="t3", build_id="b2", task_name="int-tests", task_type="test", duration_seconds=40.0, status="success", dependencies=["t1"])
    t4 = Task(task_id="t4", build_id="b2", task_name="deploy", task_type="deploy", duration_seconds=5.0, status="success", dependencies=["t2", "t3"])

    res = compute_critical_path([t1, t2, t3, t4])
    assert res["critical_path_duration"] == 55.0
    assert res["critical_path_tasks"] == ["t1", "t3", "t4"]
    assert res["total_sequential_duration"] == 75.0
    assert res["parallel_efficiency"] < 1.0
