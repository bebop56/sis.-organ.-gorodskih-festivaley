from datetime import date

from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.festivals import is_venue_available
from models.venues import find_venue_by_id, sort_venues
from storage import load_all


def venues(request):
    """Список площадок, отсортированный по вместимости."""
    venues_list, _, _ = load_all(settings.DATA_DIR)
    items = ""
    for venue in sort_venues(venues_list, reverse=True):
        items += f"""
        <a href="/venues/{venue.id}/"
           class="list-group-item list-group-item-action
                  d-flex justify-content-between align-items-center">
            <span>
                <strong>{escape(venue.name)}</strong><br>
                <small class="text-muted">{escape(venue.address)}</small>
            </span>
            <span class="badge bg-primary rounded-pill">
                до {venue.capacity} чел.
            </span>
        </a>"""
    content = f"""
    <h1 class="mb-3">Площадки</h1>
    <div class="list-group shadow-sm">{items}</div>
    """
    return HttpResponse(page("FestCity – площадки", content))


def venue_detail(request, venue_id):
    """Карточка площадки, её доступность сегодня и фестивали на ней."""
    venues_list, _, festivals_list = load_all(settings.DATA_DIR)
    venue = find_venue_by_id(venues_list, venue_id)
    if venue is None:
        content = """
        <h1 class="text-danger">Площадка не найдена</h1>
        <a href="/venues/" class="btn btn-outline-secondary">
            ← к списку площадок
        </a>
        """
        return HttpResponse(
            page("Площадка не найдена", content),
            status=404,
        )
    available = is_venue_available(festivals_list, venue, date.today())
    status = "свободна" if available else "занята"
    badge = "bg-success" if available else "bg-danger"
    events = ""
    for festival in festivals_list:
        if festival.venue.id != venue.id:
            continue
        crossed = " text-decoration-line-through" if (
            festival.is_cancelled
        ) else ""
        events += f"""
        <li class="list-group-item{crossed}">
            <a href="/festivals/{festival.id}/">
                {escape(festival.title)}
            </a> – {festival.festival_date:%d.%m.%Y}
        </li>"""
    if not events:
        events = '<li class="list-group-item">Фестивалей пока нет</li>'
    content = f"""
    <div class="card shadow-sm mb-4">
        <div class="card-body">
            <h1 class="card-title h3">{escape(venue.name)}</h1>
            <p class="card-text"><strong>ID:</strong> {venue.id}</p>
            <p class="card-text">
                <strong>Адрес:</strong> {escape(venue.address)}
            </p>
            <p class="card-text">
                <strong>Вместимость:</strong> {venue.capacity} чел.
            </p>
            <p class="card-text">
                Доступность на текущую дату:
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/venues/" class="btn btn-outline-secondary">
                ← к списку площадок
            </a>
        </div>
    </div>
    <h2 class="h5">Фестивали на площадке</h2>
    <ul class="list-group">{events}</ul>
    """
    return HttpResponse(page(escape(venue.name), content))
