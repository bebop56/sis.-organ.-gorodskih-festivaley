"""Сохранение и загрузка данных проекта в JSON-файлах.

JSON используется для хранения, объекты – для работы приложения:
при загрузке словари превращаются в объекты, при сохранении – обратно.
"""
import json
import os
from datetime import date
from typing import List, Sequence, Tuple

from models import Festival, Organizer, Venue
from models.base import Entity
from models.organizers import find_organizer_by_id
from models.venues import find_venue_by_id


def _load_list(filename: str) -> list[dict]:
    """Прочитать список словарей из JSON-файла.

    При отсутствии файла или некорректном JSON возвращается пустой список.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные не загружены.")
        return []
    if not isinstance(data, list):
        return []
    return data


def save_entities(filename: str, entities: Sequence[Entity]) -> None:
    """Сохранить любые сущности в JSON-файл (полиморфный вызов to_data)."""
    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            [entity.to_data() for entity in entities],
            file,
            ensure_ascii=False,
            indent=4,
        )


def load_venues(filename: str) -> List[Venue]:
    """Загрузить площадки и вернуть список объектов Venue."""
    venues = []
    for item in _load_list(filename):
        try:
            venues.append(Venue.from_data(item))
        except (KeyError, ValueError) as error:
            print(f"Пропущена некорректная запись площадки: {error}")
    return venues


def load_organizers(filename: str) -> List[Organizer]:
    """Загрузить организаторов и вернуть список объектов Organizer."""
    organizers = []
    for item in _load_list(filename):
        try:
            organizers.append(Organizer.from_data(item))
        except (KeyError, ValueError) as error:
            print(f"Пропущена некорректная запись организатора: {error}")
    return organizers


def load_festivals(
    filename: str,
    venues: List[Venue],
    organizers: List[Organizer],
) -> List[Festival]:
    """Загрузить фестивали, восстановив ссылки на Venue и Organizer."""
    festivals = []
    for item in _load_list(filename):
        try:
            venue = find_venue_by_id(venues, item["venue_id"])
            organizer = find_organizer_by_id(organizers, item["organizer_id"])
            if venue is None or organizer is None:
                raise ValueError("нет связанной площадки или организатора")
            festivals.append(Festival(
                item["id"],
                item["title"],
                venue,
                date.fromisoformat(item["festival_date"]),
                organizer,
                item["expected_visitors"],
                item.get("is_cancelled", False),
            ))
        except (KeyError, ValueError) as error:
            print(f"Пропущена некорректная запись фестиваля: {error}")
    return festivals


def save_venues(filename: str, venues: List[Venue]) -> None:
    """Сохранить площадки в JSON-файл."""
    save_entities(filename, venues)


def save_organizers(filename: str, organizers: List[Organizer]) -> None:
    """Сохранить организаторов в JSON-файл."""
    save_entities(filename, organizers)


def save_festivals(filename: str, festivals: List[Festival]) -> None:
    """Сохранить фестивали в JSON-файл (объекты-ссылки → id)."""
    save_entities(filename, festivals)


def load_all(
    data_dir: str,
) -> Tuple[List[Venue], List[Organizer], List[Festival]]:
    """Загрузить все коллекции из каталога data_dir со связями."""
    venues = load_venues(os.path.join(data_dir, "venues.json"))
    organizers = load_organizers(os.path.join(data_dir, "organizers.json"))
    festivals = load_festivals(
        os.path.join(data_dir, "festivals.json"), venues, organizers
    )
    return venues, organizers, festivals
