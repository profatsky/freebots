import pytest
from httpx import AsyncClient

from src.apps.auth.schemas import AuthCredentialsSchema
from src.apps.users.schemas import UserReadSchema


class TestRegisterAPI:
    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient):
        payload = {
            'email': 'email@email.com',
            'password': 'password',
        }
        response = await client.post('/register', json=payload)
        assert response.status_code == 201

        response_data = response.json()
        assert response_data['detail'] == 'Registration was successful'
        assert 'access_token' in response_data

    @pytest.mark.asyncio
    async def test_register_existing_user(
        self,
        client: AsyncClient,
        test_user: UserReadSchema,
        test_user_credentials: AuthCredentialsSchema,
    ):
        response = await client.post('/register', json=test_user_credentials.model_dump())
        assert response.status_code == 409
        assert response.json() == {'detail': 'User with this email address is already registered'}

    @pytest.mark.asyncio
    async def test_registration_with_invalid_email_format(self, client: AsyncClient):
        payload = {
            'email': 'invalid_email',
            'password': 'password',
        }
        response = await client.post('/register', json=payload)
        assert response.status_code == 422

        error_location = response.json()['detail'][0]['loc']
        assert error_location == ['body', 'email']

    @pytest.mark.asyncio
    async def test_register_with_invalid_password_format(self, client: AsyncClient):
        payload = {
            'email': 'email@email.com',
            'password': '123',
        }
        response = await client.post('/register', json=payload)
        assert response.status_code == 422

        error_location = response.json()['detail'][0]['loc']
        assert error_location == ['body', 'password']

    @pytest.mark.asyncio
    async def test_register_with_missing_fields(self, client: AsyncClient):
        invalid_payloads = [
            {'email': 'missing_password@email.com'},
            {'password': 'missing_email'},
            {},
        ]
        for payload in invalid_payloads:
            response = await client.post('/register', json=payload)
            assert response.status_code == 422


class TestLoginAPI:
    @pytest.mark.asyncio
    async def test_login_success(
        self,
        client: AsyncClient,
        test_user: UserReadSchema,
        test_user_credentials: AuthCredentialsSchema,
    ):
        response = await client.post('/login', json=test_user_credentials.model_dump())
        assert response.status_code == 200

        response_data = response.json()
        assert response_data['detail'] == 'Authorization was successful'
        assert 'access_token' in response_data

    @pytest.mark.asyncio
    async def test_login_with_invalid_email(self, client: AsyncClient):
        payload = {
            'email': 'unregistered@email.com',
            'password': 'password',
        }
        response = await client.post('/login', json=payload)
        assert response.status_code == 401
        assert response.json() == {'detail': 'Invalid credentials'}

    @pytest.mark.asyncio
    async def test_login_with_invalid_password(self, client: AsyncClient, test_user: UserReadSchema):
        payload = {
            'email': test_user.email,
            'password': 'invalid_password',
        }
        response = await client.post('/login', json=payload)
        assert response.status_code == 401
        assert response.json() == {'detail': 'Invalid credentials'}

    @pytest.mark.asyncio
    async def test_login_with_invalid_email_format(self, client: AsyncClient):
        payload = {
            'email': 'invalid_email',
            'password': 'password',
        }
        response = await client.post('/login', json=payload)
        assert response.status_code == 422

        error_location = response.json()['detail'][0]['loc']
        assert error_location == ['body', 'email']

    @pytest.mark.asyncio
    async def test_login_with_invalid_password_format(self, client: AsyncClient):
        payload = {
            'email': 'email@email.com',
            'password': '123',
        }
        response = await client.post('/login', json=payload)
        assert response.status_code == 422

        error_location = response.json()['detail'][0]['loc']
        assert error_location == ['body', 'password']

    @pytest.mark.asyncio
    async def test_login_with_missing_fields(self, client: AsyncClient):
        invalid_payloads = [
            {'email': 'missing_password@email.com'},
            {'password': 'missing_email'},
            {},
        ]
        for payload in invalid_payloads:
            response = await client.post('/login', json=payload)
            assert response.status_code == 422
