"""FestCity – консольное приложение для организации городских фестивалей."""
from typing import List

from models import Festival, Organizer, Venue
from models.festivals import (
    cancel_festival,
    create_festival,
    festivals_statistics,
    get_venue_status,
    is_venue_available,
    show_festivals,
)
from models.organizers import (
    add_organizer,
    find_organizer,
    find_organizer_by_id,
    show_organizers,
)
from models.venues import (
    add_venue,
    filter_venues_by_capacity,
    find_venue,
    find_venue_by_id,
    show_venues,
    sort_venues,
)
from storage import (
    load_festivals,
    load_organizers,
    load_venues,
    save_festivals,
    save_organizers,
    save_venues,
)
from utils import input_date, input_int

VENUES_FILE = "data/venues.json"
ORGANIZERS_FILE = "data/organizers.json"
FESTIVALS_FILE = "data/festivals.json"

MENU = """
=== FestCity: организация городских фестивалей ===
1. Показать площадки
2. Найти площадку по названию
3. Подобрать площадки по вместимости
4. Проверить доступность площадки на дату
5. Запланировать фестиваль
6. Отменить фестиваль
7. Показать фестивали
8. Добавить площадку
9. Показать организаторов
10. Найти организатора
11. Добавить организатора
12. Статистика
0. Выход
"""


def check_availability(
    festivals: List[Festival],
    venues: List[Venue],
) -> None:
    """Сценарий проверки доступности площадки на дату."""
    venue = find_venue_by_id(venues, input_int("ID площадки: ", 1))
    if venue is None:
        print("Площадка не найдена.")
        return
    day = input_date("Дата (ДД.ММ.ГГГГ): ")
    print(get_venue_status(is_venue_available(festivals, venue, day)))


def create_new_festival(
    festivals: List[Festival],
    venues: List[Venue],
    organizers: List[Organizer],
) -> None:
    """Сценарий планирования фестиваля."""
    title = input("Название фестиваля: ").strip()
    if not title:
        print("Название не может быть пустым.")
        return
    venue = find_venue_by_id(venues, input_int("ID площадки: ", 1))
    if venue is None:
        print("Площадка не найдена.")
        return
    organizer = find_organizer_by_id(
        organizers, input_int("ID организатора: ", 1)
    )
    if organizer is None:
        print("Организатор не найден.")
        return
    visitors = input_int("Ожидаемое число посетителей: ", 1)
    if not venue.is_suitable_for(visitors):
        print(get_venue_status(True, fits=False))
        return
    day = input_date("Дата (ДД.ММ.ГГГГ): ")
    festival = create_festival(
        festivals, title, venue, day, organizer, visitors
    )
    if festival is None:
        print(get_venue_status(False))
    else:
        print(f"Фестиваль запланирован, номер #{festival.id}.")


def add_new_venue(venues: List[Venue]) -> None:
    """Сценарий добавления площадки."""
    name = input("Название площадки: ").strip()
    address = input("Адрес: ").strip()
    capacity = input_int("Вместимость: ", 1)
    venue = add_venue(venues, name, address, capacity)
    print(f"Площадка добавлена: [{venue.id}] {venue}")


def add_new_organizer(organizers: List[Organizer]) -> None:
    """Сценарий добавления организатора."""
    name = input("Имя: ").strip()
    email = input("E-mail: ").strip()
    try:
        organizer = add_organizer(organizers, name, email)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return
    print(f"Организатор добавлен: [{organizer.id}] {organizer}")


def show_statistics(festivals: List[Festival]) -> None:
    """Вывести статистику по активным фестивалям."""
    stats = festivals_statistics(festivals)
    print(
        f"Фестивалей: {stats['festivals']}, "
        f"ожидается посетителей: {stats['visitors']}, "
        f"задействовано площадок: {stats['venues_used']}"
    )


def save_all(
    venues: List[Venue],
    organizers: List[Organizer],
    festivals: List[Festival],
) -> None:
    """Сохранить все коллекции в JSON-файлы."""
    save_venues(VENUES_FILE, venues)
    save_organizers(ORGANIZERS_FILE, organizers)
    save_festivals(FESTIVALS_FILE, festivals)


def main() -> None:
    """Точка запуска: загрузка данных, цикл меню, сохранение."""
    venues = load_venues(VENUES_FILE)
    organizers = load_organizers(ORGANIZERS_FILE)
    festivals = load_festivals(FESTIVALS_FILE, venues, organizers)

    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            show_venues(sort_venues(venues))
        elif choice == "2":
            show_venues(find_venue(venues, input("Название: ")))
        elif choice == "3":
            visitors = input_int("Число посетителей: ", 1)
            show_venues(list(filter_venues_by_capacity(venues, visitors)))
        elif choice == "4":
            check_availability(festivals, venues)
        elif choice == "5":
            create_new_festival(festivals, venues, organizers)
        elif choice == "6":
            if cancel_festival(festivals, input_int("Номер фестиваля: ", 1)):
                print("Фестиваль отменён.")
            else:
                print("Фестиваль не найден или уже отменён.")
        elif choice == "7":
            show_festivals(festivals)
        elif choice == "8":
            add_new_venue(venues)
        elif choice == "9":
            show_organizers(organizers)
        elif choice == "10":
            show_organizers(find_organizer(organizers, input("Запрос: ")))
        elif choice == "11":
            add_new_organizer(organizers)
        elif choice == "12":
            show_statistics(festivals)
        elif choice == "0":
            save_all(venues, organizers, festivals)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неизвестная команда.")
            continue
        if choice in {"5", "6", "8", "11"}:
            save_all(venues, organizers, festivals)


if __name__ == "__main__":
    main()
