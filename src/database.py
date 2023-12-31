from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from sqlalchemy.pool import NullPool

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column("id", Integer, primary_key=True)
    email = Column("email", String, nullable=False)
    username = Column("username", String, nullable=False)
    registered_at = Column("registered_at", TIMESTAMP, default=datetime.utcnow)
    hashed_password = Column("hashed_password", String, nullable=False)
    is_active = Column("is_active", Boolean, default=True, nullable=False)
    is_superuser = Column("is_superuser", Boolean, default=False, nullable=False)
    is_verified = Column("is_verified", Boolean, default=False, nullable=False)


engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
