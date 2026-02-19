import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload

from app.db import async_session, engine
from app.logging_setup import setup_logging
from app.models import ApiRequest
from app.scheduler import start_scheduler, stop_scheduler
from app.schemas import HistoryItem

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


@app.get("/history", response_model=list[HistoryItem])
async def get_history(limit: int = Query(default=50, ge=1, le=1000)):
    async with async_session() as session:
        stmt = (
            select(ApiRequest)
            .options(selectinload(ApiRequest.response))
            .order_by(ApiRequest.requested_at.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        records = result.scalars().all()
    return records
