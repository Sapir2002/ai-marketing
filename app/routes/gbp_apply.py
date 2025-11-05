from fastapi import APIRouter, HTTPException
from typing import Any, Dict

router = APIRouter(prefix="/gbp", tags=["GBP Apply"])

@router.post("/apply")
async def apply_updates(payload: Dict[str, Any]):
    try:
        result = {"locationId": payload.get("locationId"), "updated": list(payload.keys())}
        return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
