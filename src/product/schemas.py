from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from src.product.enums import StatusType


class StatusBase(BaseModel):
    id: int
    created_at: datetime
    status_type: StatusType


class PlayersBase(BaseModel):
    id: int
    nickname: str
    role: str
    mmr: int
    status: Optional[List[StatusBase]] = []


class CreatePlayer(BaseModel):
    id: int
    nickname: str
    role: str
    mmr: int


class UpdateNickname(BaseModel):
    nickname: Optional[str] = None
