from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


async def get_all_courses(db: AsyncSession):
    result = await db.execute(select(Course))
    return result.scalars().all()


async def get_course_by_id(db: AsyncSession, course_id: str):
    result = await db.execute(select(Course).where(Course.course_id == course_id))
    return result.scalars().first()


async def get_course_by_code(db: AsyncSession, code: str):
    result = await db.execute(select(Course).where(Course.code == code))
    return result.scalars().first()


async def create_course(db: AsyncSession, course: CourseCreate):
    db_course = Course(
        title=course.title,
        code=course.code,
        capacity=course.capacity
    )
    db.add(db_course)
    await db.flush()
    return db_course


async def update_course(db: AsyncSession, course_id: str, course: CourseUpdate):
    result = await db.execute(select(Course).where(Course.course_id == course_id))
    db_course = result.scalars().first()
    if not db_course:
        return None
    if course.title is not None:
        db_course.title = course.title
    if course.code is not None:
        db_course.code = course.code
    if course.capacity is not None:
        db_course.capacity = course.capacity
    if course.is_active is not None:
        db_course.is_active = course.is_active
    await db.flush()
    return db_course


async def delete_course(db: AsyncSession, course_id: str):
    result = await db.execute(select(Course).where(Course.course_id == course_id))
    db_course = result.scalars().first()
    if not db_course:
        return None
    await db.delete(db_course)
    await db.flush()
    return db_course