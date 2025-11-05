# app/routes/gbp_fetch.py
from typing import Literal
from fastapi import APIRouter, HTTPException, Query
from app.models.gbp import NormalizedGBP

router = APIRouter(prefix="/gbp", tags=["GBP Fetch"])


Scope = Literal["all", "description", "services", "products", "qna", "reviews"]

@router.get("/fetch", response_model=NormalizedGBP)
async def fetch_gbp(scope: Scope = Query("all"), location_id: str = Query(...)):
    try:
        # Mock data; swap with real Google API later
        data = NormalizedGBP(
            description="Current business description",
            services=[{"title": "Teeth Whitening", "price": 149.0, "description": "60-min treatment"}],
            products=[{"name": "Starter Kit", "price": 29.0, "category": "Kits", "description": "All you need"}],
            qna=[{"question": "Do you take walk-ins?", "answer": "Yes, until 5pm", "upvoteCount": 3}],
            reviews=[{"reviewId": "r1", "starRating": 5, "comment": "Great!"}],
        )
        if scope == "description":
            data.services = []; data.products = []; data.qna = []; data.reviews = []
        elif scope == "services":
            data.description = None; data.products = []; data.qna = []; data.reviews = []
        elif scope == "products":
            data.description = None; data.services = []; data.qna = []; data.reviews = []
        elif scope == "qna":
            data.description = None; data.services = []; data.products = []; data.reviews = []
        elif scope == "reviews":
            data.description = None; data.services = []; data.products = []; data.qna = []
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

