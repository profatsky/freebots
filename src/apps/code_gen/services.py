import io
import os
import zipfile
from pathlib import Path
from typing import Optional
from uuid import UUID

from jinja2 import Template, Environment, FileSystemLoader

from src.apps.dialogues.errors import DialoguesLimitExceededError
from src.apps.plugins.errors import PluginsNotAvailableForFreeUsersError
from src.apps.enums import (
    KeyboardType,
    HandlerType,
    BlockType,
    TriggerEventType,
    AnswerMessageType,
    HTTPMethod,
    AiohttpSessionMethod,
)
from src.api.v1.code_gen.schemas import HandlerSchema, StateSchema, StatesGroupSchema, KeyboardSchema
from src.apps.subscriptions.dependencies import SubscriptionServiceDI
from src.core.consts import MAX_DIALOGUES_WITH_FREE_PLAN
from src.infrastructure.db.dependencies import AsyncSessionDI
from src.apps.projects.dependencies.services_dependencies import ProjectServiceDI
from src.api.v1.projects.schemas import ProjectToGenerateCodeReadSchema
from src.apps.code_gen.bot_templates import code
from src.apps.blocks.utils import escape_inner_text

BOT_FILE_TEMPLATES_DIR = Path('src') / 'apps' / 'code_gen' / 'bot_templates' / 'project_structure'


# TODO: create repositories layer
class CodeGenService:
    def __init__(
        self,
        session: AsyncSessionDI,
        project_service: ProjectServiceDI,
        subscription_service: SubscriptionServiceDI,
    ):
        self._session = session
        self._project_service = project_service
        self._subscription_service = subscription_service

    async def get_bot_code_in_zip(self, user_id: UUID, project_id: int) -> io.BytesIO:
        project = await self._project_service.get_project_to_generate_code(user_id=user_id, project_id=project_id)

        active_subscription = await self._subscription_service.get_active_subscription(user_id)
        if active_subscription is None:
            if project.plugins:
                raise PluginsNotAvailableForFreeUsersError
            if len(project.dialogues) > MAX_DIALOGUES_WITH_FREE_PLAN:
                raise DialoguesLimitExceededError

        zip_data = io.BytesIO()
        # TODO: anyio.to_thread
        with zipfile.ZipFile(zip_data, mode='w') as zipf:
            self._add_custom_handlers_code_to_zip(project, zipf)
            self._add_plugins_code_to_zip(project, zipf)
            self._add_images_to_zip(project, zipf)

            template_paths = [
                'main.py.j2',
                'loader.py.j2',
                'config.py.j2',
                Path('db/base.py.j2'),
                'middlewares.py.j2',
                '.env.example',
                'requirements.txt',
                'Dockerfile',
                'ИНСТРУКЦИЯ.txt',
            ]
            for path in template_paths:
                zipf.write(BOT_FILE_TEMPLATES_DIR / path, str(path).removesuffix('.j2'))

        zip_data.seek(0)
        return zip_data

    # TODO refactoring
    def _add_plugins_code_to_zip(self, project: ProjectToGenerateCodeReadSchema, zip_file: zipfile.ZipFile):
        handlers_file_names = []
        db_funcs_file_names = []

        for plugin in project.plugins:
            # handlers
            handlers_file_name = os.path.basename(plugin.handlers_file_path)
            handlers_file_name_with_py_extension = os.path.splitext(handlers_file_name)[0]

            handlers_file_name_without_extension = os.path.splitext(handlers_file_name_with_py_extension)[0]
            handlers_file_names.append(handlers_file_name_without_extension)

            handlers_file_path = os.path.join('src', 'apps', plugin.handlers_file_path)
            zip_file.write(handlers_file_path, os.path.join('handlers', handlers_file_name_with_py_extension))

            # database funcs
            db_funcs_file_name = os.path.basename(plugin.handlers_file_path)
            db_funcs_file_name_with_py_extension = os.path.splitext(db_funcs_file_name)[0]

            db_funcs_file_name_without_extension = os.path.splitext(db_funcs_file_name_with_py_extension)[0]
            db_funcs_file_names.append(db_funcs_file_name_without_extension)

            db_funcs_file_path = os.path.join('src', 'apps', plugin.db_funcs_file_path)
            zip_file.write(db_funcs_file_path, os.path.join('db', db_funcs_file_name_with_py_extension))

        handlers_init_template = self._get_template(os.path.join(BOT_FILE_TEMPLATES_DIR, 'handlers', '__init__.py.j2'))
        handlers_init_code = handlers_init_template.render(
            {
                'handlers_file_names': handlers_file_names,
            }
        )
        handlers_init_in_memory_file = io.BytesIO(str.encode(handlers_init_code))
        zip_file.writestr(os.path.join('handlers', '__init__.py'), handlers_init_in_memory_file.getvalue())

        db_funcs_init_template = self._get_template(os.path.join(BOT_FILE_TEMPLATES_DIR, 'db', '__init__.py.j2'))
        db_funcs_init_code = db_funcs_init_template.render(
            {
                'db_funcs_file_names': db_funcs_file_names,
            }
        )
        db_funcs_init_in_memory_file = io.BytesIO(str.encode(db_funcs_init_code))
        zip_file.writestr(os.path.join('db', '__init__.py'), db_funcs_init_in_memory_file.getvalue())

    @staticmethod
    def _add_images_to_zip(project: ProjectToGenerateCodeReadSchema, zip_file: zipfile.ZipFile):
        for dialogue in project.dialogues:
            for block in dialogue.blocks:
                if block.type == BlockType.IMAGE_BLOCK.value:
                    image_path = os.path.join('src', 'media', block.image_path)
                    zip_file.write(image_path, os.path.join('img', os.path.basename(block.image_path)))

    def _add_custom_handlers_code_to_zip(self, project: ProjectToGenerateCodeReadSchema, zip_file: zipfile.ZipFile):
        custom_handlers_code = self._generate_custom_handlers_code(project)
        custom_handlers_in_memory_file = io.BytesIO(str.encode(custom_handlers_code))
        zip_file.writestr(os.path.join('handlers', 'custom.py'), custom_handlers_in_memory_file.getvalue())

    # TODO refactoring
    # TODO add customize env variables
    # TODO change start func call
    def _generate_custom_handlers_code(self, project: ProjectToGenerateCodeReadSchema) -> str:
        utils_funcs = set()
        states_groups: list[StatesGroupSchema] = []
        handlers: list[HandlerSchema] = []
        commands_values: list[str] = []

        start_keyboard = self._get_start_keyboard(project.start_keyboard_type)

        for dialogue in project.dialogues:
            if not dialogue.trigger.value:
                continue

            states_group = None

            handler = HandlerSchema()
            handler.signature = code.func_signature_for_common_handler_with_msg.format(
                trigger_event_type=dialogue.trigger.event_type.value,
                dialogue_id=dialogue.dialogue_id,
            )

            if dialogue.trigger.event_type == TriggerEventType.COMMAND:
                commands_values.append(dialogue.trigger.value)
                handler.decorator = code.command_decorator.format(trigger_value=dialogue.trigger.value)

            elif dialogue.trigger.event_type == TriggerEventType.BUTTON:
                if project.start_keyboard_type == KeyboardType.INLINE_KEYBOARD:
                    start_keyboard.add_to_buttons(code.inline_keyboard_button.format(text=dialogue.trigger.value))
                    handler.decorator = code.callback_button_decorator.format(trigger_value=dialogue.trigger.value)
                    handler.signature = code.func_signature_for_callback_handler_with_callback.format(
                        trigger_event_type=dialogue.trigger.event_type.value,
                        dialogue_id=dialogue.dialogue_id,
                    )
                    handler.type = HandlerType.CALLBACK
                    handler.add_to_body(code.callback_answer)
                    handler.add_to_body(code.callback_message)
                else:
                    start_keyboard.add_to_buttons(code.reply_keyboard_button.format(text=dialogue.trigger.value))
                    handler.decorator = code.text_button_decorator.format(trigger_value=dialogue.trigger.value)

            elif dialogue.trigger.event_type == TriggerEventType.TEXT:
                handler.decorator = code.text_decorator.format(trigger_value=dialogue.trigger.value)

            if not dialogue.blocks:
                handler.add_to_body('pass')

            dialogue_blocks = sorted(dialogue.blocks, key=lambda x: x.sequence_number)
            for block in dialogue_blocks:
                if block.is_draft:
                    continue

                if block.type == BlockType.TEXT_BLOCK.value:
                    handler.add_to_body(code.message_answer.format(message_text=escape_inner_text(block.message_text)))

                elif block.type == BlockType.IMAGE_BLOCK.value:
                    image_path_in_bot_project = os.path.join('img/', os.path.basename(block.image_path))
                    handler.add_to_body(code.image_block.format(image_path=image_path_in_bot_project))

                elif block.type == BlockType.QUESTION_BLOCK.value:
                    if states_group is None:
                        state = StateSchema(name=f'state_from_block{block.sequence_number}')
                        states_group = StatesGroupSchema(name=f'StatesGroup{len(states_groups) + 1}', states=[state])
                        states_groups.append(states_group)

                        handler.add_to_body(
                            code.message_answer_with_reply_kb_remove.format(
                                message_text=escape_inner_text(block.message_text)
                            )
                        )

                        handler.add_to_body(
                            code.set_state.format(states_group_name=states_group.name, state_name=state.name)
                        )

                        if handler.type == HandlerType.CALLBACK:
                            handler.signature = code.func_signature_for_callback_handler_with_callback_and_state.format(
                                trigger_event_type=dialogue.trigger.event_type.value,
                                dialogue_id=dialogue.dialogue_id,
                            )
                        elif handler.type == HandlerType.MESSAGE:
                            handler.signature = code.func_signature_for_common_handler_with_msg_and_state.format(
                                trigger_event_type=dialogue.trigger.event_type.value,
                                dialogue_id=dialogue.dialogue_id,
                            )

                        handlers.append(handler)
                    else:
                        state = StateSchema(name=f'state_from_block{block.sequence_number}')
                        states_groups[-1].states.append(state)

                        handler.add_to_body(
                            code.message_answer_with_reply_kb_remove.format(
                                message_text=escape_inner_text(block.message_text)
                            )
                        )
                        handler.add_to_body(
                            code.set_state.format(states_group_name=states_group.name, state_name=state.name)
                        )
                        handlers.append(handler)

                    handler = HandlerSchema()
                    handler.decorator = code.state_decorator.format(
                        states_group_name=states_group.name,
                        state_name=state.name,
                    )
                    handler.signature = code.func_signature_for_state_handler_with_msg_and_state.format(
                        state_name=state.name,
                        dialogue_id=dialogue.dialogue_id,
                    )

                    answer_type_check_code = self._get_answer_type_check_code(block.answer_type)
                    if answer_type_check_code is not None:
                        handler.add_to_body(answer_type_check_code)

                    utils_func_code_for_answer_type_check = self._get_utils_func_code_for_answer_type_check(
                        block.answer_type
                    )
                    if utils_func_code_for_answer_type_check is not None:
                        utils_funcs.add(utils_func_code_for_answer_type_check)

                    handler.add_to_body(code.update_state_data.format(answer_num=len(states_group.states)))
                    handler.add_to_body(code.get_state_data)

                elif block.type == BlockType.EMAIL_BLOCK.value:
                    handler.add_to_body(
                        code.email_block.format(
                            recipient_email=escape_inner_text(block.recipient_email),
                            subject=escape_inner_text(block.subject),
                            text=escape_inner_text(block.text),
                        )
                    )

                    utils_funcs.add(code.send_email.strip())
                    utils_funcs.add(code.is_answer_from_user.strip())

                elif block.type == BlockType.CSV_BLOCK.value:
                    handler.add_to_body(
                        code.csv_block.format(
                            file_path=block.file_path,
                            data=block.data,
                        )
                    )

                elif block.type == BlockType.EXCEL_BLOCK.value:
                    handler.add_to_body(
                        code.excel_block.format(
                            file_path=block.file_path,
                            data=block.data,
                        )
                    )

                elif block.type == BlockType.API_BLOCK.value:
                    aiohttp_session_method = self._get_aiohttp_session_method(block.http_method)

                    handler.add_to_body(
                        code.api_block.format(
                            aiohttp_session_method=aiohttp_session_method.value,
                            url=block.url,
                            headers=block.headers,
                            body=block.body,
                        )
                    )

            if states_group:
                handler.add_to_body(code.clear_state)

            handler.add_to_body(code.call_start_func)
            handlers.append(handler)

        admin_keyboard = self._get_start_keyboard(project.start_keyboard_type)
        for plugin in project.plugins:
            for trigger in plugin.triggers:
                if trigger.event_type == TriggerEventType.BUTTON:
                    if trigger.is_admin:
                        keyboard = admin_keyboard
                    else:
                        keyboard = start_keyboard

                    if project.start_keyboard_type == KeyboardType.INLINE_KEYBOARD:
                        keyboard.add_to_buttons(code.inline_keyboard_button.format(text=trigger.value))
                    else:
                        keyboard.add_to_buttons(code.reply_keyboard_button.format(text=trigger.value))

        template = self._get_template(os.path.join(BOT_FILE_TEMPLATES_DIR, 'handlers', 'custom.py.j2'))
        bot_code = template.render(
            {
                'utils_funcs': utils_funcs,
                'states_groups': states_groups,
                'handlers': handlers,
                'commands_values': commands_values,
                'start_keyboard': start_keyboard,
                'admin_keyboard': admin_keyboard,
                'start_message': escape_inner_text(project.start_message) if project.start_message else 'Главное меню',
            }
        )
        return bot_code

    @staticmethod
    def _get_start_keyboard(keyboard_type: KeyboardType) -> KeyboardSchema:
        if keyboard_type == KeyboardType.INLINE_KEYBOARD:
            declaration = code.inline_keyboard_declaration
        else:
            declaration = code.reply_keyboard_declaration
        return KeyboardSchema(type=keyboard_type, declaration=declaration)

    @staticmethod
    def _get_answer_type_check_code(
        answer_type: AnswerMessageType,
    ) -> Optional[str]:
        types_to_code = {
            AnswerMessageType.ANY: None,
            AnswerMessageType.TEXT: code.answer_text_type_check,
            AnswerMessageType.INT: code.answer_int_type_check,
            AnswerMessageType.EMAIL: code.answer_email_type_check,
            AnswerMessageType.PHONE_NUMBER: code.answer_phone_number_type_check,
        }
        return types_to_code[answer_type]

    @staticmethod
    def _get_utils_func_code_for_answer_type_check(
        answer_type: AnswerMessageType,
    ) -> Optional[str]:
        types_to_code = {
            AnswerMessageType.ANY: None,
            AnswerMessageType.TEXT: None,
            AnswerMessageType.INT: None,
            AnswerMessageType.EMAIL: code.is_email.strip(),
            AnswerMessageType.PHONE_NUMBER: code.is_phone_number.strip(),
        }
        return types_to_code[answer_type]

    @staticmethod
    def _get_aiohttp_session_method(
        http_method: HTTPMethod,
    ) -> AiohttpSessionMethod:
        http_methods_to_aiohttp_methods = {
            http_method.GET: AiohttpSessionMethod.GET,
            http_method.POST: AiohttpSessionMethod.POST,
            http_method.PUT: AiohttpSessionMethod.PUT,
            http_method.DELETE: AiohttpSessionMethod.DELETE,
            http_method.PATCH: AiohttpSessionMethod.PATCH,
            http_method.CONNECT: AiohttpSessionMethod.CONNECT,
            http_method.HEAD: AiohttpSessionMethod.HEAD,
            http_method.OPTIONS: AiohttpSessionMethod.OPTIONS,
        }
        return http_methods_to_aiohttp_methods[http_method]

    @staticmethod
    def _get_template(file_path: str) -> Template:
        with open(file_path, 'r', encoding='utf-8') as f:
            template_str = f.read()

        env = Environment(
            loader=FileSystemLoader(os.path.join('src', 'code_gen', 'bot_templates')),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        return env.from_string(template_str)
