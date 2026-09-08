from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.build import Build
from ..schemas.build import BuildSchema
from ..services.ingestion_service import ingest_build

router = APIRouter()

@router.post("/", response_model=BuildSchema, status_code=status.HTTP_201_CREATED)
def create_build(build: BuildSchema, db: Session = Depends(get_db)):
    existing = db.query(Build).filter(Build.build_id == build.build_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Build ID already exists")
    created = ingest_build(db, build)
    return created

@router.get("/", response_model=list[BuildSchema])
def list_builds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    builds = db.query(Build).offset(skip).limit(limit).all()
    return builds

@router.get("/{build_id}", response_model=BuildSchema)
def get_build(build_id: str, db: Session = Depends(get_db)):
    build = db.query(Build).filter(Build.build_id == build_id).first()
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    return build
