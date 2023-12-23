from fastapi.testclient import TestClient
from httpx import AsyncClient


async def test_add_player(ac: AsyncClient):
    response = await ac.post(
        "/players/", json={"id": 10, "nickname": "string", "role": "string", "mmr": 0}
    )

    assert response.status_code == 200


async def test_get_players(ac: TestClient):
    response = await ac.get("/players/")

    assert response.status_code == 200
    assert response.json()
