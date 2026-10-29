import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

# Create test tables
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def auth_token():
    """Register + login once and reuse the token."""
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123",
    })
    res = client.post("/auth/login", data={
        "username": "testuser",
        "password": "test123",
    })
    return res.json()["access_token"]


def test_create_transaction(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.post("/transactions/", json={
        "title": "Salary",
        "amount": 5000,
        "type": "income",
        "category": "Work",
        "date": "2024-01-15",
    }, headers=headers)
    assert res.status_code == 201
    assert res.json()["title"] == "Salary"


def test_get_transactions(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("/transactions/", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) >= 1


def test_get_specific_transaction(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Get first transaction ID
    all_tx = client.get("/transactions/", headers=headers).json()
    tx_id = all_tx[0]["id"]
    res = client.get(f"/transactions/{tx_id}", headers=headers)
    assert res.status_code == 200
    assert res.json()["id"] == tx_id


def test_update_transaction(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    all_tx = client.get("/transactions/", headers=headers).json()
    tx_id = all_tx[0]["id"]
    res = client.put(f"/transactions/{tx_id}", json={
        "amount": 6000,
    }, headers=headers)
    assert res.status_code == 200
    assert res.json()["amount"] == 6000


def test_delete_transaction(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    all_tx = client.get("/transactions/", headers=headers).json()
    tx_id = all_tx[0]["id"]
    res = client.delete(f"/transactions/{tx_id}", headers=headers)
    assert res.status_code == 200
    assert "deleted" in res.json()["message"]