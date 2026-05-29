from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.models import Movie
from app.utils import exceptions

pytestmark = pytest.mark.asyncio

movies_prefix = "/api/v1/movies/"

def _build_mock_movie(**override) -> Movie:
    import uuid
    from datetime import datetime, timezone

    data = {
        "uid": uuid.uuid4(),
        "title": "Test Movie",
        "director": "Test Director",
        "year": 2024,
        "rating": 8.5,
        "genre": "Action",
        "is_showing": True,
        "imdb": "tt1234567",
        "created_at": datetime.now(timezone.utc),
        "reviews": [],
    }
    data.update(override)
    return Movie(**data)

MOVIE_CREATE_DATA = {
    "title": "New Movie",
    "director": "New Director",
    "year": 2025,
    "rating": 9.0,
    "genre": "Sci-Fi",
    "is_showing": True,
    "imdb": "tt7654321",
}

MOVIE_UPDATE_DATA = {
    "title": "Updated Movie",
    "rating": 7.5,
}

class TestGetMovies:
    async def test_get_movies_success(self, authed_client):
        mock_movies = [_build_mock_movie(), _build_mock_movie()]

        with patch(
            "app.routers.movies.movie_service.get_all_movies",
            new=AsyncMock(return_value=mock_movies)
        ):
            resp = await authed_client.get(movies_prefix)
        
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert len(body["data"]) == 2 

    async def test_get_movies_unauthenticated(self, async_client):
        resp = await async_client.get(movies_prefix)
        assert resp.status_code == 401
    
class TestGetMovie:
    async def test_get_movie_success(self, authed_client):
        mock_movie = _build_mock_movie()

        with patch(
            "app.routers.movies.movie_service.get_movie",
            new=AsyncMock(return_value=mock_movie),
        ):
            resp = await authed_client.get(f"{movies_prefix}00000000-0000-0000-0000-000000000000")
        
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert body["data"]["title"] == "Test Movie"

    async def test_get_movie_not_found(self, authed_client):
        with patch(
            "app.routers.movies.movie_service.get_movie",
            side_effect=exceptions.MovieNotFoundError,
        ):
            resp = await authed_client.get(
                f"{movies_prefix}00000000-0000-0000-0000-000000000000"
            )

        assert resp.status_code == 404

class TestCreateMovie:
    async def test_create_movie_as_superuser(self, superuser_client):
        mock_movie = _build_mock_movie(**MOVIE_CREATE_DATA)

        with patch(
            "app.routers.movies.movie_service.create_movie",
            new=AsyncMock(return_value=mock_movie),
        ):
            resp = await superuser_client.post(movies_prefix, json=MOVIE_CREATE_DATA)

        assert resp.status_code == 201
        body = resp.json()
        assert body["data"]["title"] == "New Movie"
        assert body["data"]["imdb"] == "tt7654321"

    async def test_create_movie_as_normal_user(self, authed_client):
        resp = await authed_client.post(movies_prefix, json=MOVIE_CREATE_DATA)
        assert resp.status_code == 403

    async def test_create_movie_duplicate_imdb(self, superuser_client):
        with patch(
            "app.routers.movies.movie_service.create_movie",
            side_effect=exceptions.MovieAlreadyExistsError,
        ):
            resp = await superuser_client.post(movies_prefix, json=MOVIE_CREATE_DATA)

        assert resp.status_code == 400

    async def test_create_movie_invalid_data(self, superuser_client):
        resp = await superuser_client.post(
            movies_prefix,
            json={
                "title": "",
                "director": "",
                "year": "not_a_number",
                "rating": 20,
                "genre": "",
                "imdb": "",
            },
        )
        assert resp.status_code == 422

class TestUpdateMovie:
    async def test_update_movie_as_superuser(self, superuser_client):
        mock_movie = _build_mock_movie(title="Updated Movie", rating=7.5)

        with patch(
            "app.routers.movies.movie_service.update_movie",
            new=AsyncMock(return_value=mock_movie),
        ):
            resp = await superuser_client.patch(
                f"{movies_prefix}00000000-0000-0000-0000-000000000000",
                json=MOVIE_UPDATE_DATA,
            )

        assert resp.status_code == 200
        body = resp.json()
        assert body["data"]["title"] == "Updated Movie"
        assert body["data"]["rating"] == 7.5

    async def test_update_movie_as_normal_user(self, authed_client):
        resp = await authed_client.patch(
            f"{movies_prefix}00000000-0000-0000-0000-000000000000",
            json=MOVIE_UPDATE_DATA,
        )
        assert resp.status_code == 403

    async def test_update_movie_not_found(self, superuser_client):
        with patch(
            "app.routers.movies.movie_service.update_movie",
            side_effect=exceptions.MovieNotFoundError,
        ):
            resp = await superuser_client.patch(
                f"{movies_prefix}00000000-0000-0000-0000-000000000000",
                json=MOVIE_UPDATE_DATA,
            )

        assert resp.status_code == 404


class TestDeleteMovie:
    async def test_delete_movie_as_superuser(self, superuser_client):
        with patch(
            "app.routers.movies.movie_service.delete_movie",
            new=AsyncMock(),
        ):
            resp = await superuser_client.delete(
                f"{movies_prefix}00000000-0000-0000-0000-000000000000"
            )

        assert resp.status_code == 204

    async def test_delete_movie_as_normal_user(self, authed_client):
        resp = await authed_client.delete(
            f"{movies_prefix}00000000-0000-0000-0000-000000000000"
        )
        assert resp.status_code == 403

    async def test_delete_movie_not_found(self, superuser_client):
        with patch(
            "app.routers.movies.movie_service.delete_movie",
            side_effect=exceptions.MovieNotFoundError,
        ):
            resp = await superuser_client.delete(
                f"{movies_prefix}00000000-0000-0000-0000-000000000000"
            )

        assert resp.status_code == 404