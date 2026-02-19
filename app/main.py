from fastapi import FastAPI

app = FastAPI(title="Currency Rate Poller")


@app.get("/health")
async def health():
    return {"status": "ok"}
