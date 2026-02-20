import logging
from datetime import datetime, timezone

import httpx

from app.config import settings
from app.db import async_session
from app.models import ApiRequest, ApiResponse

logger = logging.getLogger(__name__)

API_BASE_URL = "https://open.er-api.com/v6/latest"


async def fetch_rates() -> None:
    url = f"{API_BASE_URL}/{settings.base}"
    symbols = settings.symbols_list

    request_record = ApiRequest(
        requested_at=datetime.now(timezone.utc),
        method="GET",
        url=url,
        query_params={"base": settings.base, "symbols": ",".join(symbols)},
        timeout_seconds=settings.http_timeout_seconds,
    )

    async with async_session() as session:
        try:
            async with httpx.AsyncClient(timeout=settings.http_timeout_seconds) as client:
                resp = await client.get(url)
                resp.raise_for_status()

            payload = resp.json()
            request_record.status_code = resp.status_code

            all_rates = payload.get("rates")
            if not all_rates:
                request_record.error_type = "empty_response"
                request_record.error_message = "API returned response without rates"
                session.add(request_record)
                logger.warning("API response missing rates: %s", payload)
                await session.commit()
                return

            filtered_rates = {s: all_rates[s] for s in symbols if s in all_rates}
            filtered_payload = {
                "base": payload.get("base_code", settings.base),
                "rates": filtered_rates,
            }

            session.add(request_record)
            await session.flush()

            response_record = ApiResponse(
                request_id=request_record.id,
                received_at=datetime.now(timezone.utc),
                payload=filtered_payload,
            )
            session.add(response_record)
            logger.info(
                "Rates fetched successfully: status=%d, rates_count=%d",
                resp.status_code,
                len(filtered_rates),
            )

        except httpx.TimeoutException as exc:
            request_record.error_type = "timeout"
            request_record.error_message = str(exc)
            session.add(request_record)
            logger.error("Timeout fetching rates from %s: %s", url, exc)

        except httpx.ConnectError as exc:
            request_record.error_type = "connection_error"
            request_record.error_message = str(exc)
            session.add(request_record)
            logger.error("Connection error fetching rates: %s", exc)

        except httpx.HTTPStatusError as exc:
            request_record.status_code = exc.response.status_code
            request_record.error_type = "http_error"
            request_record.error_message = str(exc)
            session.add(request_record)
            logger.error("HTTP %d error: %s", exc.response.status_code, exc)

        except Exception as exc:
            request_record.error_type = "unknown"
            request_record.error_message = str(exc)
            session.add(request_record)
            logger.error("Unexpected error fetching rates: %s", exc)

        await session.commit()
