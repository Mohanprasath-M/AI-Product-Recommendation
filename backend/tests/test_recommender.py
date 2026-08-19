import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_personalized_recommendations():
    # Fetch a customer
    cust_res = client.get("/api/customers?size=1")
    customer_id = cust_res.json()["items"][0]["id"]

    response = client.get(f"/api/recommendations/{customer_id}?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0
    assert "reason" in data["recommendations"][0]
    assert "signals" in data["recommendations"][0]


def test_similar_products():
    prod_res = client.get("/api/products?size=1")
    product_id = prod_res.json()["items"][0]["id"]

    response = client.get(f"/api/recommendations/product/{product_id}/similar?limit=4")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_bought_together():
    prod_res = client.get("/api/products?size=1")
    product_id = prod_res.json()["items"][0]["id"]

    response = client.get(f"/api/recommendations/product/{product_id}/bought-together?limit=4")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
