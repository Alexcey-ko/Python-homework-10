"""Модуль для работы с БД."""

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, declarative_base

from app.core.config import settings


def get_db_url()->URL:
    """Формирование URL для подключения к БД."""
    # Диалект
    dialect  = 'postgresql'
    driver   = 'psycopg2'
    
    return URL.create(
        f'{dialect}+{driver}',
        username = settings.POSTGRES_USER,
        password = settings.POSTGRES_PASSWORD,
        host = settings.POSTGRES_HOST,
        port = settings.POSTGRES_PORT,
        database = settings.POSTGRES_DB )

def get_engine():
    """Создание движка для работы с POSTGRESS."""
    return create_engine(get_db_url(), echo=False)

#Базовый класс для создания таблиц БД
Base:DeclarativeBase = declarative_base()

#Движок для работы с БД
engine = get_engine()

#Сессия
session = Session(engine)