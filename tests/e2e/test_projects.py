import pytest
from httpx import AsyncClient

from src.apps.projects.repositories import ProjectRepository
from src.api.v1.projects.schemas import ProjectReadSchema
from src.apps.users.schemas import UserReadSchema
from tests.factories.projects import ProjectCreateSchemaFactory, ProjectUpdateSchemaFactory
from tests.utils.projects import assert_project_response


class TestProjectsApi:
    @pytest.mark.asyncio
    async def test_create_project_success(
        self,
        test_user: UserReadSchema,
        authorized_test_client: AsyncClient,
    ):
        project_data = ProjectCreateSchemaFactory()

        response = await authorized_test_client.post(
            '/projects',
            json=project_data.model_dump(mode='json'),
        )
        assert response.status_code == 201

        response_data = response.json()
        assert_project_response(
            response_data=response_data,
            expected_data=project_data,
            user_id=test_user.user_id,
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize('created_projects', [5], indirect=True)
    async def test_create_project_limit_exceeded(
        self,
        test_user: UserReadSchema,
        authorized_test_client: AsyncClient,
        created_projects: list[ProjectReadSchema],
    ):
        response = await authorized_test_client.post(
            '/projects',
            json=ProjectCreateSchemaFactory().model_dump(mode='json'),
        )

        assert response.status_code == 403
        assert response.json() == {'detail': 'Projects limit exceeded'}

    @pytest.mark.asyncio
    @pytest.mark.parametrize('created_projects', [5], indirect=True)
    async def test_get_projects_success(
        self,
        test_user: UserReadSchema,
        authorized_test_client: AsyncClient,
        project_repository: ProjectRepository,
        created_projects: list[ProjectReadSchema],
    ):
        response = await authorized_test_client.get('/projects')
        assert response.status_code == 200

        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == len(created_projects)

        for i, project_data in enumerate(created_projects):
            assert_project_response(
                response_data=response_data[i],
                expected_data=project_data,
                user_id=test_user.user_id,
            )

    @pytest.mark.asyncio
    async def test_get_projects_empty(self, authorized_test_client: AsyncClient):
        response = await authorized_test_client.get('/projects')
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_update_project_success(
        self,
        authorized_test_client: AsyncClient,
        test_project: ProjectReadSchema,
    ):
        update_data = ProjectUpdateSchemaFactory()

        response = await authorized_test_client.put(
            f'/projects/{test_project.project_id}',
            json=update_data.model_dump(mode='json'),
        )
        assert response.status_code == 200

        response_data = response.json()
        assert response_data['name'] == update_data.name
        assert response_data['start_message'] == update_data.start_message
        assert response_data['start_keyboard_type'] == update_data.start_keyboard_type.value

    @pytest.mark.asyncio
    async def test_update_project_no_permission(
        self,
        authorized_another_client: AsyncClient,
        test_project: ProjectReadSchema,
        project_repository: ProjectRepository,
    ):
        update_data = ProjectUpdateSchemaFactory()
        response = await authorized_another_client.put(
            f'/projects/{test_project.project_id}',
            json=update_data.model_dump(mode='json'),
        )

        assert response.status_code == 404
        assert response.json() == {'detail': 'Project does not exist'}

        project_after_update = await project_repository.get_project(test_project.project_id)
        assert test_project == project_after_update

    @pytest.mark.asyncio
    async def test_update_project_not_found(self, authorized_test_client: AsyncClient):
        update_data = ProjectUpdateSchemaFactory()
        response = await authorized_test_client.put(
            '/projects/999999',
            json=update_data.model_dump(mode='json'),
        )

        assert response.status_code == 404
        assert response.json() == {'detail': 'Project does not exist'}

    @pytest.mark.asyncio
    async def test_delete_project_success(
        self,
        authorized_test_client: AsyncClient,
        test_project: ProjectReadSchema,
        project_repository: ProjectRepository,
    ):
        response = await authorized_test_client.delete(
            f'/projects/{test_project.project_id}',
        )
        assert response.status_code == 204

        project = await project_repository.get_project(test_project.project_id)
        assert project is None

    @pytest.mark.asyncio
    async def test_delete_project_no_permission(
        self,
        authorized_another_client: AsyncClient,
        test_project: ProjectReadSchema,
    ):
        response = await authorized_another_client.delete(
            f'/projects/{test_project.project_id}',
        )
        assert response.status_code == 404
        assert response.json() == {'detail': 'Project does not exist'}

    @pytest.mark.asyncio
    async def test_delete_project_not_found(self, authorized_test_client: AsyncClient):
        response = await authorized_test_client.delete(
            '/projects/999999',
        )
        assert response.status_code == 404
        assert response.json() == {'detail': 'Project does not exist'}
