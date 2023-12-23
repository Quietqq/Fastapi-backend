from fastapi import APIRouter, Depends
from sqlalchemy import delete, insert, select, update

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.engine import Result

from src.product.schemas import CreatePlayer, UpdateNickname
from src.database import get_async_session
from src.product.models import Player

from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

players_router = APIRouter(prefix="/players", tags=["Player"])


@players_router.get("/{player_id}")
async def get_player_id(
    player_id: int, session: AsyncSession = Depends(get_async_session)
):
    query = select(Player).where(Player.id == player_id)
    res: Result = await session.execute(query)
    players = res.scalars().all()
    return list(players)


@players_router.get("/")
@cache(expire=30)
async def get_players(session: AsyncSession = Depends(get_async_session)):
    query = select(Player).order_by(Player.id)
    res: Result = await session.execute(query)
    players = res.scalars().all()
    return list(players)


@players_router.post("/")
async def add_new_player(
    operation: CreatePlayer, session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(Player).values(operation.model_dump())
    await session.execute(stmt)
    await session.commit()

    query = select(Player).order_by(Player.id)
    res: Result = await session.execute(query)
    players = res.scalars().all()

    return list(players)


@players_router.patch("/new_nickname/{player_id}")
async def change_player_nickname(
    player_id: int,
    operation: UpdateNickname,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = update(Player).where(Player.id == player_id).values(operation.dict())
    await session.execute(stmt)
    await session.commit()
    query = select(Player).where(Player.id == player_id)
    res: Result = await session.execute(query)
    players = res.scalars().all()
    return list(players)


@players_router.patch("/new_mmr/{player_nickmane}")
async def change_player_mmr(
    player_nickname: str,
    new_mmr: int,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = update(Player).where(Player.nickname == player_nickname).values(mmr=new_mmr)
    await session.execute(stmt)
    await session.commit()

    query = select(Player).where(Player.nickname == player_nickname)
    res: Result = await session.execute(query)
    players = res.scalars().all()

    return list(players)


@players_router.delete("/{player_id}")
async def delete_player(
    player_id: int, session: AsyncSession = Depends(get_async_session)
):
    stmt = delete(Player).where(Player.id == player_id)
    await session.execute(stmt)
    await session.commit()

    query = select(Player).order_by(Player.id)
    res: Result = await session.execute(query)
    players = res.scalars().all()

    return list(players)
