"""Функции для планирования и отмены фестивалей."""
from datetime import date
from typing import Optional


def is_venue_available(
    festivals: list[dict],
    venue_id: int,
    festival_date: date,
) -> bool:
    """Проверить, свободна ли площадка на указанную дату."""
    for festival in festivals:
        if (
            festival["venue_id"] == venue_id
            and festival["festival_date"] == festival_date.isoformat()
        ):
            return False
    return True


def create_festival(
    festivals: list[dict],
    title: str,
    venue_id: int,
    festival_date: date,
    expected_visitors: int,
) -> Optional[dict]:
    """Запланировать фестиваль, если площадка свободна на эту дату.

    Возвращает словарь созданного фестиваля или None, если площадка занята.
    """
    if not is_venue_available(festivals, venue_id, festival_date):
        return None
    festival_id = max((f["id"] for f in festivals), default=0) + 1
    festival = {
        "id": festival_id,
        "title": title,
        "venue_id": venue_id,
        "festival_date": festival_date.isoformat(),
        "expected_visitors": expected_visitors,
    }
    festivals.append(festival)
    return festival


def cancel_festival(festivals: list[dict], festival_id: int) -> bool:
    """Отменить фестиваль (удалить из списка). Вернуть True при успехе."""
    for index, festival in enumerate(festivals):
        if festival["id"] == festival_id:
            del festivals[index]
            return True
    return False


def get_venue_status(is_free: bool, fits: bool = True) -> str:
    """Вернуть текстовый статус площадки (функция из ПР1)."""
    if is_free and fits:
        return "Площадка доступна для проведения фестиваля"
    elif not fits:
        return "Площадка слишком мала для ожидаемого числа посетителей"
    return "Площадка уже занята на эту дату"


def festivals_statistics(festivals: list[dict]) -> dict[str, int]:
    """Посчитать количество фестивалей и суммарное число посетителей."""
    total_visitors = sum(f["expected_visitors"] for f in festivals)
    used_venues = {f["venue_id"] for f in festivals}
    return {
        "festivals": len(festivals),
        "visitors": total_visitors,
        "venues_used": len(used_venues),
    }
