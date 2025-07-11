from datetime import datetime

from db.base import DatabaseConnector


async def _create_products_table(db_connector: DatabaseConnector):
    async with db_connector as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                description TEXT,
                price TEXT,
                image_path TEXT,
                seller_username TEXT,
                created_at DATE
            );
        ''')
        await conn.commit()


async def create_tables(db_connector: DatabaseConnector):
    await _create_products_table(db_connector)


async def get_products(db_connector: DatabaseConnector):
    async with db_connector as conn:
        products = await conn.execute(
            '''
                SELECT * FROM products
                ORDER BY product_id
            '''
        )
        products = await products.fetchall()

    return products


async def add_product(
        db_connector: DatabaseConnector,
        name: str,
        description: str,
        price: str,
        image_path: str,
        seller_username: str,
):
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    async with db_connector as conn:
        await conn.execute(
            '''
                INSERT INTO products (name, description, price, image_path, seller_username, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (name, description, price, image_path, seller_username, created_at)
        )
        await conn.commit()


async def delete_product(
        db_connector: DatabaseConnector,
        name: str,
):
    async with db_connector as conn:
        await conn.execute(
            '''
                DELETE FROM products
                WHERE name = ?
            ''',
            (name,)
        )
        await conn.commit()
