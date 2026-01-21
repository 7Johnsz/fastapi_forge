from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import (
    DateTime,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
)

import datetime


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="users_pkey"),
        UniqueConstraint("name", name="users_name_key"),
        Index("ix_users_email", "email", unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    hash_host: Mapped[str] = mapped_column(String, nullable=True)
