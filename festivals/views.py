from datetime import date

from django.conf import settings
from django.shortcuts import render

from models.festivals import find_festival_by_id
from storage import load_all


def festivals(request):
    """Список фестивалей в порядке дат проведения."""
    _, _, festivals_list = load_all(settings.DATA_DIR)
    context = {
        "festivals": sorted(festivals_list, key=lambda f: f.festival_date),
    }
    return render(request, "festivals/festival_list.html", context)


def festival_detail(request, festival_id):
    """Карточка фестиваля со связанными площадкой и организатором."""
    _, _, festivals_list = load_all(settings.DATA_DIR)
    festival = find_festival_by_id(festivals_list, festival_id)
    context = {"festival": festival}
    if festival is not None:
        context["days_left"] = festival.days_until(date.today())
        context["load_percent"] = round(
            festival.expected_visitors / festival.venue.capacity * 100
        )
    return render(
        request,
        "festivals/festival_detail.html",
        context,
        status=404 if festival is None else 200,
    )
