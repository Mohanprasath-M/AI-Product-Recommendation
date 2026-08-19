import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_analytics_overview():
    response = client.get("/api/analytics/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_customers" in data
    assert "total_products" in data
    assert "total_revenue" in data
    assert data["total_customers"] > 0


def test_conversion_funnel():
    response = client.get("/api/analytics/conversion-funnel")
    assert response.status_code == 200
    data = response.json()
    assert "views" in data
    assert "purchases" in data


def test_nlp_sentiment_review_creation():
    prod_res = client.get("/api/products?size=1")
    product_id = prod_res.json()["items"][0]["id"]

    response = client.post("/api/reviews", json={
        "product_id": product_id,
        "rating": 5.0,
        "title": "Superb Quality",
        "comment": "Amazing sound quality, very comfortable and fast battery charging!"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["sentiment_label"] == "POSITIVE"
    assert len(data["positive_topics"]) > 0
