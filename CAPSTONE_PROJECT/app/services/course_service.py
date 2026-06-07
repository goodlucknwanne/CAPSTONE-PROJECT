from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.course_repo import (
    get_all_courses,
    get_course_by_id,
    get_course_by_code,
    create_course,
    update_course,
    delete_course
)
from app.schemas.course import CourseCreate, CourseUpdate
from fastapi import HTTPException, status
from uuid import UUID


async def fetch_all_courses(db: AsyncSession):
    return await get_all_courses(db)


async def fetch_course_by_id(db: AsyncSession, course_id: UUID):
    course = await get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course


async def add_course(db: AsyncSession, course: CourseCreate):
    existing_course = await get_course_by_code(db, course.code)
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course code already exists"
        )
    if course.capacity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Capacity must be greater than zero"
        )
    return await create_course(db, course)


async def edit_course(db: AsyncSession, course_id: UUID, course: CourseUpdate):
    existing_course = await get_course_by_id(db, course_id)
    if not existing_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.code is not None:
        code_taken = await get_course_by_code(db, course.code)
        if code_taken and str(code_taken.course_id) != str(course_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course code already exists"
            )
        
    if course.capacity is not None and course.capacity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Capacity must be greater than zero"
        )
    return await update_course(db, course_id, course)


async def remove_course(db: AsyncSession, course_id: UUID):
    course = await get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return await delete_course(db, course_id)