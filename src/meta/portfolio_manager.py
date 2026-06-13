"""Research Portfolio Manager."""

from __future__ import annotations

import logging
from uuid import UUID

from src.db.models import ResearchPortfolio, ResearchTrack
from src.db.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class PortfolioManager:
    """Tracks and manages active research investigations across portfolios."""

    def __init__(
        self,
        portfolio_repo: BaseRepository[ResearchPortfolio],
        track_repo: BaseRepository[ResearchTrack],
    ) -> None:
        self.portfolio_repo = portfolio_repo
        self.track_repo = track_repo

    async def get_or_create_portfolio(self, name: str, description: str) -> ResearchPortfolio:
        """Fetch an existing portfolio or create a new one."""
        # Note: A real implementation would use a specialized repo method to query by name
        # For this prototype, we'll just create it.
        try:
            return await self.portfolio_repo.create(
                name=name,
                description=description,
                status="active",
                overall_progress=0.0
            )
        except Exception:
            logger.warning(f"Portfolio {name} might already exist or creation failed.")
            raise

    async def update_portfolio_progress(self, portfolio_id: UUID) -> ResearchPortfolio | None:
        """
        Recalculate the overall progress of a portfolio based on its constituent tracks.
        """
        # In a complete implementation, this would query all tracks associated with the portfolio
        # (Assuming we added a foreign key from ResearchTrack -> ResearchPortfolio, 
        # though the spec didn't strictly require it, we'd calculate the average).
        # We will mock the calculation for now.
        logger.info(f"Updating progress for portfolio {portfolio_id}")
        
        # Mocking an update
        portfolio = await self.portfolio_repo.update(portfolio_id, overall_progress=0.5)
        return portfolio

    async def get_dashboard_summary(self) -> dict[str, Any]:
        """Generate a summary of all active portfolios."""
        # Simple mock response
        return {
            "active_portfolios": 3,
            "portfolios": [
                {"name": "Memory Research", "progress": 83.0},
                {"name": "Reasoning Research", "progress": 41.0},
                {"name": "Planning Research", "progress": 12.0},
            ]
        }
