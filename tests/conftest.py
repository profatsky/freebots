import random

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.apps.auth.schemas import AuthCredentialsSchema
from src.core.config import settings
from src.apps.dialogues.repositories import DialogueRepository
from src.apps.dialogues.schemas import DialogueReadSchema
from src.infrastructure.db.sessions import get_async_session, Base
from src.infrastructure.db.utils import get_dsn
from src.main import app
from src.apps.projects.repositories import ProjectRepository
from src.api.v1.projects.schemas import ProjectReadSchema
from src.apps.users.repositories import UserRepository
from src.apps.users.schemas import UserReadSchema
from tests.factories.dialogues import DialogueCreateSchemaFactory
from tests.factories.projects import ProjectCreateSchemaFactory

SQLALCHEMY_DATABASE_URL = get_dsn(
    prefix='postgresql+asyncpg',
    user=settings.DB_USER,
    password=settings.DB_PASS,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.TEST_DB_NAME,
)

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = async_sessionmaker(
    expire_on_commit=False,
    bind=async_engine,
    class_=AsyncSession,
)


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if pytest_asyncio.is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope='session')
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest_asyncio.fixture(scope='session')
async def session():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(scope='function', loop_scope='session', autouse=True)
async def cleanup_tables(session):
    yield
    async with session.begin():
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(text(f'TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE'))
        await session.commit()


@pytest_asyncio.fixture(scope='session')
async def client(session) -> AsyncClient:
    async def override_get_session():
        try:
            yield session
        finally:
            await session.close()

    app.dependency_overrides[get_async_session] = override_get_session
    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app),
            base_url='http://127.0.0.1:8000/api',
        ) as cli:
            yield cli


@pytest_asyncio.fixture(scope='session')
async def user_repository(session) -> UserRepository:
    return UserRepository(session)


@pytest_asyncio.fixture(scope='session')
async def test_user_credentials(session) -> AuthCredentialsSchema:
    return AuthCredentialsSchema(
        email='test@test.com',
        password='password',
    )


@pytest_asyncio.fixture(scope='function', loop_scope='session')
async def test_user(user_repository: UserRepository, test_user_credentials: AuthCredentialsSchema) -> UserReadSchema:
    user = await user_repository.create_user(test_user_credentials)
    yield user
    await user_repository.delete_user(user.user_id)


@pytest_asyncio.fixture(scope='session')
async def another_user_credentials(session) -> AuthCredentialsSchema:
    return AuthCredentialsSchema(
        email='another@test.com',
        password='password',
    )


@pytest_asyncio.fixture(scope='function', loop_scope='session')
async def another_user(
    user_repository: UserRepository, another_user_credentials: AuthCredentialsSchema
) -> UserReadSchema:
    user = await user_repository.create_user(another_user_credentials)
    yield user
    await user_repository.delete_user(user.user_id)


@pytest_asyncio.fixture(scope='function', loop_scope='session')
async def authorized_test_client(
    client: AsyncClient,
    test_user: UserReadSchema,
    test_user_credentials: AuthCredentialsSchema,
) -> AsyncClient:
    response = await client.post('/login', json=test_user_credentials.model_dump())

    access_token = response.json()['access_token']
    client.headers['Authorization'] = access_token
    yield client
    client.headers.pop('Authorization')


@pytest_asyncio.fixture(scope='function', loop_scope='session')
async def authorized_another_client(
    client: AsyncClient,
    another_user: UserReadSchema,
    another_user_credentials: AuthCredentialsSchema,
) -> AsyncClient:
    response = await client.post('/login', json=another_user_credentials.model_dump())

    access_token = response.json()['access_token']
    client.headers['Authorization'] = access_token
    yield client
    client.headers.pop('Authorization')


@pytest_asyncio.fixture(scope='session')
async def project_repository(session) -> ProjectRepository:
    return ProjectRepository(session)


@pytest_asyncio.fixture(scope='function', loop_scope='session')
async def test_project(
    test_user: UserReadSchema,
    project_repository: ProjectRepository,
) -> ProjectReadSchema:
    project = await project_repository.create_project(
        user_id=test_user.user_id,
        project_data=ProjectCreateSchemaFactory(),
    )
    yield project
    await project_repository.delete_project(project.project_id)


@pytest_asyncio.fixture(scope='function', loop_scope='session')
async def created_projects(
    test_user: UserReadSchema,
    project_repository: ProjectRepository,
    dialogue_repository: DialogueRepository,
    request,
) -> list[ProjectReadSchema]:
    num_projects = getattr(request, 'param', 1)

    projects = []
    for _ in range(num_projects):
        project = await project_repository.create_project(
            user_id=test_user.user_id,
            project_data=ProjectCreateSchemaFactory(),
        )
        for _ in range(random.randint(0, 10)):
            await dialogue_repository.create_dialogue(
                project_id=project.project_id,
                dialogue_data=DialogueCreateSchemaFactory(),
            )

        project = await project_repository.get_project(project.project_id)
        projects.append(project)

    return projects


@pytest_asyncio.fixture(scope='session')
async def dialogue_repository(session) -> DialogueRepository:
    return DialogueRepository(session)


@pytest_asyncio.fixture(scope='function', loop_scope='session')
async def test_dialogue(
    test_project: ProjectReadSchema,
    dialogue_repository: DialogueRepository,
) -> DialogueReadSchema:
    dialogue = DialogueCreateSchemaFactory()
    dialogue = await dialogue_repository.create_dialogue(
        project_id=test_project.project_id,
        dialogue_data=dialogue,
    )
    yield dialogue
    await dialogue_repository.delete_dialogue(dialogue.dialogue_id)
