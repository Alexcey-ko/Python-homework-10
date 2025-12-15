"""Модуль, содержащий инструменты для генерации случайных данных в БД."""

import asyncio

import app.entities as entities
import app.generators as gens
import app.repositories as repo
from app.cache import cache
from app.database import async_session


async def generate_all(airp_n: int = 5, carr_n: int = 5, cust_n: int = 5, spfli_n: int = 5, sflight_n: int = 5, sbook_n: int = 5):
    """Генерация данных для всех таблиц и коммит в БД."""
    async with async_session() as session:
        #Генерация клиентов и добавление в БД
        scustom_repo = repo.ScustomRepository(session)
        scustom_list = gens.generate_scustom(cust_n)
        scustom_list_orm = scustom_repo.create_scustom_list(scustom_list)

        #Генерация перевозчиков и добавление в БД
        scarr_repo = repo.ScarrRepository(session)
        scarr_list = gens.generate_scarr(carr_n)
        scarr_list_orm = scarr_repo.create_scarr_list(scarr_list)

        #Генерация аэропортов и добавление в БД
        sairport_repo = repo.SairportRepository(session)
        sairport_list = gens.generate_sairport(airp_n)
        sairport_list_orm = sairport_repo.create_sairport_list(sairport_list)
        #Генерация всех ID с автоинкрементом
        await session.flush()
        #Обновление списков с ID из БД
        scustom_list = [entities.ScustomData(
            id = scust_orm.id,
            email = scust_orm.email,
            phone_number = scust_orm.phone_number,
            name = scust_orm.name,
        ) for scust_orm in scustom_list_orm]
        scarr_list = [entities.ScarrData(
            carrid = scarr_orm.carrid,
            carrname = scarr_orm.carrname,
            carrcode = scarr_orm.carrcode,
            url = scarr_orm.url,
        ) for scarr_orm in scarr_list_orm]
        sairport_list = [entities.SairportData(
            id = sairport_orm.id,
            name = sairport_orm.name,
            timezone = sairport_orm.timezone,
            country = sairport_orm.country,
            city = sairport_orm.city,
        ) for sairport_orm in sairport_list_orm]

        #Генерация маршрутов и добавление в БД
        spfli_repo = repo.SpfliRepository(session)
        spfli_list = gens.generate_spfli(scarr_list, sairport_list, spfli_n)
        spfli_repo.create_spfli_list(spfli_list)
        await session.flush()

        #Генерация рейсов и добавление в БД
        sflight_repo = repo.SflightRepository(session)
        sflight_list = gens.generate_sflight(spfli_list, sflight_n)
        sflight_repo.create_sflight_list(sflight_list)
        await session.flush()

        #Генерация бронирований и добавление в БД
        sbook_repo = repo.SbookRepository(session)
        sbook_list = gens.generate_sbook(sflight_list, scustom_list, sbook_n)
        sbook_repo.create_sbook_list(sbook_list)
        await session.flush()
        
        #Кэширование свободных мест
        for item in sflight_list:
            cache.cache_set(f'{item.carrid}:{item.connid}:{item.fldate}', item.seatsmax - item.seatsocc, 60 * 60 * 24)

        #Коммит таблиц в БД
        await session.commit()

if __name__ == '__main__':
    asyncio.run(generate_all(4, 5, 5, 25, 75, 20))