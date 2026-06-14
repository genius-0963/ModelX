from __future__ import annotations
import asyncio
import time
from datetime import datetime, timezone
from pydantic import BaseModel
from src.config.logging import get_logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = get_logger(__name__)

class WorkerMetrics(BaseModel):
    jobs_submitted: int
    jobs_completed: int
    duration_sec: float
    throughput_per_sec: float
    model_config = {"from_attributes": True}

class WorkerStressTester:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.completed = 0

    async def dummy_job(self) -> None:
        # Extremely fast dummy job
        await asyncio.sleep(0.001)
        self.completed += 1

    async def run_stress_test(self, job_count: int = 1000) -> WorkerMetrics:
        logger.info(f"Loading APScheduler with {job_count} jobs...")
        self.scheduler.start()
        start_time = time.perf_counter()

        # Schedule all jobs as quickly as possible
        now = datetime.now(timezone.utc)
        for _ in range(job_count):
            self.scheduler.add_job(self.dummy_job, 'date', run_date=now)

        # Wait for completion
        while self.completed < job_count:
            await asyncio.sleep(0.1)

        duration = time.perf_counter() - start_time
        self.scheduler.shutdown()

        return WorkerMetrics(
            jobs_submitted=job_count,
            jobs_completed=self.completed,
            duration_sec=duration,
            throughput_per_sec=job_count / duration if duration > 0 else 0.0
        )
