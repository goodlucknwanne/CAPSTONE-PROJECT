from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers.auth import auth_router
from app.routers.courses import course_router
from app.routers.users import user_router
from app.routers.enrollments import enrollment_router
from app.core.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This automatically spawns your tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Course Enrollment API",
    description="A secure REST API for managing course enrollments",
    version="1.0.0"
)


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["User"])
app.include_router(course_router, prefix="/courses", tags=["Course"])
app.include_router(enrollment_router, prefix="/enrollments", tags=["Enrollments"])