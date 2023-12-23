from datetime import datetime
from sqlalchemy import JSON, Boolean, Column, Integer, String, TIMESTAMP, ForeignKey

from src.database import Base


class Status(Base):
    __tablename__ = "status"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    created_at = Column("created_at", TIMESTAMP, default=datetime.utcnow)
    status_type = Column("awards", JSON)


class Player(Base):
    __tablename__ = "player"

    id = Column("id", Integer, primary_key=True)
    nickname = Column("nickname", String, nullable=False)
    role = Column("role", String, nullable=False)
    mmr = Column("mmr", Integer, nullable=False)

    status = Column("status_id", Integer, ForeignKey("status.id"), default=None)
