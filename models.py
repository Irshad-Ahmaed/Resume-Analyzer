from typing import List
import uuid
from db import Base
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import Uuid, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(225), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(225), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship
    reports: Mapped[List["Report"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"
    

class Report(Base):
    __tablename__ = 'reports'

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
    resume_text: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(225), nullable=True)
    experience: Mapped[str] = mapped_column(String(50), nullable=True)
    result: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship
    user: Mapped["User"] = relationship(back_populates="reports")

    def __repr__(self):
        return f"<Report {self.id}>"
