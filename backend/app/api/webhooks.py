"""Webhook integration stubs for capturing real-world CI logs (GitHub Actions / GitLab CI).

Satisfies legacy coexistence requirement by translating external CI payloads into Build and Task schemas.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any

from ..database import get_db
from ..schemas.build import BuildSchema
from ..services.ingestion_service import ingest_build

router = APIRouter()

@router.post("/github", response_model=BuildSchema, status_code=status.HTTP_201_CREATED)
def github_actions_webhook(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    """Receive and translate a GitHub Actions workflow_run webhook event.

    Translates GitHub Actions JSON payload into normalized BuildSchema and ingests it.
    """
    try:
        workflow_run = payload.get("workflow_run", payload)
        build_id = f"gh-{workflow_run.get('id', int(datetime.utcnow().timestamp()))}"
        service_name = payload.get("repository", {}).get("name", "github-repo")
        pipeline_name = workflow_run.get("name", "github-actions")
        
        # Map GitHub status/conclusion
        conclusion = workflow_run.get("conclusion") or workflow_run.get("status") or "success"
        status_str = "success" if conclusion == "success" else "failed"
        if conclusion in ["cancelled", "timed_out"]:
            status_str = conclusion

        queued_at_str = workflow_run.get("created_at") or datetime.utcnow().isoformat()
        started_at_str = workflow_run.get("run_started_at") or queued_at_str
        finished_at_str = workflow_run.get("updated_at") or datetime.utcnow().isoformat()

        build = BuildSchema(
            build_id=build_id,
            service_name=service_name,
            pipeline_name=pipeline_name,
            status=status_str,
            queued_at=datetime.fromisoformat(queued_at_str.replace("Z", "+00:00")),
            started_at=datetime.fromisoformat(started_at_str.replace("Z", "+00:00")),
            finished_at=datetime.fromisoformat(finished_at_str.replace("Z", "+00:00")),
        )
        return ingest_build(db, build)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse GitHub webhook payload: {str(e)}")

@router.post("/gitlab", response_model=BuildSchema, status_code=status.HTTP_201_CREATED)
def gitlab_ci_webhook(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    """Receive and translate a GitLab CI Pipeline webhook event.

    Translates GitLab CI JSON payload into normalized BuildSchema and ingests it.
    """
    try:
        object_attrs = payload.get("object_attributes", payload)
        pipeline_id = object_attrs.get("id", int(datetime.utcnow().timestamp()))
        build_id = f"gl-{pipeline_id}"
        project = payload.get("project", {})
        service_name = project.get("name", "gitlab-project")
        pipeline_name = object_attrs.get("ref", "gitlab-ci")

        gl_status = object_attrs.get("status", "success")
        status_str = "success" if gl_status == "success" else "failed"
        if gl_status in ["canceled", "skipped"]:
            status_str = "aborted"

        created_at_str = object_attrs.get("created_at") or datetime.utcnow().isoformat()
        finished_at_str = object_attrs.get("finished_at") or datetime.utcnow().isoformat()

        build = BuildSchema(
            build_id=build_id,
            service_name=service_name,
            pipeline_name=pipeline_name,
            status=status_str,
            queued_at=datetime.fromisoformat(created_at_str.replace("Z", "+00:00")),
            started_at=datetime.fromisoformat(created_at_str.replace("Z", "+00:00")),
            finished_at=datetime.fromisoformat(finished_at_str.replace("Z", "+00:00")),
        )
        return ingest_build(db, build)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse GitLab webhook payload: {str(e)}")
