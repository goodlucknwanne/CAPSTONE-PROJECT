from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.course import Course, CourseCreate, CourseUpdate
from app.dependencies.rbac import require_admin
from app.services.course_service import (
    fetch_all_courses,
    fetch_course_by_id,
    add_course,
    edit_course,
    remove_course
)

course_router = APIRouter()


@course_router.get("/", response_model=list[Course])
async def get_all_courses(db: AsyncSession = Depends(get_db)):
    return await fetch_all_courses(db)


@course_router.get("/{course_id}", response_model=Course)
async def get_course(course_id: UUID, db: AsyncSession = Depends(get_db)):
    return await fetch_course_by_id(db, course_id)


@course_router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    return await add_course(db, course)


@course_router.put("/{course_id}", response_model=Course)
async def update_course(
    course_id: UUID,
    course: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    return await edit_course(db, course_id, course)


@course_router.patch("/{course_id}/status", response_model=Course)
async def toggle_course_status(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    course = await fetch_course_by_id(db, course_id)
    toggle = CourseUpdate(is_active=not course.is_active)
    return await edit_course(db, course_id, toggle)


@course_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    await remove_course(db, course_id)