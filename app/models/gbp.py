from typing import List, Optional
from pydantic import BaseModel, Field

class GBPService(BaseModel):
    serviceTypeId: Optional[str] = None
    title: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

class GBPProduct(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None

class GBPQA(BaseModel):
    question: str
    answer: Optional[str] = None
    upvoteCount: Optional[int] = 0

class GBPReview(BaseModel):
    reviewId: str
    starRating: int = Field(ge=1, le=5)
    comment: Optional[str] = None

class NormalizedGBP(BaseModel):
    description: Optional[str] = None
    services: List[GBPService] = []
    products: List[GBPProduct] = []
    qna: List[GBPQA] = []
    reviews: List[GBPReview] = []

class OptimizedText(BaseModel):
    original: Optional[str] = None
    improved: Optional[str] = None
    notes: Optional[str] = None

class OptimizedGBP(BaseModel):
    description: Optional[OptimizedText] = None
    services: List[GBPService] = []
    products: List[GBPProduct] = []
    qna: List[GBPQA] = []
    reviewReplies: List[dict] = []  # {reviewId, reply, tone}
