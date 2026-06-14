from __future__ import annotations

from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from src.config.logging import get_logger
from src.api.schemas.projects import ProjectCreate, ProjectResponse, TaskCreate, TaskResponse

logger = get_logger(__name__)
router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(project: ProjectCreate):
    logger.info(f"Creating project: {project.name}")
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: UUID):
    logger.info(f"Fetching project: {project_id}")
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.get("/", response_model=List[ProjectResponse])
async def list_projects():
    logger.info("Listing projects")
    return []

@router.post("/{project_id}/tasks", response_model=TaskResponse, status_code=201)
async def create_task(project_id: UUID, task: TaskCreate):
    logger.info(f"Creating task for project: {project_id}")
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.get("/{project_id}/tasks", response_model=List[TaskResponse])
async def list_tasks(project_id: UUID):
    logger.info(f"Listing tasks for project: {project_id}")
    return []
