import asyncio
import os

from sqlalchemy import select

from src.apps.enums import TriggerEventType, AnswerMessageType, HTTPMethod
from src.apps.dialogues.models import DialogueModel, DialogueTriggerModel
from src.apps.blocks.models import TextBlockModel, QuestionBlockModel, ExcelBlockModel, APIBlockModel
from src.apps.dialogue_templates.models import DialogueTemplateModel
from src.infrastructure.db.sessions import async_session_maker


async def create():
    await create_survey_dialogue_template()
    await create_api_demo_dialogue_template()


async def create_survey_dialogue_template():
    async with async_session_maker() as session:
        existing_template = await session.execute(
            select(DialogueTemplateModel).where(DialogueTemplateModel.name == '✏️ Опрос')
        )
        existing_template = existing_template.scalar()

        if existing_template:
            return

        image_path = os.path.join('dialogue_templates', 'survey', 'cover.svg')
        readme_file_path = os.path.join('dialogue_templates', 'survey', 'README.md')

        trigger = DialogueTriggerModel(event_type=TriggerEventType.BUTTON, value='✏️ Опрос')

        dialogue = DialogueModel(trigger=trigger)

        blocks = [
            TextBlockModel(
                sequence_number=1,
                message_text='👋 Пройдите опрос',
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=2,
                message_text='✏️ Как вас зовут?',
                answer_type=AnswerMessageType.TEXT,
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=3,
                message_text='🔢 Сколько вам лет?',
                answer_type=AnswerMessageType.INT,
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=4,
                message_text='🧑‍💻 Кем вы работаете?',
                answer_type=AnswerMessageType.TEXT,
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=5,
                message_text='📞 Введите свой номер телефона',
                answer_type=AnswerMessageType.PHONE_NUMBER,
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=6,
                message_text='📧 Введите свою электронную почту',
                answer_type=AnswerMessageType.EMAIL,
                dialogue=dialogue,
            ),
            ExcelBlockModel(
                sequence_number=7,
                file_path='survey',
                data={
                    'name': '<answers[1]>',
                    'age': '<answers[2]>',
                    'job': '<answers[3]>',
                    'phone_number': '<answers[4]>',
                    'email': '<answers[5]>',
                },
                dialogue=dialogue,
            ),
            TextBlockModel(
                sequence_number=8,
                message_text='❤️ Благодарим за участие в опросе!',
                dialogue=dialogue,
            ),
        ]

        description = """
            <p>
                Шаблон опроса пользователей чат-бота для сбора следующей информации:
            </p>
            <ul>
                <li>имя</li>
                <li>возраст</li>
                <li>род деятельности</li>
                <li>номер телефона</li>
                <li>электронная почта</li>
            </ul>
            <p>
                Введенные пользователем данные будут сохранены в CSV файл под названием survey.csv
            </p>
        """

        template = DialogueTemplateModel(
            name='✏️ Опрос',
            summary='Пример как сделать опросник в чат-боте',
            description=description,
            dialogue=dialogue,
            image_path=image_path,
            readme_file_path=readme_file_path,
        )

        session.add(trigger)
        session.add(dialogue)
        for block in blocks:
            session.add(block)
        session.add(template)

        await session.commit()


async def create_api_demo_dialogue_template():
    async with async_session_maker() as session:
        existing_template = await session.execute(
            select(DialogueTemplateModel).where(DialogueTemplateModel.name == '🌐 Простой API-запрос')
        )
        existing_template = existing_template.scalar()

        if existing_template:
            return

        image_path = os.path.join('dialogue_templates', 'simple_api_request', 'cover.svg')
        readme_file_path = os.path.join('dialogue_templates', 'simple_api_request', 'README.md')

        trigger = DialogueTriggerModel(event_type=TriggerEventType.BUTTON, value='🌐 Простой API-запрос')

        dialogue = DialogueModel(trigger=trigger)

        blocks = [
            TextBlockModel(
                sequence_number=1,
                message_text='🌐 Демонстрация запроса к открытому API\nВведите имя — попробуем предсказать возраст.',
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=2,
                message_text='Как вас зовут?',
                answer_type=AnswerMessageType.TEXT,
                dialogue=dialogue,
            ),
            APIBlockModel(
                sequence_number=3,
                url='https://api.agify.io/?name=<answers[1]>',
                http_method=HTTPMethod.GET,
                headers={},
                body={},
                dialogue=dialogue,
            ),
            TextBlockModel(
                sequence_number=4,
                message_text='Имя: <answers[1]>\nПредполагаемый возраст: <response["age"]>\nСчетчик статистических данных: <response["count"]>',
                dialogue=dialogue,
            ),
            TextBlockModel(
                sequence_number=5,
                message_text='✅ Готово! Это пример работы API: ввод → запрос → ответ.',
                dialogue=dialogue,
            ),
        ]

        description = """
            <p>
                Шаблон демонстрирует, как отправлять запрос к открытому API и выводить результат с помощью
                плейсхолдера <code>&lt;response[...]&gt;</code>.
            </p>
            <p>
                Сценарий: пользователь вводит имя → отправляем GET на <code>agify.io</code> → выводим поля
                <code>age</code> и <code>count</code> из JSON-ответа.
            </p>
        """

        template = DialogueTemplateModel(
            name='🌐 Простой API-запрос',
            summary='Пример как отправить простой API-запрос',
            description=description,
            dialogue=dialogue,
            image_path=image_path,
            readme_file_path=readme_file_path,
        )

        session.add(trigger)
        session.add(dialogue)
        for block in blocks:
            session.add(block)
        session.add(template)

        await session.commit()


if __name__ == '__main__':
    asyncio.run(create())
