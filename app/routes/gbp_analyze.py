from fastapi import APIRouter
from app.core.ai_utils import improve_gbp_listing
import json

router = APIRouter()

@router.post("/gbp/analyze")
async def analyze_gbp(data: dict):
    improved_text = improve_gbp_listing(data)
    return improved_text

