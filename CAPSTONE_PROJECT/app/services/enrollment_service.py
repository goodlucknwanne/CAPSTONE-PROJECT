from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.repositories.enrollment_repo import (
    get_enrollment_by_user_and_course,
    get_enrollments_by_course,
    get_all_enrollments,
    count_enrollments_by_course,
    create_enrollment,
    delete_enrollment,
    delete_enrollment_by_id
)
from app.repositories.course_repo import get_course_by_id


async def enroll_student(db: AsyncSession, user_id: UUID, course_id: UUID):
    course = await get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    if not course.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is not active"
        )
    enrollment_count = await count_enrollments_by_course(db, course_id)
    if enrollment_count >= course.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is full"
        )
    existing_enrollment = await get_enrollment_by_user_and_course(db, user_id, course_id)
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already enrolled in this course"
        )
    return await create_enrollment(db, user_id, course_id)


async def deregister_student(db: AsyncSession, user_id: UUID, course_id: UUID):
    enrollment = await get_enrollment_by_user_and_course(db, user_id, course_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return await delete_enrollment(db, user_id,course_id)


async def fetch_all_enrollments(db: AsyncSession):
    return await get_all_enrollments(db)


async def fetch_enrollments_by_course(db: AsyncSession, course_id: UUID):
    course = await get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return await get_enrollments_by_course(db, course_id)


async def remove_student_from_course(db: AsyncSession, enrollment_id: UUID):
    enrollment = await delete_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return enrollment