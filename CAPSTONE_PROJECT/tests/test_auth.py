import pytest
from fastapi import status



@pytest.mark.asyncio
async def test_register_user_success(client):
    """Happy Path: Successfully register a new user using SQLite."""
    payload = {
        "email": "test_register@example.com",
        "password": "securepassword123",
        "name": "Test User",
        "role": "user",
        "is_active": True
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == "test_register@example.com"


@pytest.mark.asyncio
async def test_register_user_invalid_payload(client):
    """Negative Path: Registration fails if payload is empty."""
    payload = {} 

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



@pytest.mark.asyncio
async def test_login_success(client):
    """Happy Path: Login with a real user profile inside SQLite database."""
    # Register the account profile first
    await client.post("/auth/register", json={
        "email": "login_test@example.com",
        "password": "securepassword123",
        "name": "Test User",
        "role": "user",
        "is_active": True
    })
    
    
    form_payload = {
        "username": "login_test@example.com",
        "password": "securepassword123"
    }

    response = await client.post("/auth/login", data=form_payload)

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    """Negative Path: Login throws 401 when account credentials mismatch."""
    form_payload = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    }

    response = await client.post("/auth/login", data=form_payload)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect email or password"