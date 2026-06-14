from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from src.config.logging import get_logger

logger = get_logger(__name__)

class ProjectTask(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    milestone_id: uuid.UUID
    title: str
    description: str
    status: str = "todo"
    dependencies: List[uuid.UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskDecomposer(BaseModel):
    model_config = {"from_attributes": True}
    
    async def decompose_milestone(self, milestone_id: uuid.UUID, description: str) -> List[ProjectTask]:
        logger.info(f"Decomposing milestone {milestone_id} into tasks")
        tasks = [
            ProjectTask(milestone_id=milestone_id, title="Task 1", description="First step"),
            ProjectTask(milestone_id=milestone_id, title="Task 2", description="Second step")
        ]
        return tasks
