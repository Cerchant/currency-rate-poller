FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY app/ app/

RUN pip install --no-cache-dir .

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
