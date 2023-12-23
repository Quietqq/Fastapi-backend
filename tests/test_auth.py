from conftest import client


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "id": 0,
            "email": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "string",
            "password": "string",
        },
    )

    assert response.status_code == 201
