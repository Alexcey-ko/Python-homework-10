"""Базовый класс репозитория."""

from sqlalchemy.ext.asyncio import AsyncSession


class Repository():
    """Базовый клсс для классов Repository."""

    def __init__(self, session: AsyncSession):
        """Инициализация объекта."""
        self.session = session