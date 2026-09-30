"""FastAPI entry point for CI Bottleneck Analyzer.

Includes routers for builds, analysis, recommendations, metrics, and experiments.
"""

import uvicorn
from fastapi import FastAPI
from .config import DB_URL
from .database import Base, engine
from .api import builds, analysis, recommendations, metrics, experiments, webhooks

app = FastAPI(title="CI Bottleneck Analyser")

# Include routers
app.include_router(builds.router, prefix="/builds", tags=["Builds"])
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
app.include_router(experiments.router, prefix="/experiments", tags=["Experiments"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])

# Create tables on startup
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health", tags=["Health"]) 
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
