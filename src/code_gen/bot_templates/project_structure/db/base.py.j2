from datetime import datetime

import aiosqlite


class DatabaseConnector:
    def __init__(self, name):
        self.name = name
        self.conn = None

    async def connect(self):
        self.conn = await aiosqlite.connect(self.name)
        self.conn.row_factory = aiosqlite.Row

    async def close_connection(self):
        await self.conn.close()

    async def __aenter__(self):
        await self.connect()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_connection()


async def _create_user_table(db_connector: DatabaseConnector):
    async with db_connector as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                is_admin INTEGER DEFAULT 0,
                created_at DATE
            );
        ''')
        await conn.commit()


async def create_tables(db_connector: DatabaseConnector):
    await _create_user_table(db_connector)


async def add_user(
        db_connector: DatabaseConnector,
        tg_id: int,
        first_name: str,
        last_name: str,
        username: str,
        is_admin: bool,
):
    user = await get_user(db_connector, tg_id)

    if user is None:
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        async with db_connector as conn:
            await conn.execute(
                '''
                    INSERT INTO users (tg_id, first_name, last_name, username, is_admin, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (tg_id, first_name, last_name, username, is_admin, created_at)
            )
            await conn.commit()


async def get_user(db_connector: DatabaseConnector, tg_id: int):
    async with db_connector as conn:
        user = await conn.execute(
            '''
               SELECT * FROM users WHERE tg_id = ?
            ''',
            (tg_id,)
        )
        user = await user.fetchone()

    return user
