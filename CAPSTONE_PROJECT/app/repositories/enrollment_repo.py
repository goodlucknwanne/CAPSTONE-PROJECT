from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate
from uuid import UUID


async def get_enrollment_by_user_and_course(db: AsyncSession, user_id: UUID, course_id: UUID):
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        )
    )
    return result.scalars().first()


async def get_enrollments_by_course(db: AsyncSession, course_id: UUID):
    result = await db.execute(
        select(Enrollment).where(Enrollment.course_id == course_id)
    )
    return result.scalars().all()


async def get_all_enrollments(db: AsyncSession):
    result = await db.execute(select(Enrollment))
    return result.scalars().all()


async def count_enrollments_by_course(db: AsyncSession, course_id: UUID):
    result = await db.execute(
        select(Enrollment).where(Enrollment.course_id == course_id)
    )
    return len(result.scalars().all())


async def create_enrollment(db: AsyncSession, user_id: UUID, course_id: UUID):
    db_enrollment = Enrollment(
        user_id=user_id,
        course_id=course_id
    )
    db.add(db_enrollment)
    await db.flush()
    return db_enrollment


async def delete_enrollment(db: AsyncSession, user_id: UUID, course_id: UUID):
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        )
    )
    db_enrollment = result.scalars().first()
    if not db_enrollment:
        return None
    await db.delete(db_enrollment)
    await db.flush()
    return db_enrollment


async def delete_enrollment_by_id(db: AsyncSession, enrollment_id: UUID):
    result = await db.execute(
        select(Enrollment).where(Enrollment.enrollment_id == enrollment_id)
    )
    db_enrollment = result.scalars().first()
    if not db_enrollment:
        return None
    await db.delete(db_enrollment)
    await db.flush()
    return db_enrollment