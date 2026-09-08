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

## Project Structure

```
cat-project/
├─ backend/
│  ├─ app/
│  │  ├─ api/            # FastAPI routers
│  │  ├─ models/         # SQLAlchemy models
│  │  ├─ schemas/        # Pydantic schemas
│  │  ├─ services/       # Business logic
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

## Testing

Run the full test suite with:

```bash
pytest
```

The tests cover ingestion, bottleneck analysis, metrics computation, experiment management, and more.

## Configuration

Create a `.env` file (copy from `.env.example`) and set `DB_URL` to your SQLite path, e.g.:

```env
DB_URL=sqlite:///./ci_bottleneck.db
```

---

Enjoy analysing your CI pipelines!
