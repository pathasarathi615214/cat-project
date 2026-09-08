"""Synthetic CI data generator.

Creates CSV files under `data/raw/` to simulate builds, tasks, cache metrics,
queue metrics, and agent utilisation. Uses a fixed random seed for reproducibility.
"""

import csv
import random
from datetime import datetime, timedelta
import os

SEED = 42
random.seed(SEED)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

NUM_BUILDS = 200
NUM_TASKS_PER_BUILD = (5, 15)  # range

def generate_builds():
    builds = []
    for i in range(NUM_BUILDS):
        build_id = f"build_{i+1:04d}"
        service_name = random.choice(["auth", "payments", "orders", "notifications"])
        pipeline_name = random.choice(["dev", "staging", "prod"])
        status = random.choice(["success", "failed"])
        queued_at = datetime.utcnow() - timedelta(minutes=random.randint(10, 120))
        started_at = queued_at + timedelta(seconds=random.randint(30, 300))
        finished_at = started_at + timedelta(seconds=random.randint(60, 600))
        queue_time = (started_at - queued_at).total_seconds()
        exec_time = (finished_at - started_at).total_seconds()
        cache_hits = random.randint(0, 10)
        parallel_tasks = random.randint(1, 8)
        parallel_time = exec_time / random.uniform(1.0, parallel_tasks)
        builds.append([
            build_id, service_name, pipeline_name, status,
            queued_at.isoformat(), started_at.isoformat(), finished_at.isoformat(),
            queue_time, exec_time, cache_hits, parallel_tasks, parallel_time
        ])
    return builds

def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

if __name__ == "__main__":
    builds = generate_builds()
    write_csv(
        os.path.join(RAW_DIR, "ci_build_logs.csv"),
        ["build_id", "service_name", "pipeline_name", "status",
         "queued_at", "started_at", "finished_at",
         "queue_time_seconds", "execution_time_seconds",
         "cache_hits", "parallel_tasks", "parallel_time_seconds"],
        builds,
    )
    # Generate simple tasks data (one per build for illustration)
    tasks = []
    for b in builds:
        num_tasks = random.randint(*NUM_TASKS_PER_BUILD)
        for t in range(num_tasks):
            task_id = f"{b[0]}_task_{t+1}"
            duration = random.uniform(0.5, 5.0)
            tasks.append([b[0], task_id, duration])
    write_csv(
        os.path.join(RAW_DIR, "ci_task_timings.csv"),
        ["build_id", "task_id", "duration_seconds"],
        tasks,
    )
    # Cache metrics
    cache_rows = [[b[0], b[9]] for b in builds]
    write_csv(os.path.join(RAW_DIR, "cache_metrics.csv"), ["build_id", "cache_hits"], cache_rows)
    # Queue metrics
    queue_rows = [[b[0], b[7]] for b in builds]
    write_csv(os.path.join(RAW_DIR, "queue_metrics.csv"), ["build_id", "queue_time_seconds"], queue_rows)
    # Agent utilisation (random example)
    agents = []
    for i in range(5):
        agent_id = f"agent_{i+1}"
        utilisation = random.uniform(0.4, 0.95)
        agents.append([agent_id, utilisation])
    write_csv(os.path.join(RAW_DIR, "agent_utilisation.csv"), ["agent_id", "utilisation"], agents)
    print(f"Synthetic data generated in {RAW_DIR}")
