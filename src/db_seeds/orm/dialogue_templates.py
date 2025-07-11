import asyncio

from sqlalchemy import select

from src.core.db import async_session_maker
from src.enums import TriggerEventType, AnswerMessageType
from src.dialogues.models import DialogueModel, TriggerModel
from src.blocks.models import TextBlockModel, QuestionBlockModel, CSVBlockModel
from src.dialogue_templates.models import DialogueTemplateModel


async def create():
    await create_survey_dialogue_template()


async def create_survey_dialogue_template():
    async with async_session_maker() as session:
        existing_template = await session.execute(
            select(DialogueTemplateModel)
            .where(DialogueTemplateModel.name == 'Опрос')
        )
        existing_template = existing_template.scalar()

        if existing_template:
            return

        trigger = TriggerModel(
            event_type=TriggerEventType.TEXT,
            value='Опрос'
        )

        dialogue = DialogueModel(
            trigger=trigger
        )

        blocks = [
            TextBlockModel(
                sequence_number=1,
                message_text='Пройдите опрос',
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=2,
                message_text='Как вас зовут?',
                answer_type=AnswerMessageType.TEXT,
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=3,
                message_text='Сколько вам лет?',
                answer_type=AnswerMessageType.INT,
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=4,
                message_text='Кем вы работаете?',
                answer_type=AnswerMessageType.TEXT,
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=5,
                message_text='Введите свой номер телефона',
                answer_type=AnswerMessageType.PHONE_NUMBER,
                dialogue=dialogue,
            ),
            QuestionBlockModel(
                sequence_number=6,
                message_text='Введите свою электронную почту',
                answer_type=AnswerMessageType.EMAIL,
                dialogue=dialogue,
            ),
            CSVBlockModel(
                sequence_number=7,
                file_path='survey',
                data={
                    'name': '<answers[1]>',
                    'age': '<answers[2]>',
                    'job': '<answers[3]>',
                    'phone_number': '<answers[4]>',
                    'email': '<answers[5]>'
                },
                dialogue=dialogue,
            ),
            TextBlockModel(
                sequence_number=8,
                message_text='Благодарим за участие в опросе!',
                dialogue=dialogue,
            ),
        ]

        description = '''
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
        '''

        template = DialogueTemplateModel(
            name='Опрос',
            summary='Сбор и сохранение данных от пользователей чат-бота',
            description=description,
            dialogue=dialogue,
            image_path='dialogue_templates/survey.png',
        )

        session.add(trigger)
        session.add(dialogue)
        for block in blocks:
            session.add(block)
        session.add(template)

        await session.commit()


if __name__ == '__main__':
    asyncio.run(create())
