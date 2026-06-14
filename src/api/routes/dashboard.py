from __future__ import annotations

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.config.logging import get_logger
from src.api.schemas.dashboard import DashboardMetrics, ChartDataPoint

logger = get_logger(__name__)
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/overview", response_model=DashboardMetrics)
async def get_dashboard_overview() -> DashboardMetrics:
    """Get dashboard overview metrics."""
    logger.info("Fetching dashboard overview")
    raise HTTPException(status_code=501, detail="Not implemented")

@router.get("/charts", response_model=List[ChartDataPoint])
async def get_dashboard_charts() -> List[ChartDataPoint]:
    """Get data points for dashboard charts."""
    logger.info("Fetching dashboard charts")
    return []
