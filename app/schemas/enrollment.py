from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class EnrollmentBase(BaseModel):
    user_id: UUID
    course_id: UUID


class EnrollmentCreate(EnrollmentBase):
    pass


class Enrollment(EnrollmentBase):
    enrollment_id: UUID
    created_at: datetime


    class Config:
        from_attributes = True