from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Dummy Loan API is running"


def test_high_risk_prediction_for_low_credit_score():
    response = client.post("/predict", json={"credit_score": 550, "debt_to_income": 0.25})
    assert response.status_code == 200
    assert response.json()["risk"] == "high"


def test_low_risk_prediction():
    response = client.post("/predict", json={"credit_score": 760, "debt_to_income": 0.20})
    assert response.status_code == 200
    assert response.json()["risk"] == "low"


def test_invalid_credit_score_is_rejected():
    response = client.post("/predict", json={"credit_score": 950, "debt_to_income": 0.20})
    assert response.status_code == 422
