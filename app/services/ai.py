from typing import Dict
from app.models.gbp import NormalizedGBP, OptimizedGBP, OptimizedText

class AIProvider:
    def analyze(self, payload: NormalizedGBP) -> OptimizedGBP:
        # basic rules mock (no external calls)
        improved_desc = None
        if payload.description:
            improved_desc = OptimizedText(
                original=payload.description,
                improved=f"{payload.description} — Now with faster booking and same-day support.",
                notes="Added benefits + call to action"
            )
        replies=[]
        for r in payload.reviews:
            replies.append({"reviewId": r.reviewId, "reply": "Thank you for your feedback!", "tone":"friendly"})
        return OptimizedGBP(
            description=improved_desc,
            services=payload.services,
            products=payload.products,
            qna=payload.qna,
            reviewReplies=replies,
        )

provider = AIProvider()
