from __future__ import annotations

from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.schemas.capability import CapabilityCreate, CapabilityInDB, CapabilityUpdate
from src.config.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/capabilities", tags=["Capabilities"])

async def get_db_session():
    yield None

@router.post("/", response_model=CapabilityInDB, status_code=status.HTTP_201_CREATED)
async def create_capability(
    capability_in: CapabilityCreate,
    session: Any = Depends(get_db_session)
) -> CapabilityInDB:
    logger.info(f"Creating capability {capability_in.name}")
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/", response_model=List[CapabilityInDB])
async def list_capabilities(
    skip: int = 0,
    limit: int = 100,
    session: Any = Depends(get_db_session)
) -> List[CapabilityInDB]:
    logger.info(f"Listing capabilities skip={skip} limit={limit}")
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/{capability_id}", response_model=CapabilityInDB)
async def get_capability(
    capability_id: UUID,
    session: Any = Depends(get_db_session)
) -> CapabilityInDB:
    logger.info(f"Fetching capability {capability_id}")
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.patch("/{capability_id}", response_model=CapabilityInDB)
async def update_capability(
    capability_id: UUID,
    capability_update: CapabilityUpdate,
    session: Any = Depends(get_db_session)
) -> CapabilityInDB:
    logger.info(f"Updating capability {capability_id}")
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.delete("/{capability_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_capability(
    capability_id: UUID,
    session: Any = Depends(get_db_session)
) -> None:
    logger.info(f"Deleting capability {capability_id}")
    raise HTTPException(status_code=501, detail="Not Implemented")
