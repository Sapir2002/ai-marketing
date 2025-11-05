# app/routes/gbp_reviews.py
from fastapi import APIRouter, HTTPException
from typing import Dict, List

router = APIRouter(prefix="/gbp/reviews", tags=["GBP Reviews"])

# in-memory pending store (mock)
_PENDING: Dict[str, Dict] = {}

def _get_fake_reviews():
    return [
        {"id": "r1", "author": "John D", "stars": 2, "comment": "Long wait times."},
        {"id": "r2", "author": "Amy L", "stars": 5, "comment": "Great service!"},
    ]

def _draft_reply(stars: int, comment: str) -> str:
    return ("We’re sorry about your experience. Please email support@example.com "
            "so we can make it right.") if stars <= 3 else "Thank you for the kind words!"

@router.get("/monitor", response_model=List[Dict])
def monitor_now():
    pending = []
    for rv in _get_fake_reviews():
        if rv["stars"] <= 3:
            sug = _draft_reply(rv["stars"], rv["comment"])
            _PENDING[rv["id"]] = {"review": rv, "suggested": sug}
            pending.append({"id": rv["id"], "review": rv, "suggestedReply": sug})
    return pending

@router.post("/{review_id}/approve")
def approve(review_id: str):
    item = _PENDING.get(review_id)
    if not item:
        raise HTTPException(status_code=404, detail="No pending reply for that review")
    # mock publish succeeds
    del _PENDING[review_id]
    return {"status": "sent", "reviewId": review_id}
