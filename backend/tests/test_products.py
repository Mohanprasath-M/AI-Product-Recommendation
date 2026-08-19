import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_products():
    response = client.get("/api/products?page=1&size=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) > 0


def test_get_categories():
    response = client.get("/api/products/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_product_detail():
    list_res = client.get("/api/products?size=1")
    first_item = list_res.json()["items"][0]
    
    response = client.get(f"/api/products/{first_item['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == first_item["id"]
