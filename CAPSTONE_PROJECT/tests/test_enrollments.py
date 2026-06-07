import pytest
from uuid import uuid4
from fastapi import status
from app.main import app
from app.dependencies.rbac import require_admin, require_student


class MockStudent:
    user_id = uuid4()
    role = "student"

@pytest.fixture(autouse=True)
def override_rbac_dependencies():
    """Bypasses security dependencies across this entire file."""
    # Force student endpoints to recognize our mock student profile
    app.dependency_overrides[require_student] = lambda: MockStudent()
    # Force admin endpoints to return a dummy administrative context
    app.dependency_overrides[require_admin] = lambda: {"user_id": str(uuid4()), "role": "admin"}
    yield
    app.dependency_overrides.pop(require_student, None)
    app.dependency_overrides.pop(require_admin, None)



@pytest.fixture
async def test_course_id(client) -> str:
    """Helper fixture to create a course so we can enroll into it."""
    payload = {
        "title": "Enrollment Test Course",
        "code": "ENROLL-101",
        "capacity": 20
    }
    
    response = await client.post("/courses/", json=payload)
    return response.json()["course_id"]




@pytest.mark.asyncio
async def test_get_all_enrollments_empty(client):
    """Happy Path: Fetching all enrollments returns an empty list initially."""
    response = await client.get("/enrollments/") # Adjust path if using prefixes like /api/v1/enrollments/
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_enroll_student_success(client, test_course_id):
    """Happy Path: Successfully enroll the logged-in student into a course."""
    
    response = await client.post(f"/enrollments/?course_id={test_course_id}")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["course_id"] == test_course_id
    assert response.json()["user_id"] == str(MockStudent.user_id)
    assert "enrollment_id" in response.json()


@pytest.mark.asyncio
async def test_student_deregister_success(client, test_course_id):
    """Happy Path: Student successfully cancels their own enrollment."""
    
    await client.post(f"/enrollments/?course_id={test_course_id}")

   
    response = await client.delete(f"/enrollments/deregister/{test_course_id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_get_enrollments_by_course(client, test_course_id):
    """Happy Path: Admin successfully fetches enrollments filtered by course ID."""
    
    await client.post(f"/enrollments/?course_id={test_course_id}")

   
    response = await client.get(f"/enrollments/course/{test_course_id}")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["course_id"] == test_course_id


@pytest.mark.asyncio
async def test_admin_remove_student_success(client, test_course_id):
    """Happy Path: Admin successfully drops a student using an enrollment ID."""
    enroll_res = await client.post(f"/enrollments/?course_id={test_course_id}")
    enrollment_id = enroll_res.json()["enrollment_id"]


    response = await client.delete(f"/enrollments/admin/{enrollment_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT