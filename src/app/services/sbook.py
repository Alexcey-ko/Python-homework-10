"""Функции для работы с бронированием."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import ScustomAuth, SflightData
from app.repositories.sbook import SbookRepository


class SbookService:
    """Класс-сервис бронирований."""
    def __init__(self, session: AsyncSession):
        """Инициализация сервиса."""
        self.session = session
        self.sbook_repo = SbookRepository(self.session)

    async def book_flight(self, sfl:SflightData, scust:ScustomAuth, seats:int):
        """Бронирование выбранного рейса."""
        return await self.sbook_repo.book_flight(sfl, scust, seats)