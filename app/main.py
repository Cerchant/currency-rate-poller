import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.db import engine
from app.logging_setup import setup_logging
from app.scheduler import start_scheduler, stop_scheduler

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    logger.info("Database connection OK")
    start_scheduler()
    yield
    stop_scheduler()
    await engine.dispose()


app = FastAPI(title="Currency Rate Poller", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}
