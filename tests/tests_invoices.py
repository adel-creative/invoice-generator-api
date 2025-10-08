"""
Invoice Tests
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def auth_token():
    """Fixture to get auth token"""
    # Register user
    client.post("/auth/register", json={
        "email": "invoice_test@example.com",
        "username": "invoice_user",
        "password": "testpass123"
    })
    
    # Login
    response = client.post("/auth/login", json={
        "username": "invoice_user",
        "password": "testpass123"
    })
    
    return response.json()["access_token"]


def test_create_invoice_success(auth_token):
    """Test successful invoice creation"""
    response = client.post(
        "/invoices/generate",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "client_name": "Test Client",
            "client_email": "client@test.com",
            "language": "en",
            "currency": "USD",
            "items": [
                {
                    "name": "Test Service",
                    "quantity": 1,
                    "price": 100
                }
            ],
            "tax_rate": 10
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["client_name"] == "Test Client"
    assert data["total"] == 110  # 100 + 10% tax
    assert "invoice_number" in data
    assert "pdf_path" in data


def test_create_invoice_no_auth():
    """Test invoice creation without authentication"""
    response = client.post(
        "/invoices/generate",
        json={
            "client_name": "Test Client",
            "client_email": "client@test.com",
            "language": "en",
            "currency": "USD",
            "items": [{"name": "Service", "quantity": 1, "price": 100}]
        }
    )
    
    assert response.status_code == 401


def test_create_invoice_invalid_data(auth_token):
    """Test invoice creation with invalid data"""
    response = client.post(
        "/invoices/generate",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "client_name": "",  # Empty name
            "client_email": "invalid-email",  # Invalid email
            "items": []  # No items
        }
    )
    
    assert response.status_code == 422


def test_get_invoice(auth_token):
    """Test getting invoice by ID"""
    # Create invoice first
    create_response = client.post(
        "/invoices/generate",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "client_name": "Test Client",
            "client_email": "client@test.com",
            "language": "ar",
            "currency": "MAD",
            "items": [{"name": "Service", "quantity": 2, "price": 500}]
        }
    )
    
    invoice_id = create_response.json()["id"]
    
    # Get invoice
    response = client.get(
        f"/invoices/{invoice_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == invoice_id
    assert data["client_name"] == "Test Client"


def test_list_invoices(auth_token):
    """Test listing invoices"""
    response = client.get(
        "/invoices",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "invoices" in data
    assert "total" in data
    assert "page" in data


def test_update_invoice(auth_token):
    """Test updating invoice"""
    # Create invoice
    create_response = client.post(
        "/invoices/generate",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "client_name": "Original Name",
            "client_email": "client@test.com",
            "language": "en",
            "currency": "USD",
            "items": [{"name": "Service", "quantity": 1, "price": 100}]
        }
    )
    
    invoice_id = create_response.json()["id"]
    
    # Update invoice
    response = client.put(
        f"/invoices/{invoice_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "client_name": "Updated Name",
            "status": "paid"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["client_name"] == "Updated Name"
    assert data["status"] == "paid"


def test_delete_invoice(auth_token):
    """Test deleting invoice"""
    # Create invoice
    create_response = client.post(
        "/invoices/generate",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "client_name": "Test Client",
            "client_email": "client@test.com",
            "language": "en",
            "currency": "USD",
            "items": [{"name": "Service", "quantity": 1, "price": 100}]
        }
    )
    
    invoice_id = create_response.json()["id"]
    
    # Delete invoice
    response = client.delete(
        f"/invoices/{invoice_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 204
    
    # Verify deleted
    get_response = client.get(
        f"/invoices/{invoice_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == 404