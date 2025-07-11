import asyncio
import os

from sqlalchemy import select

from src.core.db import async_session_maker
from src.plugins.models import PluginModel
from src.plugins.schemas import PluginCreateSchema


async def create():
    await create_statistics_plugin()
    await create_catalog_plugin()
    await create_support_plugin()


async def _create_plugin(plugin: PluginCreateSchema):
    async with async_session_maker() as session:
        existing_plugin = await session.execute(
            select(PluginModel)
            .where(PluginModel.name == plugin.name)
        )
        existing_plugin = existing_plugin.scalar()

        if existing_plugin is None:
            plugin = PluginModel(
                name=plugin.name,
                summary=plugin.summary,
                description=plugin.description,
                image_path=plugin.image_path,
                handlers_file_path=plugin.handlers_file_path,
                db_funcs_file_path=plugin.db_funcs_file_path,
            )

            session.add(plugin)
            await session.commit()


async def create_statistics_plugin():
    description = '''
        <p>
            Плагин Статистика предоставляет информацию о количестве пользователей вашего чат-бота.
        </p>
        <p>
            Администратор чат-бота может просматривать статистику с помощью команды <code>/stats</code>.
        </p>
    '''

    image_path = os.path.join('plugins', 'statistic.png')
    handlers_file_path = os.path.join('code_gen', 'bot_templates', 'project_structure', 'handlers', 'statistic.py.j2')
    db_funcs_file_path = os.path.join('code_gen', 'bot_templates', 'project_structure', 'db', 'statistic.py.j2')

    plugin = PluginCreateSchema(
        name='Статистика',
        summary='Предоставляет статистику по пользователям чат-бота',
        description=description,
        image_path=image_path,
        handlers_file_path=handlers_file_path,
        db_funcs_file_path=db_funcs_file_path,
    )

    await _create_plugin(plugin)


async def create_catalog_plugin():
    description = '''
        <p>
            Плагин Каталог добавляет в чат-бота функционал каталога товаров (услуг).
        </p>
        <p>
            Каждый товар содержит следующую информацию:
        </p>
        <ul>
            <li>название</li>
            <li>описание</li>
            <li>цена</li>
            <li>изображение</li>
            <li>ссылка на Telegram продавца</li>
        </ul>
        <p>
            Пользователи чат-бота могут просматривать каталог товаров с помощью команды <code>/catalog</code>. 
            Администратор чат-бота может добавлять новые товары в каталог с помощью команды <code>/add_product</code> 
            и удалять имеющиеся во время просмотра каталога.
        </p>
    '''

    image_path = os.path.join('plugins', 'catalog.png')
    handlers_file_path = os.path.join('code_gen', 'bot_templates', 'project_structure', 'handlers', 'catalog.py.j2')
    db_funcs_file_path = os.path.join('code_gen', 'bot_templates', 'project_structure', 'db', 'catalog.py.j2')

    plugin = PluginCreateSchema(
        name='Каталог',
        summary='Готовое решение для продажи товаров и услуг',
        description=description,
        image_path=image_path,
        handlers_file_path=handlers_file_path,
        db_funcs_file_path=db_funcs_file_path,
    )

    await _create_plugin(plugin)


async def create_support_plugin():
    description = '''
        <p>
            Плагин Техническая поддержка добавляет в чат-бота функционал технической поддержки. 
        </p>
        <p>
            Каждый пользователь может создать обращение в техническую поддержку, отправив интересующий его вопрос с 
            помощью команды <code>/support</code>.
        </p>
        <p>
            Администратор чат-бота может просмотреть список обращений с помощью команды <code>/requests</code> и 
            отправить пользователю ответ с помощью команды <code>/answer</code>. С помощью команды 
            <code>/setadmin</code> можно назначить администратора, а с помощью <code>/unsetadmin</code> разжаловать. 
            С помощью команды <code>/connect</code> администратор может подключиться к чату пользователя и отправлять 
            сообщения от имени чат-бота.
        </p>
    '''

    image_path = os.path.join('plugins', 'support.png')
    handlers_file_path = os.path.join('code_gen', 'bot_templates', 'project_structure', 'handlers', 'support.py.j2')
    db_funcs_file_path = os.path.join('code_gen', 'bot_templates', 'project_structure', 'db', 'support.py.j2')

    plugin = PluginCreateSchema(
        name='Тех. поддержка',
        summary='Готовый функционал для технической поддержки',
        description=description,
        image_path=image_path,
        handlers_file_path=handlers_file_path,
        db_funcs_file_path=db_funcs_file_path,
    )

    await _create_plugin(plugin)


if __name__ == '__main__':
    asyncio.run(create())
