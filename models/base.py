"""Базовый класс сущностей предметной области."""


class Entity:
    """Сущность с целочисленным идентификатором.

    Общий предок Venue, Organizer и Festival: хранит идентификатор
    и задаёт единый интерфейс to_data() для сохранения в JSON.
    Каждый наследник переопределяет to_data() и __str__() по-своему
    (полиморфизм), а storage.py работает с ними одинаково.
    """

    def __init__(self, entity_id: int) -> None:
        """Сохранить идентификатор сущности."""
        if entity_id <= 0:
            raise ValueError("Идентификатор должен быть положительным")
        self._id = entity_id

    @property
    def id(self) -> int:
        """Идентификатор сущности (только для чтения)."""
        return self._id

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для записи в JSON."""
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        """Сущности равны, если совпадают тип и идентификатор."""
        return type(self) is type(other) and self.id == other.id

    def __hash__(self) -> int:
        """Хэш по типу и идентификатору."""
        return hash((type(self).__name__, self.id))
