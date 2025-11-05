from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_fetch_all():
    r = client.get("/gbp/fetch", params={"scope":"all","location_id":"loc1"})
    assert r.status_code == 200
    body = r.json()
    assert "services" in body and "products" in body and "qna" in body and "reviews" in body

def test_analyze_roundtrip():
    payload = {
        "description":"We’re a local dental clinic.",
        "services":[{"title":"Cleaning","price":99.0}],
        "products":[],
        "qna":[],
        "reviews":[{"reviewId":"r1","starRating":5,"comment":"Great"}]
    }
    r = client.post("/gbp/analyze", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "reviewReplies" in body
    if body.get("description"):
        assert body["description"]["improved"]

def test_apply_stub():
    r = client.post("/gbp/apply", json={"locationId":"loc1","description":"New desc"})
    assert r.status_code == 200
    assert r.json()["ok"] is True
