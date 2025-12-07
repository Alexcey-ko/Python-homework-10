"""SQL запросы для таблицы SFLIGHT."""

from sqlalchemy import select

from app.db import session
from app.db.cache import cache
from app.db.models import Sairport, Sflight, Spfli


def get_sflight_by_cities(from_city:str, to_city:str)->list[Sflight]:
    """Выбор клиента по email."""
    #Найдем id аэропортов для выбранных городов
    from_airports = select(Sairport.id).where(Sairport.city == from_city)
    to_airports = select(Sairport.id).where(Sairport.city == to_city)

    #Найдем маршруты между аэропортами
    spfli_subq = select(Spfli).where(
        Spfli.airpfrom.in_(from_airports),
        Spfli.airpto.in_(to_airports)
    ).subquery()

    #Найдем полеты по этим маршрутам
    stmt = select(Sflight).join(
        spfli_subq,
        (Sflight.carrid == spfli_subq.c.carrid) &
        (Sflight.connid == spfli_subq.c.connid)
    )

    flights = session.execute(stmt).scalars().all()
    return flights

def get_av_seats(sflight:Sflight):
    """Получение количества свободных мест."""
    cache_key = f'{sflight.carrid}:{sflight.connid}:{sflight.fldate}'
    av_seats = int(cache.cache_get(cache_key))
    if av_seats:
        return av_seats
    
    av_seats = sflight.seatsmax - sflight.seatsocc
    cache.cache_set(cache_key, av_seats, 60 * 60 * 24)
    return av_seats