"""Класс Festival и функции для планирования фестивалей."""
from datetime import date
from typing import List, Optional

from .base import Entity
from .organizers import Organizer
from .venues import Venue


class Festival(Entity):
    """Фестиваль, закреплённый за площадкой на определённую дату."""

    def __init__(
        self,
        festival_id: int,
        title: str,
        venue: Venue,
        festival_date: date,
        organizer: Organizer,
        expected_visitors: int,
        is_cancelled: bool = False,
    ) -> None:
        """Создать фестиваль."""
        super().__init__(festival_id)
        self.title = title
        self.venue = venue
        self.festival_date = festival_date
        self.organizer = organizer
        self.expected_visitors = expected_visitors
        self.is_cancelled = is_cancelled

    def cancel(self) -> None:
        """Отменить фестиваль: площадка на эту дату освобождается."""
        self.is_cancelled = True

    def blocks(self, venue: Venue, festival_date: date) -> bool:
        """Проверить, занимает ли фестиваль площадку на указанную дату."""
        return (
            not self.is_cancelled
            and self.venue.id == venue.id
            and self.festival_date == festival_date
        )

    def days_until(self, today: date) -> int:
        """Количество дней до начала фестиваля (функция из ПР1)."""
        return (self.festival_date - today).days

    def to_data(self) -> dict:
        """Преобразовать фестиваль в словарь для JSON (ссылки → id)."""
        return {
            "id": self.id,
            "title": self.title,
            "venue_id": self.venue.id,
            "festival_date": self.festival_date.isoformat(),
            "organizer_id": self.organizer.id,
            "expected_visitors": self.expected_visitors,
            "is_cancelled": self.is_cancelled,
        }

    def __str__(self) -> str:
        """Строковое представление фестиваля с учётом его состояния."""
        status = "отменён" if self.is_cancelled else "запланирован"
        return (
            f"«{self.title}» – {self.venue.name}, "
            f"{self.festival_date:%d.%m.%Y}, "
            f"{self.expected_visitors} чел., {status}"
        )


def is_venue_available(
    festivals: List[Festival],
    venue: Venue,
    festival_date: date,
) -> bool:
    """Проверить, свободна ли площадка на дату (с учётом отмен)."""
    return not any(f.blocks(venue, festival_date) for f in festivals)


def create_festival(
    festivals: List[Festival],
    title: str,
    venue: Venue,
    festival_date: date,
    organizer: Organizer,
    expected_visitors: int,
) -> Optional[Festival]:
    """Запланировать фестиваль.

    Возвращает объект Festival или None, если площадка занята
    или не вмещает ожидаемое число посетителей.
    """
    if not venue.is_suitable_for(expected_visitors):
        return None
    if not is_venue_available(festivals, venue, festival_date):
        return None
    festival_id = max((f.id for f in festivals), default=0) + 1
    festival = Festival(
        festival_id, title, venue, festival_date, organizer, expected_visitors
    )
    festivals.append(festival)
    return festival


def find_festival_by_id(
    festivals: List[Festival],
    festival_id: int,
) -> Optional[Festival]:
    """Найти фестиваль по идентификатору."""
    for festival in festivals:
        if festival.id == festival_id:
            return festival
    return None


def cancel_festival(festivals: List[Festival], festival_id: int) -> bool:
    """Найти фестиваль и отменить его. Объект остаётся в коллекции."""
    festival = find_festival_by_id(festivals, festival_id)
    if festival is None or festival.is_cancelled:
        return False
    festival.cancel()
    return True


def get_venue_status(is_free: bool, fits: bool = True) -> str:
    """Вернуть текстовый статус площадки (функция из ПР1)."""
    if is_free and fits:
        return "Площадка доступна для проведения фестиваля"
    elif not fits:
        return "Площадка слишком мала для ожидаемого числа посетителей"
    return "Площадка уже занята на эту дату"


def festivals_statistics(festivals: List[Festival]) -> dict[str, int]:
    """Статистика по активным (не отменённым) фестивалям."""
    active = [f for f in festivals if not f.is_cancelled]
    return {
        "festivals": len(active),
        "visitors": sum(f.expected_visitors for f in active),
        "venues_used": len({f.venue.id for f in active}),
    }


def show_festivals(festivals: List[Festival]) -> None:
    """Вывести фестивали в консоль в порядке дат."""
    if not festivals:
        print("Фестивалей нет.")
        return
    for festival in sorted(festivals, key=lambda f: f.festival_date):
        print(f"#{festival.id} {festival} (орг. {festival.organizer.name})")
