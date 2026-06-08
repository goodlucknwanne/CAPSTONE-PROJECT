from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str
    role: str = "student"


class User(UserBase):
    user_id: UUID
    role: str
    is_active: bool


    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None