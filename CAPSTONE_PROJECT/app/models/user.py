from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    user_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    email:Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="student")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    enrollments = relationship("Enrollment", back_populates="user")