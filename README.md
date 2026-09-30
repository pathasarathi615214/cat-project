# CI Bottleneck Analyzer

## Overview

This project provides a **FastAPI** backend that ingests CI build data, analyses it for bottlenecks, and exposes metrics and recommendations.  A **Streamlit** frontend visualises dashboards, build analysis, recommendations, experiments, legacy migration demos, and error analysis.

## Features

- Synthetic data generator for builds, tasks, cache, queue, and agent utilisation.
- Automated bottleneck detection based on configurable thresholds.
- Recommendations engine storing actionable insights.
- Metrics service exposing cache hit rate, parallel efficiency, queue statistics.
- Experiments API to track CI optimisation trials.
- Interactive dashboards with navigation.
- Dockerised deployment (backend + frontend).

## Quick Start (Local Development)

```bash
# Clone the repository (if not already done)
git clone <repo-url>
cd cat-project

# Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Generate synthetic data
python data/generators/generate_ci_data.py

# Run the FastAPI backend
uvicorn backend.app.main:app --reload

# In another terminal, launch the Streamlit UI
streamlit run frontend/app.py
```

The UI will be available at `http://localhost:8501` and the API at `http://localhost:8000`.

## Docker Deployment

```bash
docker-compose up --build
```

- Backend runs on port **8000**.
- Streamlit dashboard runs on port **8501**.

## Database Schema Reference

The system uses SQLAlchemy ORM backed by SQLite (`ci_bottleneck.db`).

| Model | Table Name | Columns | Description |
| :--- | :--- | :--- | :--- |
| **`Build`** | `builds` | `id` (PK), `build_id` (Unique), `service_name`, `pipeline_name`, `status`, `queued_at`, `started_at`, `finished_at`, `queue_time_seconds`, `execution_time_seconds`, `feedback_time_seconds`, `created_at` | Stores overall CI build runs and operational timing milestones. |
| **`Task`** | `tasks` | `id` (PK), `task_id` (Unique), `build_id` (FK/Index), `task_name`, `task_type`, `started_at`, `finished_at`, `duration_seconds`, `cache_hit`, `dependencies` (JSON), `status` | Stores granular pipeline step executions and task dependency lists for DAG analysis. |
| **`Agent`** | `agents` | `id` (PK), `agent_id` (Unique), `cpu_utilisation`, `memory_utilisation_mb` | Tracks build runner node CPU usage and RAM saturation / OOM risks. |
| **`Recommendation`** | `recommendations` | `id` (PK), `build_id`, `recommendation_type`, `priority`, `priority_score`, `confidence_score`, `estimated_saving_seconds`, `title`, `description`, `evidence_json`, `created_at` | Stores system-generated optimization recommendations and evidence payloads. |

---

## REST API Endpoints Reference

The FastAPI backend exposes the following REST API endpoints:

| Method | Endpoint Path | Description | Expected Status Codes |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Application health check monitor | `200 OK` |
| `GET` | `/builds` | Query paginated CI builds (`?skip=0&limit=100`) | `200 OK` |
| `GET` | `/builds/{build_id}` | Fetch detailed build record by ID | `200 OK`, `404 Not Found` |
| `POST` | `/builds` | Ingest new build run payload | `201 Created`, `400 Bad Request`, `422 Unprocessable Entity` |
| `GET` | `/metrics` | Fetch aggregated metrics (cache hit rate, parallel efficiency, queue stats) | `200 OK` |
| `POST` | `/analysis/run` | Trigger bottleneck analysis run across builds | `202 Accepted`, `500 Internal Error` |
| `GET` | `/recommendations/{build_id}` | Fetch generated optimization recommendations for a build | `200 OK`, `404 Not Found` |
| `POST` | `/experiments` | Create new CI optimization experiment | `201 Created`, `500 Internal Error` |
| `GET` | `/experiments/{build_id}` | Retrieve experiment results for a build | `200 OK`, `404 Not Found` |
| `POST` | `/webhooks/github` | Webhook stub parsing GitHub Actions `workflow_run` events | `201 Created`, `400 Bad Request` |
| `POST` | `/webhooks/gitlab` | Webhook stub parsing GitLab CI pipeline events | `201 Created`, `400 Bad Request` |

---

## Technical Documentation: Unit Testing & Error Boundaries

### 1. Error Handling Boundaries & Safeguards
- **Validation Bounds (HTTP 422 / 400)**: All input endpoints enforce Pydantic type validation. Malformed payloads or missing required fields return HTTP 422/400 without corrupting database state.
- **Resource Check Isolation (HTTP 404)**: Queries for non-existent builds or recommendations return explicit 404 responses with detailed error messages.
- **DAG Algorithm Safety**: The critical path graph solver (`compute_critical_path`) utilizes memoized depth-first traversal with default fallback values (efficiency = 1.0, duration = 0.0) for isolated tasks or empty dependency lists, preventing infinite loops or recursion errors.
- **Attribute Access Boundaries**: Metrics aggregation functions (`cache_hit_rate`, `parallel_efficiency`) inspect model attributes using `hasattr()` before access, preventing dynamic schema runtime exceptions (`AttributeError`).

### 2. Unit Testing Strategy
Run unit tests with pytest or Python module runner:

```bash
# Run tests via pytest
pytest

# Alternative test execution via Python
python -c "import tests.test_parallelisation as tp; tp.test_critical_path_linear(); tp.test_critical_path_branching()"
```

- **[tests/test_ingestion.py](file:///c:/Users/HP/Desktop/cat-project/tests/test_ingestion.py)**: Validates build payload parsing and timing metric auto-calculation.
- **[tests/test_parallelisation.py](file:///c:/Users/HP/Desktop/cat-project/tests/test_parallelisation.py)**: Validates DAG critical path duration calculations across linear and branching task graphs.

---

## Project Structure

```
cat-project/
├─ backend/
│  ├─ app/
│  │  ├─ api/            # FastAPI routers (builds, metrics, analysis, recommendations, experiments, webhooks)
│  │  ├─ models/         # SQLAlchemy models (Build, Task, Agent, Recommendation)
│  │  ├─ schemas/        # Pydantic schemas
│  │  ├─ services/       # Business logic & DAG critical path solver
│  │  ├─ rules/          # Threshold definitions
│  │  ├─ database.py
│  │  ├─ config.py
│  │  └─ main.py
├─ data/
│  ├─ generators/        # Synthetic data generator
│  └─ raw/               # Generated CSV files
├─ docs/                  # Architecture, requirements, user flow, etc.
├─ frontend/
│  ├─ app.py             # Streamlit entry point
│  └─ pages/             # Individual UI pages
├─ tests/                 # Pytest suite
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
└─ README.md
```

## Configuration

Create a `.env` file (copy from `.env.example`) and set `DB_URL` to your SQLite path, e.g.:

```env
DB_URL=sqlite:///./ci_bottleneck.db
```

---

Enjoy analysing your CI pipelines!
