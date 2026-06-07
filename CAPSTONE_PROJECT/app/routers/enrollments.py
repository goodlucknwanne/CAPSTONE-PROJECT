from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.enrollment import Enrollment, EnrollmentCreate
from app.dependencies.rbac import require_admin, require_student
from app.services.enrollment_service import (
    enroll_student,
    deregister_student,
    fetch_all_enrollments,
    fetch_enrollments_by_course,
    remove_student_from_course
)

enrollment_router = APIRouter()

@enrollment_router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
async def enroll(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_student)
):
    return await enroll_student(db, current_user.user_id, course_id)

@enrollment_router.delete("/deregister/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deregister(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_student)
):
    await deregister_student(db, current_user.user_id, course_id)

@enrollment_router.get("/", response_model=list[Enrollment])
async def get_all_enrollments(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    return await fetch_all_enrollments(db)

@enrollment_router.get("/course/{course_id}", response_model=list[Enrollment])
async def get_enrollments_by_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    return await fetch_enrollments_by_course(db, course_id)

@enrollment_router.delete("/admin/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_remove_student(
    enrollment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    await remove_student_from_course(db, enrollment_id)