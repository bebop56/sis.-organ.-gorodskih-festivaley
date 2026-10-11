import pytest

from models import Venue
from models.venues import (
    add_venue,
    check_venue_capacity,
    filter_venues_by_capacity,
    find_venue,
    find_venue_by_id,
    sort_venues,
)


def test_venue_attributes_and_str():
    venue = Venue(1, "Парк Горького", "Крымский Вал, 9", 5000)
    assert venue.name == "Парк Горького"
    assert venue.capacity == 5000
    assert "Парк Горького" in str(venue)


def test_is_suitable_for():
    venue = Venue(1, "Парк", "адрес", 100)
    assert venue.is_suitable_for(100)
    assert not venue.is_suitable_for(101)


def test_capacity_is_validated():
    assert not Venue.validate_capacity(0)
    with pytest.raises(ValueError):
        Venue(1, "Парк", "адрес", -5)


def test_add_venue(venues):
    venue = add_venue(venues, "Зарядье", "Варварка, 6", 1600)
    assert venue.id == 3
    assert find_venue_by_id(venues, 3) is venue


def test_find_venue_ignores_case(venues):
    assert find_venue(venues, "парк")[0].id == 1


def test_check_venue_capacity(venues):
    assert check_venue_capacity(venues, 1, 4000)
    assert not check_venue_capacity(venues, 2, 4000)
    with pytest.raises(KeyError):
        check_venue_capacity(venues, 99, 10)


def test_filter_and_sort(venues):
    assert [v.id for v in filter_venues_by_capacity(venues, 2000)] == [1]
    assert [v.id for v in sort_venues(venues)] == [2, 1]
