"""SQL запросы для таблицы Sbook."""

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.entities import SbookData, ScustomAuth, SflightData
from app.models import Sbook, Sflight
from app.repositories.base import Repository
from app.repositories.sflight import SflightRepository


class SbookRepository(Repository):
    """SQL запросы для таблицы Sbook."""
    def __init__(self, session: AsyncSession) -> None:
        """Инициализация объекта."""
        super().__init__(session)
        self.sflight_repo = SflightRepository(self.session)

    async def book_flight(self, sfl:SflightData, scust:ScustomAuth, seats:int) -> bool:
        """Бронирование мест."""
        #Проверка свободных мест
        if seats > await self.sflight_repo.get_av_seats(sfl.carrid, sfl.connid, sfl.fldate):
            print('В рейсе недостаточно свободных мест.')
            return

        #Выборка Sflight для изменения занятых мест
        sflight_query = select(Sflight).where(
            Sflight.carrid == sfl.carrid,
            Sflight.connid == sfl.connid,
            Sflight.fldate == sfl.fldate,
            )
        sflight_stmt = await self.session.execute(sflight_query)
        sflight:Sflight|None = sflight_stmt.scalar_one_or_none()
        
        #Получение максимального bookid для данного рейса
        max_bookid_query = select(func.max(Sbook.bookid)).where(
            Sbook.carrid == sflight.carrid, 
            Sbook.connid == sflight.connid,
            Sbook.fldate == sflight.fldate)
        max_bookid_stmt = await self.session.execute(max_bookid_query)
        max_bookid = max_bookid_stmt.scalar_one_or_none()
        if not max_bookid:
            max_bookid = 1

        #Изменение количества занятых мест в рейсе
        sflight.seatsocc += seats
        self.session.add(sflight)
        #Подсчет количества свободных мест
        cache_key = f'{sflight.carrid}:{sflight.connid}:{sflight.fldate}'
        av_seats = sflight.seatsmax - sflight.seatsocc
        #Добавление записи бронирования
        sbook = Sbook(
            carrid = sflight.carrid,
            connid = sflight.connid,
            fldate = sflight.fldate,
            customid = scust.id,
            bookid = max_bookid + 1,
            seats = seats
        )
        self.session.add(sbook)

        try:
            await self.session.commit()
            cache.cache_set(cache_key, av_seats, 60 * 60 * 24)
            return True
        except SQLAlchemyError:
            await self.session.rollback()
            return False
        
    def create_sbook(self, sbook:SbookData) -> Sbook:
        """Создание записи в таблице Sbook."""
        new_sbook = Sbook(
            carrid = sbook.carrid,
            connid = sbook.connid,
            fldate = sbook.fldate,
            bookid = sbook.bookid,
            customid = sbook.customid,
            seats = sbook.seats,
        )
        self.session.add(new_sbook)

        return new_sbook

    def create_sbook_single(self, sbook:SbookData) -> Sbook:
        """Создание одной записи в таблице Sbook."""
        new_sbook = self.create_sbook(sbook)

        return new_sbook
    
    def create_sbook_list(self, sbook_list: list[SbookData]) -> list[Sbook]:
        """Создание одной записи в таблице Sbook."""
        result_list = [self.create_sbook(new_sbook) for new_sbook in sbook_list]
        self.session.add_all(result_list)

        return result_list
    