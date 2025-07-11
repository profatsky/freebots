import pytest
from httpx import AsyncClient


class TestUsersAPI:
    @pytest.mark.asyncio
    async def test_get_me_success(self, authorized_test_client: AsyncClient):
        response = await authorized_test_client.get('/users/me')
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_me_unauthorized(self, client: AsyncClient):
        response = await client.get('/users/me')
        assert response.status_code == 401
