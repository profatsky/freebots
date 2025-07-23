from src.core import settings


def get_dsn(
    prefix: str,
    user=settings.DB_USER,
    password=settings.DB_PASS,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
) -> str:
    return '{prefix}://{user}:{password}@{host}:{port}/{database}'.format(
        prefix=prefix,
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
    )
