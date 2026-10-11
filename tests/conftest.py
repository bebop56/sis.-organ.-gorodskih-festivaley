from datetime import date

import pytest

from models import Organizer, Venue

DAY = date(2026, 9, 19)


@pytest.fixture
def venues() -> list[Venue]:
    return [
        Venue(1, "Парк Горького", "Крымский Вал, 9", 5000),
        Venue(2, "Площадь Революции", "пл. Революции, 1", 1500),
    ]


@pytest.fixture
def organizers() -> list[Organizer]:
    return [
        Organizer(1, "Анна Смирнова", "anna@festcity.ru"),
        Organizer(2, "Игорь Волков", "volkov@jazzfest.ru"),
    ]
