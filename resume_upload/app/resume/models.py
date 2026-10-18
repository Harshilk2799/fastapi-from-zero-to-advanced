from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Date, func
from app.db.config import Base
from datetime import date, datetime
import enum

class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())

class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    dob: Mapped[date] = mapped_column(Date)
    state: Mapped[str] = mapped_column(String(200))
    gender: Mapped[GenderEnum]
    preferred_locations: Mapped[str] = mapped_column(Text)
    image_path: Mapped[str] = mapped_column(String(255))
    resume_file_path: Mapped[str] = mapped_column(String(255))
