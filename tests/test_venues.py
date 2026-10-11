from venues import (
    add_venue,
    check_venue_capacity,
    filter_venues_by_capacity,
    find_venue,
    sort_venues,
)


def make_venues() -> dict[int, dict]:
    venues: dict[int, dict] = {}
    add_venue(venues, "Парк Горького", "Крымский Вал, 9", 5000)
    add_venue(venues, "Площадь Революции", "пл. Революции, 1", 1500)
    return venues


def test_add_venue():
    venues = make_venues()
    assert len(venues) == 2
    assert venues[2]["name"] == "Площадь Революции"


def test_find_venue_ignores_case():
    assert find_venue(make_venues(), "парк")[0]["id"] == 1


def test_check_venue_capacity():
    venues = make_venues()
    assert check_venue_capacity(venues, 1, 4000)
    assert not check_venue_capacity(venues, 2, 4000)


def test_filter_and_sort():
    venues = make_venues()
    assert [v["id"] for v in filter_venues_by_capacity(venues, 2000)] == [1]
    assert [v["id"] for v in sort_venues(venues)] == [2, 1]
