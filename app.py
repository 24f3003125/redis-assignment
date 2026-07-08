import os

import redis
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# REDIS_URL environment se aayega.
#   Render + Key Value -> wo internal redis:// URL jo tumne copy kiya
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)


@app.get("/healthz")
def healthz():
    try:
        r.ping()                       # actually Redis ko ping karo
        return {"status": "ok", "redis": "up"}
    except Exception:
        return JSONResponse(
            status_code=503, content={"status": "error", "redis": "down"}
        )


@app.post("/hit/{key}")
def hit(key: str):
    count = r.incr(f"count:{key}")     # atomic INCR
    return {"key": key, "count": count}


@app.get("/count/{key}")
def count(key: str):
    val = r.get(f"count:{key}")
    return {"key": key, "count": int(val) if val is not None else 0}
