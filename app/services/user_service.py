from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import get_user_by_email, get_user_by_id, create_user
from app.schemas.user import UserCreate
from app.services.auth_service import hash_password, verify_password
from fastapi import HTTPException, status
from uuid import UUID


async def register_user(db: AsyncSession, user: UserCreate):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return await create_user(db, user)


async def get_user_profile(db: AsyncSession, user_id: UUID):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user