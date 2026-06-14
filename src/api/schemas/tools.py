from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel

class CapabilityGapBase(BaseModel):
    goal: str
    identified_gap: str
    status: str

class CapabilityGapCreate(CapabilityGapBase):
    pass

class CapabilityGapResponse(CapabilityGapBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ToolBase(BaseModel):
    name: str
    description: Optional[str] = None

class ToolCreate(ToolBase):
    pass

class ToolResponse(ToolBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ToolVersionBase(BaseModel):
    tool_id: UUID
    version_number: str
    code: str
    status: str

class ToolVersionCreate(ToolVersionBase):
    pass

class ToolVersionResponse(ToolVersionBase):
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}

class ToolExecutionBase(BaseModel):
    tool_version_id: UUID
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    success: bool
    error_message: Optional[str] = None
    execution_time_ms: Optional[int] = None

class ToolExecutionCreate(ToolExecutionBase):
    pass

class ToolExecutionResponse(ToolExecutionBase):
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}

class ToolBenchmarkBase(BaseModel):
    tool_version_id: UUID
    benchmark_name: str
    score: float
    details: Optional[Dict[str, Any]] = None

class ToolBenchmarkCreate(ToolBenchmarkBase):
    pass

class ToolBenchmarkResponse(ToolBenchmarkBase):
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
