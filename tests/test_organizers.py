import pytest

from models import Organizer
from models.organizers import add_organizer, find_organizer


def test_organizer_from_data_and_str():
    organizer = Organizer.from_data(
        {"id": 5, "name": "Анна", "email": "anna@festcity.ru"}
    )
    assert organizer.id == 5
    assert str(organizer) == "Анна <anna@festcity.ru>"


def test_invalid_email_rejected():
    with pytest.raises(ValueError):
        Organizer(1, "Анна", "без-почты")


def test_add_and_find_organizer(organizers):
    add_organizer(organizers, "Мария", "maria@bookfest.ru")
    assert len(organizers) == 3
    assert find_organizer(organizers, "JAZZ")[0].name == "Игорь Волков"
