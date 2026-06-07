import pytest
from uuid import uuid4
from fastapi import status
from app.main import app
from app.dependencies.rbac import require_admin


@pytest.fixture(autouse=True)
def override_rbac_dependency():
    """Automatically bypasses the admin check for all tests in this file."""
    app.dependency_overrides[require_admin] = lambda: {"user_id": str(uuid4()), "role": "admin"}
    yield
    app.dependency_overrides.pop(require_admin, None)




@pytest.mark.asyncio
async def test_get_all_courses_empty(client):
    """Happy Path: Verify an empty list returns when no courses exist."""
    response = await client.get("/courses/")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []




@pytest.mark.asyncio
async def test_create_course_success(client):
    """Happy Path: Successfully create a new course with required fields."""
    payload = {
        "title": "Introduction to Python Testing",
        "code": "PY-101",       
        "capacity": 30         
    }

    response = await client.post("/courses/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == payload["title"]
    assert response.json()["code"] == payload["code"]
    assert "course_id" in response.json()


@pytest.mark.asyncio
async def test_create_course_invalid_payload(client):
    """Negative Path: Creation fails if required fields are missing."""
    payload = {"title": "Missing Code and Capacity"}

    response = await client.post("/courses/", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY




@pytest.mark.asyncio
async def test_course_lifecycle_workflow(client):
    """Scenario Path: Creates a course, reads it, updates it, toggles status, and deletes it."""
    
   
    setup_payload = {
        "title": "Lifecycle Course", 
        "code": "LIFECYCLE-999", 
        "capacity": 50
    }
    setup_res = await client.post("/courses/", json=setup_payload)
    course_id = setup_res.json()["course_id"]

    
    get_res = await client.get(f"/courses/{course_id}")
    assert get_res.status_code == status.HTTP_200_OK
    assert get_res.json()["title"] == "Lifecycle Course"

   
    update_payload = {
        "title": "Updated Title", 
        "code": "LIFECYCLE-999", 
        "capacity": 60
    }
    put_res = await client.put(f"/courses/{course_id}", json=update_payload)
    assert put_res.status_code == status.HTTP_200_OK
    assert put_res.json()["title"] == "Updated Title"
    assert put_res.json()["capacity"] == 60

 
    patch_res = await client.patch(f"/courses/{course_id}/status")
    assert patch_res.status_code == status.HTTP_200_OK
    assert patch_res.json()["is_active"] is False  # Swapped default True to False


    delete_res = await client.delete(f"/courses/{course_id}")
    assert delete_res.status_code == status.HTTP_204_NO_CONTENT


    verify_res = await client.get(f"/courses/{course_id}")
    assert verify_res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_nonexistent_course_404(client):
    """Negative Path: Attempting to fetch a missing UUID returns a 404."""
    random_uuid = str(uuid4())
    response = await client.get(f"/courses/{random_uuid}")
    assert response.status_code == status.HTTP_404_NOT_FOUND