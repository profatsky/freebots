from src.infrastructure.db.dependencies import AsyncSessionDI


class BaseRepository:
    def __init__(self, session: AsyncSessionDI):
        self._session = session
