from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@asynccontextmanager
async def noop_lifespan(app):
    yield


@pytest.fixture()
def client():
    from app.main import app

    app.router.lifespan_context = noop_lifespan
    with TestClient(app) as c:
        yield c


def test_history_returns_200(client):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("app.main.async_session", return_value=mock_session):
        response = client.get("/history")

    assert response.status_code == 200
    assert response.json() == []


def test_history_accepts_limit_param(client):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("app.main.async_session", return_value=mock_session):
        response = client.get("/history?limit=10")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
