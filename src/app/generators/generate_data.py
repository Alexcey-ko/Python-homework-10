"""Модуль, содержащий инструменты для генерации случайных данных в БД."""

from sqlalchemy.orm import Session

from app.db import cache, engine
from app.generators.sairport import generate_sairport
from app.generators.sbook import generate_sbook
from app.generators.scarr import generate_scarr
from app.generators.scustom import generate_scustom
from app.generators.sflight import generate_sflight
from app.generators.spfli import generate_spfli


def generate_all(airp_n: int = 5, carr_n: int = 5, cust_n: int = 5, spfli_n: int = 5, sflight_n: int = 5, sbook_n: int = 5):
    """Генерация данных для всех таблиц и коммит в БД."""
    with Session(engine) as session:
        sairport = generate_sairport(airp_n)
        scarr = generate_scarr(carr_n)
        scustom = generate_scustom(cust_n)

        #Генерируем независимые данные
        session.add_all(sairport)
        session.add_all(scarr)
        session.add_all(scustom)
        #Вызываем FLUSH чтобы сгенерировались автоинкременты
        session.flush()

        #Генерируем зависимые данные
        spfli = generate_spfli(scarr, sairport, spfli_n)
        session.add_all(spfli)
        session.flush()

        sflight = generate_sflight(spfli, sflight_n)
        session.add_all(sflight)
        session.flush()

        sbook = generate_sbook(sflight, scustom, sbook_n)
        session.add_all(sbook)
        session.flush()

        #Кэширование свободных мест
        for item in sflight:
            cache.cache_set(f'{item.carrid}:{item.connid}:{item.fldate}', item.seatsmax - item.seatsocc, 60 * 60 * 24)

        #Коммитим таблиц в БД
        session.commit()

if __name__ == '__main__':
    generate_all(10, 10, 10, 30, 100, 20)