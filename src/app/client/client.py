"""Инструменты авторизации пользователя."""
from prompt_toolkit.shortcuts.dialogs import radiolist_dialog

from app.crud.scustom import create_scustom, get_scustom_by_email
from app.crud.sflight import get_av_seats, get_sflight_by_cities
from app.db.models import Scustom


def login()->Scustom:
    """Авторизация или регистрация пользователя."""
    print('Авторизация:')
    email = input('Введите Email: ')

    scustom = get_scustom_by_email(email)
    if not scustom:
        print('Пользователя с таким Email ещё не существует. Зарегистрируйтесь.')
        phone_number = input('Номер телефона: ')
        name = input('ФИО: ')
        scustom = create_scustom(email, phone_number, name)
        print('Регистрация пройдена успешно.')
    else:
        phone_number = input('Введите номер телефона: ')
        if phone_number == scustom.phone_number:
            print('Авторизация пройдена успешно.')
        else:
            print('Неверный номер телефона.')

    return scustom

def select_flight(cities:list[str]):
    """Выбор рейса между городами."""
    result = radiolist_dialog(
        title='Выбор города',
        text='Выберите город отправления',
        values=list(enumerate(cities)),
    ).run()
    city_from = cities[result]
    result = radiolist_dialog(
        title='Выбор города',
        text='Выберите город назначения',
        values=list(enumerate(cities)),
    ).run()
    city_to = cities[result]
    #Выборка рейсов между городами
    sflight = get_sflight_by_cities(city_from, city_to)
    if sflight:
        print('Доступные рейсы:')
        for idx, item in enumerate(sflight):
            print(f'Рейс №{idx + 1} на дату {item.fldate} стоимость: {item.price} {item.currency}, количество свободных мест:{get_av_seats(item)}.')
        selected_flight = int(input('Введите номер выбранного рейса:'))
        seats = int(input('Введи количество мест для бронирования:'))

        return sflight[selected_flight - 1], seats