# app/services/ai_optimizer.py
# app/services/ai_optimizer.py
from app.core.config import settings

def draft_review_reply(stars: int, comment: str) -> str:
    """Mock AI function that drafts a reply to a review."""
    if stars <= settings.REVIEW_BAD_THRESHOLD:
        return "We’re sorry about your experience. Please reach out to us directly so we can make it right."
    return "Thank you for your feedback! We appreciate your support."
