"""Приложение для бронирования авиабилетов."""

from app.client import login, select_flight
from app.crud.sairport import get_uniq_city_list
from app.crud.sbook import book_flight

#Авторизация пользователя
#Верхний тагил
#Железногорск
scustom = login()
#Выбор рейса
selected_flight, seats = select_flight(get_uniq_city_list())
#Бронирование рейса
if selected_flight and book_flight(selected_flight, scustom, seats):
    print('Рейс успешно забронирован.')