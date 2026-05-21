auth_prefix = "/api/v1/movies"
user_data = {
    "username": "WC",
    "email": "2500297686@qq.com",
    "password": "666999",
    "name": "WC_Liu",
}


def test_get_all_movies(test_client, fake_movie_service, fake_session):
    response = test_client.get(
        url=f"{auth_prefix}",
    )

    assert fake_movie_service.user_exists_called_once()
    assert fake_movie_service.user_exists_called_once_with(fake_session)
    # assert fake_movie_service.create_user_called_once()
    # assert fake_movie_service.create_user_called_once_with(signup_data, fake_session)
