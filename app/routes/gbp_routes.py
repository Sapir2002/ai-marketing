from fastapi import APIRouter

router = APIRouter()

@router.get("/gbp/fetch")
def fetch_gbp_data():
    return {
        "description": "Local cafe offering organic coffee and pastries.",
        "services": [
            {"name": "Coffee Brewing", "price": "2.99", "description": "Freshly brewed daily."},
            {"name": "Pastry Baking", "price": "1.99", "description": "Fresh croissants and muffins."}
        ],
        "products": [],
        "qna": [],
        "reviews": []
    }
