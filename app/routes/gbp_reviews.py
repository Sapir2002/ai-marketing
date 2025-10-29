from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.gbp import GBPReview

router = APIRouter(prefix="/gbp/reviews", tags=["GBP Reviews"])

@router.post("/auto-reply")
async def auto_reply(location_id: str = Query(...), dry_run: bool = True):
    """
    TODO:
      1) fetch new reviews
      2) sentiment analysis
      3) generate replies
      4) if not dry_run: POST replies to GBP
    """
    try:
        # mock run
        actions = [{"reviewId": "r1", "reply": "Thanks for the kind words!", "sentiment": "pos"}]
        return {"dry_run": dry_run, "actions": actions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
