from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth_service import hash_password



async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    await db.flush()
    return db_user