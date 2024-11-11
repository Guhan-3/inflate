# Tests for user endpoints 
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/api/v1/users/register", json={
        "username": "inflate_user",
        "email": "inflate@example.com",
        "password": "inflate123"
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_login_user():
    response = client.post("/api/v1/users/login", json={
        "email": "inflate@example.com",
        "password": "inflate123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_invalid_login():
    response = client.post("/api/v1/users/login", json={
        "email": "inflate@example.com",
        "password": "inflate111"
    })
    assert response.status_code == 401