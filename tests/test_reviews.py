import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest

from app.models.models import Review

pytestmark = pytest.mark.asyncio

reviews_prefix = "/api/v1/movies"


def _make_review(**overrides) -> Review:
    data = {
        "uid": uuid.uuid4(),
        "rating": 8.0,
        "review_text": "Great movie!",
        "user_id": uuid.uuid4(),
        "movie_id": uuid.uuid4(),
        "created_at": datetime.now(timezone.utc),
    }
    data.update(overrides)
    return Review(**data)


MOVIE_UID = "00000000-0000-0000-0000-000000000000"
REVIEW_DATA = {"rating": 9.0, "review_text": "Awesome!"}


class TestAddReview:
    async def test_add_review_success(self, authed_client):
        mock_review = _make_review(rating=9.0, review_text="Awesome!")
        #MOVIE_UID = mock_review.movie_id
        with patch(
            "app.routers.reviews.review_service.add_review_to_movie",
            new=AsyncMock(return_value=mock_review),
        ):
            resp = await authed_client.post(
                f"{reviews_prefix}/{MOVIE_UID}/reviews",
                json=REVIEW_DATA,
            )
        assert resp.status_code == 200
        body = resp.json()
        assert body["data"]["rating"] == 9.0
        assert body["data"]["review_text"] == "Awesome!"

    async def test_add_review_unauthenticated(self, async_client):
        resp = await async_client.post(
            f"{reviews_prefix}/{MOVIE_UID}/reviews",
            json=REVIEW_DATA,
        )
        assert resp.status_code == 401

    async def test_add_review_invalid_data(self, authed_client):
        resp = await authed_client.post(
            f"{reviews_prefix}/{MOVIE_UID}/reviews",
            json={"rating": 15, "review_text": ""},
        )
        assert resp.status_code == 422


class TestGetReviews:
    async def test_get_reviews_success(self, authed_client):
        mock_reviews = [
            _make_review(review_text="Good"),
            _make_review(review_text="Bad"),
        ]

        with patch(
            "app.routers.reviews.review_service.get_movie_all_reviews",
            new=AsyncMock(return_value=mock_reviews),
        ):
            resp = await authed_client.get(
                f"{reviews_prefix}/{MOVIE_UID}/reviews"
            )

        assert resp.status_code == 200
        body = resp.json()
        assert len(body["data"]) == 2
        assert body["data"][0]["review_text"] == "Good"

    async def test_get_reviews_unauthenticated(self, async_client):
        resp = await async_client.get(
            f"{reviews_prefix}/{MOVIE_UID}/reviews"
        )
        assert resp.status_code == 401


class TestDeleteReview:
    REVIEW_UID = "11111111-1111-1111-1111-111111111111"

    async def test_delete_review_success(self, authed_client):
        with patch(
            "app.routers.reviews.review_service.delete_user_review",
            new=AsyncMock(),
        ):
            resp = await authed_client.delete(
                f"{reviews_prefix}/{MOVIE_UID}/reviews/{self.REVIEW_UID}"
            )

        assert resp.status_code == 204

    async def test_delete_review_unauthenticated(self, async_client):
        resp = await async_client.delete(
            f"{reviews_prefix}/{MOVIE_UID}/reviews/{self.REVIEW_UID}"
        )
        assert resp.status_code == 401