"""SQL запросы для таблицы Sflight."""

from datetime import date

from sqlalchemy import select

from app.cache import cache
from app.entities.sflight import SflightData
from app.exceptions import SflightNotFoundError
from app.models import Sairport, Sflight, Spfli
from app.repositories.base import Repository


class SflightRepository(Repository):
    """SQL запросы для таблицы Sflight."""
    async def get_sflight(self, carrid:str, connid:str, fldate:date) -> SflightData|None:
        """Выборка рейса по первичному ключу."""
        query = select(Sflight).where(
            Sflight.carrid == carrid,
            Sflight.connid == connid,
            Sflight.fldate == fldate )
        stmt = await self.session.execute(query)
        result = stmt.scalar_one_or_none()

        if result:
            SflightData(carrid = result.carrid,
                        connid = result.connid,
                        fldate = result.fldate,
                        av_seats = result.seatsmax - result.seatsocc)
        else:
            return None

    async def get_sflight_by_cities(self, from_city:str, to_city:str)->list[SflightData]:
        """Получение рейсов по городам отправления -> назначения."""
        #Найдем id аэропортов для выбранных городов
        q_from_airports = select(Sairport.id).where(Sairport.city == from_city)
        q_to_airports = select(Sairport.id).where(Sairport.city == to_city)

        #Найдем маршруты между аэропортами
        spfli_subq = select(Spfli).where(
            Spfli.airpfrom.in_(q_from_airports),
            Spfli.airpto.in_(q_to_airports)
        ).subquery()

        #Найдем полеты по этим маршрутам
        query = select(Sflight).join(
            spfli_subq,
            (Sflight.carrid == spfli_subq.c.carrid) &
            (Sflight.connid == spfli_subq.c.connid)
        )
        stmt = await self.session.execute(query)
        result = stmt.scalars().all()

        return [SflightData(carrid = it.carrid,
                            connid = it.connid,
                            fldate = it.fldate,
                            price = it.price,
                            currency = it.currency,
                            planetype = it.planetype,
                            seatsmax = it.seatsmax,
                            seatsocc = it.seatsocc,
                            av_seats = it.seatsmax - it.seatsocc) for it in result]

    async def get_av_seats(self, carrid:str, connid:str, fldate:date) -> int:
        """Получение количества свободных мест."""
        cache_key = f'{carrid}:{connid}:{fldate}'
        av_seats = cache.cache_get(cache_key)
        if av_seats:
            return int(av_seats)
        
        query = select(Sflight).where(
            Sflight.carrid == carrid,
            Sflight.connid == connid,
            Sflight.fldate == fldate )
        stmt = await self.session.execute(query)
        result = stmt.scalar_one_or_none()

        if result:
            av_seats = result.seatsmax - result.seatsocc
            cache.cache_set(cache_key, av_seats, 60 * 60 * 24)
            return av_seats
        else:
            raise SflightNotFoundError
        
    def create_sflight(self, sflight:SflightData) -> Sflight:
        """Создание записи в таблице Sflight."""
        new_sflight = Sflight(
            carrid = sflight.carrid,
            connid = sflight.connid,
            fldate = sflight.fldate,
            price = sflight.price,
            currency = sflight.currency,
            planetype = sflight.planetype,
            seatsmax = sflight.seatsmax,
            seatsocc = sflight.seatsocc,
        )
        self.session.add(new_sflight)

        return new_sflight
    
    def create_sflight_single(self, sflight:SflightData) -> Sflight:
        """Создание одной записи в таблице Sflight."""
        new_sflight = self.create_sflight(sflight)

        return new_sflight
    
    def create_sflight_list(self, sflight_list: list[SflightData]) -> list[Sflight]:
        """Создание одной записи в таблице Sflight."""
        result_list = [self.create_sflight(new_sflight) for new_sflight in sflight_list]
        self.session.add_all(result_list)

        return result_list