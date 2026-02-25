import asyncio
from pathlib import Path

from sqlalchemy import select

from src.apps.enums import TriggerEventType
from src.infrastructure.db.sessions import async_session_maker
from src.apps.plugins.models import PluginModel, PluginTriggerModel
from src.api.v1.plugins.schemas import PluginCreateSchema, PluginTriggerCreateSchema


async def create():
    await create_statistics_plugin()
    await create_catalog_plugin()
    await create_support_plugin()


async def _create_plugin(plugin: PluginCreateSchema):
    async with async_session_maker() as session:
        existing_plugin = await session.execute(select(PluginModel).where(PluginModel.name == plugin.name))
        existing_plugin = existing_plugin.scalar()

        if existing_plugin is None:
            triggers = [
                PluginTriggerModel(
                    event_type=trigger.event_type,
                    value=trigger.value,
                    is_admin=trigger.is_admin,
                )
                for trigger in plugin.triggers
            ]

            plugin = PluginModel(
                name=plugin.name,
                summary=plugin.summary,
                image_path=str(plugin.image_path),
                handlers_file_path=str(plugin.handlers_file_path),
                db_funcs_file_path=str(plugin.db_funcs_file_path),
                readme_file_path=str(plugin.readme_file_path),
                triggers=triggers,
            )

            session.add(plugin)
            await session.commit()


async def create_statistics_plugin():
    image_path = Path('plugins', 'statistic', 'cover.svg')
    readme_file_path = Path('plugins', 'statistic', 'README.md')
    handlers_file_path = Path('handlers', 'statistic.py.j2')
    db_funcs_file_path = Path('db', 'statistic.py.j2')

    triggers = [
        PluginTriggerCreateSchema(event_type=TriggerEventType.BUTTON, value='📊 Статистика', is_admin=True),
    ]

    plugin = PluginCreateSchema(
        name='📊 Статистика',
        summary='Предоставляет статистику по пользователям чат-бота',
        image_path=image_path,
        handlers_file_path=handlers_file_path,
        db_funcs_file_path=db_funcs_file_path,
        readme_file_path=readme_file_path,
        triggers=triggers,
    )

    await _create_plugin(plugin)


async def create_catalog_plugin():
    image_path = Path('plugins', 'catalog', 'cover.svg')
    readme_file_path = Path('plugins', 'catalog', 'README.md')
    handlers_file_path = Path('handlers', 'catalog.py.j2')
    db_funcs_file_path = Path('db', 'catalog.py.j2')

    triggers = [
        PluginTriggerCreateSchema(event_type=TriggerEventType.BUTTON, value='🛍️ Каталог', is_admin=False),
        PluginTriggerCreateSchema(event_type=TriggerEventType.BUTTON, value='➕ Добавить товар', is_admin=True),
    ]

    plugin = PluginCreateSchema(
        name='🛍️ Каталог',
        summary='Готовое решение для продажи товаров и услуг',
        image_path=image_path,
        handlers_file_path=handlers_file_path,
        db_funcs_file_path=db_funcs_file_path,
        readme_file_path=readme_file_path,
        triggers=triggers,
    )

    await _create_plugin(plugin)


async def create_support_plugin():
    image_path = Path('plugins', 'support', 'cover.svg')
    readme_file_path = Path('plugins', 'support', 'README.md')
    handlers_file_path = Path('handlers', 'support.py.j2')
    db_funcs_file_path = Path('db', 'support.py.j2')

    triggers = [
        PluginTriggerCreateSchema(event_type=TriggerEventType.BUTTON, value='❓Тех.поддержка', is_admin=False),
        PluginTriggerCreateSchema(
            event_type=TriggerEventType.BUTTON, value='❓Обращения в тех.поддержку', is_admin=True
        ),
    ]

    plugin = PluginCreateSchema(
        name='❓ Тех. поддержка',
        summary='Готовый функционал для технической поддержки',
        image_path=image_path,
        handlers_file_path=handlers_file_path,
        db_funcs_file_path=db_funcs_file_path,
        readme_file_path=readme_file_path,
        triggers=triggers,
    )

    await _create_plugin(plugin)


if __name__ == '__main__':
    asyncio.run(create())
