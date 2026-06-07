import pytest
from uuid import uuid4
from fastapi import status
from app.main import app
from app.dependencies.auth import get_current_user


class MockUser:
    user_id = uuid4()
    name = "Profile Owner"
    email = "profile@example.com"
    role = "student"
    is_active = True

@pytest.fixture(autouse=True)
def override_auth_dependency():
    """Automatically logs in our mock user for all tests in this file."""
    app.dependency_overrides[get_current_user] = lambda: MockUser()
    yield
    app.dependency_overrides.pop(get_current_user, None)



@pytest.mark.asyncio
async def test_get_my_profile_success(client):
    """Happy Path: Successfully retrieve the active user profile data."""
    response = await client.get("/users/me")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == MockUser.email
    assert response.json()["name"] == MockUser.name
    assert response.json()["role"] == MockUser.role
    assert response.json()["user_id"] == str(MockUser.user_id)
    assert response.json()["is_active"] is True