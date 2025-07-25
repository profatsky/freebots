from src.infrastructure.db.seeds.orm.plugins import create as create_plugins
from src.infrastructure.db.seeds.orm.dialogue_templates import create as create_dialogue_templates

funcs = [
    create_plugins,
    create_dialogue_templates,
]


async def seed_database():
    for func in funcs:
        await func()
