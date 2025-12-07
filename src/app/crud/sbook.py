"""SQL запросы для таблицы SFLIGHT."""

from sqlalchemy import func, select

from app.crud.sflight import get_av_seats
from app.db import session
from app.db.cache import cache
from app.db.models import Sbook, Scustom, Sflight


def book_flight(sflight:Sflight, scustom:Scustom, seats:int):
    """Бронирование мест."""
    if seats > get_av_seats(sflight):
        print('В рейсе недостаточно свободных мест.')
        return
    stmt = select(func.max(Sbook.bookid)).where(
        Sbook.carrid == sflight.carrid, 
        Sbook.connid == sflight.connid,
        Sbook.fldate == sflight.fldate)
    max_bookid = session.execute(stmt).scalar_one_or_none()
    if not max_bookid:
        max_bookid = 1

    #Менеяем количество занятых мест в рейсе
    sflight.seatsocc += seats
    session.add(sflight)
    #Подсчет свободных мест
    cache_key = f'{sflight.carrid}:{sflight.connid}:{sflight.fldate}'
    av_seats = sflight.seatsmax - sflight.seatsocc
    #Добавляем запись бронирования
    sbook = Sbook(
        carrid = sflight.carrid,
        connid = sflight.connid,
        fldate = sflight.fldate,
        customid = scustom.id,
        bookid = max_bookid + 1,
        seats = seats
    )
    session.add(sbook)
    session.commit()

    cache.cache_set(cache_key, av_seats, 60 * 60 * 24)
    
    return sbook