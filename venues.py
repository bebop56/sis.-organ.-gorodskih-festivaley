"""Функции для работы с городскими площадками."""
from typing import Iterator


def add_venue(
    venues: dict[int, dict],
    name: str,
    address: str,
    capacity: int,
) -> int:
    """Добавить площадку в словарь venues и вернуть её идентификатор."""
    if capacity <= 0:
        raise ValueError("Вместимость площадки должна быть положительной")
    venue_id = max(venues, default=0) + 1
    venues[venue_id] = {
        "id": venue_id,
        "name": name,
        "address": address,
        "capacity": capacity,
    }
    return venue_id


def find_venue(venues: dict[int, dict], query: str) -> list[dict]:
    """Найти площадки по подстроке названия (без учёта регистра)."""
    query = query.lower().strip()
    return [
        venue for venue in venues.values()
        if query in venue["name"].lower()
    ]


def check_venue_capacity(
    venues: dict[int, dict],
    venue_id: int,
    visitors: int,
) -> bool:
    """Проверить, вмещает ли площадка заданное число посетителей."""
    venue = venues.get(venue_id)
    if venue is None:
        raise KeyError(f"Площадка с id={venue_id} не найдена")
    return venue["capacity"] >= visitors


def filter_venues_by_capacity(
    venues: dict[int, dict],
    min_capacity: int,
) -> Iterator[dict]:
    """Отобрать площадки вместимостью не меньше min_capacity (генератор)."""
    for venue in venues.values():
        if venue["capacity"] >= min_capacity:
            yield venue


def sort_venues(venues: dict[int, dict], reverse: bool = False) -> list[dict]:
    """Отсортировать площадки по вместимости."""
    return sorted(
        venues.values(),
        key=lambda venue: venue["capacity"],
        reverse=reverse,
    )
