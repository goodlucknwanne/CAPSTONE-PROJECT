from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import User
from app.dependencies.auth import get_current_user
from app.models.user import User as UserModel


user_router = APIRouter()


@user_router.get("/me", response_model=User)
async def get_my_profile(current_user: UserModel = Depends(get_current_user)):
    return current_user