# Currency Rate Poller

Микросервис на FastAPI для периодического опроса курсов валют через внешний API ([open.er-api.com](https://open.er-api.com/)) и сохранения истории запросов в PostgreSQL.

## Стек технологий

- Python 3.11
- FastAPI + Uvicorn
- httpx (async HTTP-клиент)
- SQLAlchemy 2.x (async engine + asyncpg)
- Alembic (миграции)
- APScheduler (периодические задачи)
- Pydantic Settings (конфигурация)
- PostgreSQL 15
- Docker / Docker Compose

## Быстрый старт

1. Клонируйте репозиторий:

```bash
git clone <url>
cd currency-rate-poller
```

2. Создайте файл `.env` на основе примера:

```bash
cp .env.example .env
```

3. Запустите через Docker Compose:

```bash
docker-compose up --build
```

Приложение будет доступно на `http://localhost:8000`.

## Конфигурация

Через `.env` файл:

| Переменная             | Описание                       | По умолчанию |
|------------------------|--------------------------------|--------------|
| DATABASE_URL           | Строка подключения к БД        | —            |
| POLL_INTERVAL_MINUTES  | Интервал опроса (мин)          | 10           |
| BASE                   | Базовая валюта                 | USD          |
| SYMBOLS                | Целевые валюты (через запятую) | EUR,RUB      |
| HTTP_TIMEOUT_SECONDS   | Таймаут HTTP-запроса (сек)     | 5            |
| LOG_LEVEL              | Уровень логирования            | INFO         |

Пример `.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/currency_db
POLL_INTERVAL_MINUTES=10
BASE=USD
SYMBOLS=EUR,RUB
HTTP_TIMEOUT_SECONDS=5
LOG_LEVEL=INFO
```

## API

### GET /history

Возвращает историю запросов к API курсов валют.

**Параметры:**

- `limit` (int, по умолчанию 50) — количество записей (от 1 до 1000)

**Пример запроса:**

```bash
curl http://localhost:8000/history
curl http://localhost:8000/history?limit=10
```

**Пример ответа:**

```json
[
  {
    "id": 1,
    "requested_at": "2026-02-20T10:00:00Z",
    "method": "GET",
    "url": "https://open.er-api.com/v6/latest/USD",
    "query_params": {"base": "USD", "symbols": "EUR,RUB"},
    "timeout_seconds": 5,
    "status_code": 200,
    "error_type": null,
    "error_message": null,
    "response": {
      "received_at": "2026-02-20T10:00:01Z",
      "payload": {"base": "USD", "rates": {"EUR": 0.92, "RUB": 96.5}}
    }
  }
]
```

### GET /health

Проверка работоспособности сервиса.

## SQL-запрос для ручной проверки

```sql
SELECT
    r.requested_at,
    r.url,
    r.status_code,
    resp.payload -> 'rates' ->> 'EUR' AS eur_rate,
    resp.payload -> 'rates' ->> 'RUB' AS rub_rate
FROM api_requests r
LEFT JOIN api_responses resp
    ON resp.request_id = r.id
ORDER BY r.requested_at DESC
LIMIT 50;
```

## Тесты

```bash
pip install ".[dev]"
pytest tests/ -v
```

## Линтинг

```bash
black app/ tests/
ruff check app/ tests/
```
