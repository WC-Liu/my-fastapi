from app.schemas.auth import UserCreate

auth_prefix = "/api/v1/auth"
user_data = {
    "username": "WC",
    "email": "2500297686@qq.com",
    "password": "666999",
    "name": "WC_Liu",
}

signup_data = UserCreate(**user_data)


def test_user_creation(fake_session, fake_user_service, test_client):
    response = test_client.post(
        url=f"{auth_prefix}/register",
        json=user_data,
    )

    assert fake_user_service.user_exists_called_once()
    assert fake_user_service.user_exists_called_once_with(
        user_data["email"], fake_session
    )
    assert fake_user_service.create_user_called_once()
    assert fake_user_service.create_user_called_once_with(signup_data, fake_session)
