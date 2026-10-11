"""FestCity – консольное приложение для организации городских фестивалей."""
from datetime import date

from festivals import (
    cancel_festival,
    create_festival,
    festivals_statistics,
    get_venue_status,
    is_venue_available,
)
from storage import load_festivals, load_venues, save_festivals, save_venues
from utils import input_date, input_int
from venues import (
    add_venue,
    check_venue_capacity,
    filter_venues_by_capacity,
    find_venue,
    sort_venues,
)

VENUES_FILE = "data/venues.json"
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
9. Статистика
0. Выход
"""


def show_venues(venues: list[dict]) -> None:
    """Вывести список площадок в виде таблицы."""
    if not venues:
        print("Площадок нет.")
        return
    print(f"{'ID':<4}{'Название':<28}{'Вместимость':>12}  Адрес")
    for venue in venues:
        print(
            f"{venue['id']:<4}{venue['name']:<28}"
            f"{venue['capacity']:>12}  {venue['address']}"
        )


def show_festivals(festivals: list[dict], venues: dict[int, dict]) -> None:
    """Вывести список фестивалей с названием площадки и датой."""
    if not festivals:
        print("Фестивалей нет.")
        return
    for festival in sorted(festivals, key=lambda f: f["festival_date"]):
        venue = venues.get(festival["venue_id"], {"name": "—"})
        day = date.fromisoformat(festival["festival_date"])
        print(
            f"#{festival['id']} {festival['title']} – {venue['name']}, "
            f"{day:%d.%m.%Y}, {festival['expected_visitors']} чел."
        )


def plan_festival(festivals: list[dict], venues: dict[int, dict]) -> None:
    """Сценарий планирования фестиваля."""
    title = input("Название фестиваля: ").strip()
    if not title:
        print("Название не может быть пустым.")
        return
    venue_id = input_int("ID площадки: ", min_value=1)
    if venue_id not in venues:
        print("Площадка не найдена.")
        return
    visitors = input_int("Ожидаемое число посетителей: ", min_value=1)
    if not check_venue_capacity(venues, venue_id, visitors):
        print(get_venue_status(True, fits=False))
        return
    festival_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    festival = create_festival(
        festivals, title, venue_id, festival_date, visitors
    )
    if festival is None:
        print(get_venue_status(False))
    else:
        print(f"Фестиваль запланирован, номер #{festival['id']}.")


def main() -> None:
    """Точка запуска: цикл меню и вызов функций проекта."""
    venues = load_venues(VENUES_FILE)
    festivals = load_festivals(FESTIVALS_FILE)

    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            show_venues(sort_venues(venues))
        elif choice == "2":
            show_venues(find_venue(venues, input("Название: ")))
        elif choice == "3":
            visitors = input_int("Число посетителей: ", min_value=1)
            show_venues(list(filter_venues_by_capacity(venues, visitors)))
        elif choice == "4":
            venue_id = input_int("ID площадки: ", min_value=1)
            if venue_id not in venues:
                print("Площадка не найдена.")
                continue
            day = input_date("Дата (ДД.ММ.ГГГГ): ")
            print(get_venue_status(
                is_venue_available(festivals, venue_id, day)
            ))
        elif choice == "5":
            plan_festival(festivals, venues)
            save_festivals(FESTIVALS_FILE, festivals)
        elif choice == "6":
            festival_id = input_int("Номер фестиваля: ", min_value=1)
            if cancel_festival(festivals, festival_id):
                save_festivals(FESTIVALS_FILE, festivals)
                print("Фестиваль отменён.")
            else:
                print("Фестиваль не найден.")
        elif choice == "7":
            show_festivals(festivals, venues)
        elif choice == "8":
            name = input("Название площадки: ").strip()
            address = input("Адрес: ").strip()
            capacity = input_int("Вместимость: ", min_value=1)
            venue_id = add_venue(venues, name, address, capacity)
            save_venues(VENUES_FILE, venues)
            print(f"Площадка добавлена, ID {venue_id}.")
        elif choice == "9":
            stats = festivals_statistics(festivals)
            print(
                f"Фестивалей: {stats['festivals']}, "
                f"ожидается посетителей: {stats['visitors']}, "
                f"задействовано площадок: {stats['venues_used']}"
            )
        elif choice == "0":
            save_venues(VENUES_FILE, venues)
            save_festivals(FESTIVALS_FILE, festivals)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
