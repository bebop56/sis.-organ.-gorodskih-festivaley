"""Вспомогательные функции безопасного ввода."""
from datetime import date, datetime


def input_int(prompt: str, min_value: int = 0) -> int:
    """Запросить целое число; при некорректном вводе повторить запрос."""
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")
            continue
        if value < min_value:
            print(f"Ошибка: число должно быть не меньше {min_value}.")
            continue
        return value


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ; при ошибке повторить запрос."""
    while True:
        raw = input(prompt)
        try:
            return datetime.strptime(raw.strip(), "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ.")
