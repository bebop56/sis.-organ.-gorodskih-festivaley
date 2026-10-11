"""Сохранение и загрузка данных проекта в JSON-файлах."""
import json
import os


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


def _save_list(filename: str, items: list[dict]) -> None:
    """Записать список словарей в JSON-файл."""
    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=4)


def load_venues(filename: str) -> dict[int, dict]:
    """Загрузить площадки и вернуть словарь {id: площадка}."""
    return {venue["id"]: venue for venue in _load_list(filename)}


def save_venues(filename: str, venues: dict[int, dict]) -> None:
    """Сохранить площадки в JSON-файл."""
    _save_list(filename, list(venues.values()))


def load_festivals(filename: str) -> list[dict]:
    """Загрузить список фестивалей."""
    return _load_list(filename)


def save_festivals(filename: str, festivals: list[dict]) -> None:
    """Сохранить список фестивалей в JSON-файл."""
    _save_list(filename, festivals)
