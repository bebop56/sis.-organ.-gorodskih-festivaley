from datetime import date

from django.conf import settings
from django.shortcuts import render

from models.festivals import is_venue_available
from models.venues import find_venue_by_id, sort_venues
from storage import load_all


def venues(request):
    """Список площадок, отсортированный по вместимости."""
    venues_list, _, _ = load_all(settings.DATA_DIR)
    context = {
        "venues": sort_venues(venues_list, reverse=True),
    }
    return render(request, "venues/venue_list.html", context)


def venue_detail(request, venue_id):
    """Карточка площадки, её доступность сегодня и фестивали на ней."""
    venues_list, _, festivals_list = load_all(settings.DATA_DIR)
    venue = find_venue_by_id(venues_list, venue_id)
    context = {"venue": venue}
    if venue is not None:
        context["available"] = is_venue_available(
            festivals_list, venue, date.today()
        )
        context["festivals"] = sorted(
            (f for f in festivals_list if f.venue.id == venue.id),
            key=lambda f: f.festival_date,
        )
    return render(
        request,
        "venues/venue_detail.html",
        context,
        status=404 if venue is None else 200,
    )
