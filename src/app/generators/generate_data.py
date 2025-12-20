"""Модуль, содержащий инструменты для генерации случайных данных в БД."""

import asyncio

import app.generators as gens
import app.repositories as repo
from app.cache import cache
from app.database import async_session


async def generate_all(airp_n: int = 5, carr_n: int = 5, cust_n: int = 5, spfli_n: int = 5, sflight_n: int = 5, sbook_n: int = 5):
    """Генерация данных для всех таблиц и коммит в БД."""
    async with async_session() as session:
        #Для SCARR, SCUSTOM, SAIRPORT: id генерируется на стороне БД, поэтому мы
        #получаем обновленные списки после добавления и flush в БД

        #Генерация клиентов и добавление в БД
        scustom_repo = repo.ScustomRepository(session)
        scustom_list = await scustom_repo.create_scustom_list(gens.generate_scustom(cust_n))

        #Генерация перевозчиков и добавление в БД
        scarr_repo = repo.ScarrRepository(session)
        scarr_list = await scarr_repo.create_scarr_list(gens.generate_scarr(carr_n))

        #Генерация аэропортов и добавление в БД
        sairport_repo = repo.SairportRepository(session)
        sairport_list = await sairport_repo.create_sairport_list(gens.generate_sairport(airp_n))

        #Генерация маршрутов и добавление в БД
        spfli_repo = repo.SpfliRepository(session)
        spfli_list = await spfli_repo.create_spfli_list(gens.generate_spfli(scarr_list, sairport_list, spfli_n))

        #Генерация рейсов и добавление в БД
        sflight_repo = repo.SflightRepository(session, cache)
        sflight_list = await sflight_repo.create_sflight_list(gens.generate_sflight(spfli_list, sflight_n))

        #Генерация бронирований и добавление в БД
        sbook_repo = repo.SbookRepository(session, cache)
        await sbook_repo.create_sbook_list(gens.generate_sbook(sflight_list, scustom_list, sbook_n))
        
        #Кэширование свободных мест
        for item in sflight_list:
            cache.cache_set(f'{item.carrid}:{item.connid}:{item.fldate}', item.seatsmax - item.seatsocc, 60 * 60 * 24)

        #Коммит таблиц в БД
        await session.commit()

if __name__ == '__main__':
    asyncio.run(generate_all(4, 5, 5, 25, 75, 20))