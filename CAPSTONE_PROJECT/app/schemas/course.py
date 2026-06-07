from pydantic import BaseModel
from uuid import UUID

class CourseBase(BaseModel):
    title: str
    code: str
    capacity: int


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):
    course_id: UUID
    is_active: bool


    class Config:
        from_attributes = True


class CourseUpdate(BaseModel):
    title: str | None = None
    code: str | None = None
    capacity: int | None = None
    is_active: bool | None = None