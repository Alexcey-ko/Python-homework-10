"""Модуль, содержащий инструменты для генерации случайных данных для SAIRPORT."""

from faker import Faker

from app.db.models import Sairport


def generate_sairport(n:int=5)->list[Sairport]:
    """Генерация списка SAIRPORT для mandt из n позиций."""
    fake = Faker('ru_RU')
    sairport_list:list[Sairport] = []
    for _ in range(n):
        sairport_list.append(
            Sairport(
                name=f'Аэропорт {fake.company()}',
                timezone=fake.timezone(),
                country=fake.country(),
                city=fake.city_name()
            ))
    return sairport_list