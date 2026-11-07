from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_ingest_lead_valid():
    payload = {
        "client_name": "Rohan Sharma",
        "contact_number": "+919876543210",
        "lead_source": "Meta Ads / Solitaire Campaign",
        "diamond_metal_preference": "Oval 2 Carat Solitaire, Platinum",
        "budget_range": "INR 3.5 - 5 Lakhs",
        "consultation_type": "In-Studio Visit"
    }
    response = client.post("/api/v1/leads/ingest", json=payload)
    assert response.status_code == 201
    assert response.json()["status"] == "Success"
    assert "HATO-" in response.json()["lead_id"]

def test_ingest_lead_invalid_phone():
    payload = {
        "client_name": "Rohan Sharma",
        "contact_number": "invalid_phone_number"
    }
    response = client.post("/api/v1/leads/ingest", json=payload)
    assert response.status_code == 422
