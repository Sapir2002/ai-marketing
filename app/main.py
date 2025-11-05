from dotenv import load_dotenv
load_dotenv(override=True)  # Load .env FIRST before any other imports, override existing env vars

import os
print("DEBUG -> MOCK_AI =", os.getenv("MOCK_AI"))
print("DEBUG -> OPENAI_API_KEY set =", bool(os.getenv("OPENAI_API_KEY")))

from fastapi import FastAPI
import asyncio

# import your routers
from app.routes import gbp_fetch, gbp_analyze, gbp_apply
from app.routes.gbp_reviews import router as reviews_router  # ← add this line

from app.core.config import settings
from app.services.google_api import get_new_reviews
from app.services.ai_optimizer import draft_review_reply

app = FastAPI()

# register routers
app.include_router(gbp_fetch.router)
app.include_router(gbp_analyze.router)
app.include_router(gbp_apply.router)
app.include_router(reviews_router)  # ← add this line

# optional: background monitor loop (mock version)
_PENDING = {}

async def _monitor_loop():
    while True:
        try:
            from app.routes.gbp_reviews import _PENDING as ROUTER_PENDING
            if settings.ENABLE_REVIEW_MONITOR:
                for rv in get_new_reviews():
                    if rv.get("stars", 5) <= settings.REVIEW_BAD_THRESHOLD:
                        sug = draft_review_reply(rv["stars"], rv.get("comment", ""))
                        ROUTER_PENDING[rv["id"]] = {"review": rv, "suggested": sug}
        except Exception as e:
            print("monitor error:", e)
        await asyncio.sleep(settings.REVIEW_POLL_SECONDS)

@app.on_event("startup")
async def _startup():
    asyncio.create_task(_monitor_loop())

