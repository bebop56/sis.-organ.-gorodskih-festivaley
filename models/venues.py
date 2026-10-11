"""Класс Venue и функции для работы с коллекцией площадок."""
from typing import Iterator, List, Optional

from .base import Entity


class Venue(Entity):
    """Городская площадка для проведения фестивалей."""

    def __init__(
        self,
        venue_id: int,
        name: str,
        address: str,
        capacity: int,
    ) -> None:
        """Создать площадку."""
        super().__init__(venue_id)
        self.name = name
        self.address = address
        self.capacity = capacity

    @property
    def capacity(self) -> int:
        """Вместимость площадки, человек."""
        return self._capacity

    @capacity.setter
    def capacity(self, value: int) -> None:
        """Изменить вместимость с проверкой корректности."""
        if not Venue.validate_capacity(value):
            raise ValueError("Вместимость площадки должна быть положительной")
        self._capacity = value

    @staticmethod
    def validate_capacity(capacity: int) -> bool:
        """Проверить корректность значения вместимости."""
        return isinstance(capacity, int) and capacity > 0

    def is_suitable_for(self, visitors: int) -> bool:
        """Проверить, вмещает ли площадка заданное число посетителей."""
        return self.capacity >= visitors

    @classmethod
    def from_data(cls, data: dict) -> "Venue":
        """Создать площадку из словаря, прочитанного из JSON."""
        return cls(data["id"], data["name"], data["address"], data["capacity"])

    def to_data(self) -> dict:
        """Преобразовать площадку в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "capacity": self.capacity,
        }

    def __str__(self) -> str:
        """Строковое представление площадки."""
        return f"{self.name} ({self.address}), до {self.capacity} чел."


def add_venue(
    venues: List[Venue],
    name: str,
    address: str,
    capacity: int,
) -> Venue:
    """Создать площадку, добавить её в коллекцию и вернуть."""
    venue_id = max((venue.id for venue in venues), default=0) + 1
    venue = Venue(venue_id, name, address, capacity)
    venues.append(venue)
    return venue


def find_venue_by_id(venues: List[Venue], venue_id: int) -> Optional[Venue]:
    """Найти площадку по идентификатору."""
    for venue in venues:
        if venue.id == venue_id:
            return venue
    return None


def find_venue(venues: List[Venue], query: str) -> List[Venue]:
    """Найти площадки по подстроке названия (без учёта регистра)."""
    query = query.lower().strip()
    return [venue for venue in venues if query in venue.name.lower()]


def check_venue_capacity(
    venues: List[Venue],
    venue_id: int,
    visitors: int,
) -> bool:
    """Найти площадку и проверить её вместимость."""
    venue = find_venue_by_id(venues, venue_id)
    if venue is None:
        raise KeyError(f"Площадка с id={venue_id} не найдена")
    return venue.is_suitable_for(visitors)


def filter_venues_by_capacity(
    venues: List[Venue],
    visitors: int,
) -> Iterator[Venue]:
    """Отобрать площадки, подходящие для visitors посетителей."""
    return (venue for venue in venues if venue.is_suitable_for(visitors))


def sort_venues(venues: List[Venue], reverse: bool = False) -> List[Venue]:
    """Отсортировать площадки по вместимости."""
    return sorted(venues, key=lambda venue: venue.capacity, reverse=reverse)


def show_venues(venues: List[Venue]) -> None:
    """Вывести список площадок в консоль."""
    if not venues:
        print("Площадок нет.")
        return
    for venue in venues:
        print(f"[{venue.id}] {venue}")
