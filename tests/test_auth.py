"""
Authentication Tests
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():
    """Test user registration"""
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Test User",
        "company_name": "Test Company"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "payment_link" in data


def test_register_duplicate_email():
    """Test registration with duplicate email"""
    # Register first user
    client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "pass123"
    })
    
    # Try to register with same email
    response = client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "username": "user2",
        "password": "pass456"
    })
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_success():
    """Test successful login"""
    # Register user
    client.post("/auth/register", json={
        "email": "login@example.com",
        "username": "loginuser",
        "password": "loginpass123"
    })
    
    # Login
    response = client.post("/auth/login", json={
        "username": "loginuser",
        "password": "loginpass123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "expires_in" in data


def test_login_wrong_password():
    """Test login with wrong password"""
    # Register user
    client.post("/auth/register", json={
        "email": "wrong@example.com",
        "username": "wronguser",
        "password": "correctpass"
    })
    
    # Try login with wrong password
    response = client.post("/auth/login", json={
        "username": "wronguser",
        "password": "wrongpass"
    })
    
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


def test_login_nonexistent_user():
    """Test login with non-existent user"""
    response = client.post("/auth/login", json={
        "username": "nonexistent",
        "password": "somepass"
    })
    
    assert response.status_code == 401