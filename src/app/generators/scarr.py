"""Модуль, содержащий инструменты для генерации случайных данных для SCARR."""

from faker import Faker

from app.db.models import Scarr


def generate_scarr(n:int=5)->list[Scarr]:
    """Генерация списка SCARR для mandt из n позиций."""
    fake = Faker('ru_RU')
    scarr_list:list[Scarr] = []
    for _ in range(n):
        scarr_list.append(Scarr(
            carrname = fake.company(),
            carrcode = fake.ean(length=8),
            url = fake.url(),
        ))
    return scarr_list