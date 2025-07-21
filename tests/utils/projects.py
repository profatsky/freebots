from src.projects.schemas import ProjectCreateSchema, ProjectReadSchema


def assert_project_response(response_data: dict, expected_data: ProjectCreateSchema | ProjectReadSchema, user_id: int):
    assert 'project_id' in response_data
    assert 'created_at' in response_data
    assert response_data['name'] == expected_data.name
    assert response_data['user_id'] == user_id
    assert response_data['start_message'] == expected_data.start_message
    assert response_data['start_keyboard_type'] == expected_data.start_keyboard_type.value
    if not isinstance(expected_data, ProjectCreateSchema):
        assert response_data['dialogues'] == [dialogue.model_dump(mode='json') for dialogue in expected_data.dialogues]
