from fastapi import Depends, FastAPI
import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from src.auth.manager import get_user_manager
from src.auth.schemas import UserCreate, UserRead

from src.database import User

# from contextlib import asynccontextmanager
from src.config import REDIS_HOST, REDIS_PORT

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


from redis import asyncio as aioredis


from fastapi.middleware.cors import CORSMiddleware

from src.product.players import players_router
from src.auth.cokkie import auth_backend

app = FastAPI(title="Test app", debug=True)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("starting db session")
#     redis = aioredis.from_url(
#         url="redis://localhost", encoding="utf8", decode_responses=True
#     )
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache", coder=JSONCoder)

#     yield
#     await redis.close()
#     print("shutdown db session")


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(players_router)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return "Hello, anonym"
