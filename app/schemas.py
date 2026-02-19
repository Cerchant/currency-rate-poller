from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ResponsePayload(BaseModel):
    received_at: datetime
    payload: dict[str, Any]


class HistoryItem(BaseModel):
    id: int
    requested_at: datetime
    method: str
    url: str
    query_params: dict[str, Any] | None
    timeout_seconds: int
    status_code: int | None
    error_type: str | None
    error_message: str | None
    response: ResponsePayload | None

    model_config = {"from_attributes": True}
