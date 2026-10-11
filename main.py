"""FestCity – начальный сценарий (ПР1).

Проверка возможности провести фестиваль на выбранной площадке.
"""
from datetime import date

venue_name = "Парк Горького"
venue_capacity = 5000
festival_name = "Фестиваль уличной еды"
expected_visitors = int("3500")
festival_date = date(2026, 9, 19)
is_venue_free = True


def check_capacity(capacity: int, visitors: int) -> bool:
    """Проверить, вмещает ли площадка ожидаемое число посетителей."""
    return capacity >= visitors


def days_until(event_date: date, today: date) -> int:
    """Вернуть количество дней до начала фестиваля."""
    return (event_date - today).days


def get_venue_status(is_free: bool, fits: bool) -> str:
    """Вернуть текстовый статус возможности провести фестиваль."""
    if is_free and fits:
        return "Площадка доступна для проведения фестиваля"
    elif not fits:
        return "Площадка слишком мала для ожидаемого числа посетителей"
    return "Площадка уже занята на эту дату"


fits = check_capacity(venue_capacity, expected_visitors)
load_percent = round(expected_visitors / venue_capacity * 100, 1)

print(f"Фестиваль: {festival_name}")
print(f"Площадка: {venue_name} (вместимость {venue_capacity} чел.)")
print(f"Дата: {festival_date.strftime('%d.%m.%Y')}")
print(f"Ожидается посетителей: {expected_visitors} ({load_percent}%)")
print(f"Дней до начала: {days_until(festival_date, date(2026, 9, 1))}")
print(get_venue_status(is_venue_free, fits))
