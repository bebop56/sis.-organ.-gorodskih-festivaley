from datetime import date

from models.festivals import (
    cancel_festival,
    create_festival,
    festivals_statistics,
    is_venue_available,
)
from storage import load_festivals, save_festivals

DAY = date(2026, 9, 19)


def test_festival_links_objects(venues, organizers):
    festivals = []
    festival = create_festival(
        festivals, "Еда", venues[0], DAY, organizers[0], 3000
    )
    assert festival.venue.name == "Парк Горького"
    assert festival.organizer.email == "anna@festcity.ru"
    assert festival.days_until(date(2026, 9, 1)) == 18


def test_venue_available_when_empty(venues):
    assert is_venue_available([], venues[0], DAY)


def test_duplicate_festival_forbidden(venues, organizers):
    festivals = []
    create_festival(festivals, "Еда", venues[0], DAY, organizers[0], 100)
    second = create_festival(
        festivals, "Джаз", venues[0], DAY, organizers[1], 100
    )
    assert second is None
    assert not is_venue_available(festivals, venues[0], DAY)


def test_too_many_visitors_forbidden(venues, organizers):
    festivals = []
    result = create_festival(
        festivals, "Рок", venues[1], DAY, organizers[0], 2000
    )
    assert result is None
    assert festivals == []


def test_cancel_frees_venue_but_keeps_object(venues, organizers):
    festivals = []
    festival = create_festival(
        festivals, "Еда", venues[0], DAY, organizers[0], 100
    )
    assert cancel_festival(festivals, festival.id)
    assert festival.is_cancelled
    assert "отменён" in str(festival)
    assert len(festivals) == 1
    assert is_venue_available(festivals, venues[0], DAY)
    assert not cancel_festival(festivals, festival.id)


def test_statistics_ignores_cancelled(venues, organizers):
    festivals = []
    create_festival(festivals, "A", venues[0], DAY, organizers[0], 100)
    b = create_festival(festivals, "B", venues[1], DAY, organizers[0], 50)
    b.cancel()
    assert festivals_statistics(festivals) == {
        "festivals": 1, "visitors": 100, "venues_used": 1,
    }


def test_save_and_load_restores_links(tmp_path, venues, organizers):
    path = str(tmp_path / "festivals.json")
    festivals = []
    create_festival(festivals, "Еда", venues[0], DAY, organizers[1], 100)
    festivals[0].cancel()
    save_festivals(path, festivals)
    loaded = load_festivals(path, venues, organizers)
    assert loaded[0].venue is venues[0]
    assert loaded[0].organizer is organizers[1]
    assert loaded[0].festival_date == DAY
    assert loaded[0].is_cancelled


def test_load_handles_broken_file(tmp_path, venues, organizers):
    path = tmp_path / "festivals.json"
    path.write_text("{broken json", encoding="utf-8")
    assert load_festivals(str(path), venues, organizers) == []
