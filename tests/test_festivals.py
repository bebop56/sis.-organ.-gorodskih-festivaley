from datetime import date

import pytest

from festivals import (
    cancel_festival,
    create_festival,
    festivals_statistics,
    is_venue_available,
)
from storage import load_festivals, save_festivals

DAY = date(2026, 9, 19)


def test_venue_available_when_empty():
    assert is_venue_available([], 1, DAY)


def test_duplicate_festival_forbidden():
    festivals: list[dict] = []
    assert create_festival(festivals, "Еда", 1, DAY, 100) is not None
    assert create_festival(festivals, "Джаз", 1, DAY, 100) is None
    assert not is_venue_available(festivals, 1, DAY)


def test_cancel_frees_venue():
    festivals: list[dict] = []
    festival = create_festival(festivals, "Еда", 1, DAY, 100)
    assert cancel_festival(festivals, festival["id"])
    assert is_venue_available(festivals, 1, DAY)


def test_statistics():
    festivals: list[dict] = []
    create_festival(festivals, "A", 1, DAY, 100)
    create_festival(festivals, "B", 1, date(2026, 9, 20), 50)
    assert festivals_statistics(festivals) == {
        "festivals": 2, "visitors": 150, "venues_used": 1,
    }


@pytest.mark.parametrize("content", [None, "{broken json"])
def test_load_handles_bad_files(tmp_path, content):
    path = tmp_path / "festivals.json"
    if content is not None:
        path.write_text(content, encoding="utf-8")
    assert load_festivals(str(path)) == []


def test_save_and_load(tmp_path):
    path = str(tmp_path / "f.json")
    festivals: list[dict] = []
    create_festival(festivals, "Еда", 1, DAY, 100)
    save_festivals(path, festivals)
    assert load_festivals(path) == festivals
