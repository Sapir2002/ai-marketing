from fastapi import APIRouter, HTTPException
from app.core.ai_utils import improve_gbp_listing  # using the mock-aware helper

router = APIRouter(prefix="/gbp", tags=["GBP Analyzer"])

@router.post("/analyze")
async def analyze_gbp(data: dict):
    try:
        return improve_gbp_listing(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




