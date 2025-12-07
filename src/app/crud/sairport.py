"""SQL запросы для таблицы SCUSTOM."""

from sqlalchemy import select

from app.db import session
from app.db.models import Sairport


def get_uniq_city_list():
    """Выбор всех городов."""
    stmt = select(Sairport.city).distinct()
    result = session.execute(stmt)

    return result.scalars().all()

def get_airps_by_city(city:str):
    """Выбор всех аэропортов по городу."""
    stmt = select(Sairport).where(Sairport.city == city)
    result = session.execute(stmt)

    return result.scalars().all()