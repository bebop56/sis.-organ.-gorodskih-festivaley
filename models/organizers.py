"""Класс Organizer и функции для работы с организаторами."""
from typing import List, Optional

from .base import Entity


class Organizer(Entity):
    """Организатор фестиваля – пользователь системы."""

    def __init__(self, organizer_id: int, name: str, email: str) -> None:
        """Создать организатора."""
        super().__init__(organizer_id)
        if "@" not in email:
            raise ValueError(f"Некорректный e-mail: {email}")
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "Organizer":
        """Создать организатора из словаря, прочитанного из JSON."""
        return cls(data["id"], data["name"], data["email"])

    def to_data(self) -> dict:
        """Преобразовать организатора в словарь для JSON."""
        return {"id": self.id, "name": self.name, "email": self.email}

    def __str__(self) -> str:
        """Строковое представление организатора."""
        return f"{self.name} <{self.email}>"


def add_organizer(
    organizers: List[Organizer],
    name: str,
    email: str,
) -> Organizer:
    """Создать организатора, добавить в коллекцию и вернуть."""
    organizer_id = max((o.id for o in organizers), default=0) + 1
    organizer = Organizer(organizer_id, name, email)
    organizers.append(organizer)
    return organizer


def find_organizer_by_id(
    organizers: List[Organizer],
    organizer_id: int,
) -> Optional[Organizer]:
    """Найти организатора по идентификатору."""
    for organizer in organizers:
        if organizer.id == organizer_id:
            return organizer
    return None


def find_organizer(organizers: List[Organizer], query: str) -> List[Organizer]:
    """Найти организаторов по подстроке имени или e-mail."""
    query = query.lower().strip()
    return [
        o for o in organizers
        if query in o.name.lower() or query in o.email.lower()
    ]


def show_organizers(organizers: List[Organizer]) -> None:
    """Вывести список организаторов в консоль."""
    if not organizers:
        print("Организаторов нет.")
        return
    for organizer in organizers:
        print(f"[{organizer.id}] {organizer}")
