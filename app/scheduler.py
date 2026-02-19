import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import settings
from app.service import fetch_rates

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def start_scheduler() -> None:
    scheduler.add_job(
        fetch_rates,
        "interval",
        minutes=settings.poll_interval_minutes,
        id="fetch_rates",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started, polling every %d min", settings.poll_interval_minutes)


def stop_scheduler() -> None:
    scheduler.shutdown(wait=False)
    logger.info("Scheduler stopped")
