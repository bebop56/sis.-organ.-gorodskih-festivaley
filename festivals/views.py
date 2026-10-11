from datetime import date

from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.festivals import find_festival_by_id
from storage import load_all


def status_badge(festival):
    """Вернуть текст статуса и CSS-класс бейджа фестиваля."""
    if festival.is_cancelled:
        return "отменён", "bg-secondary"
    return "запланирован", "bg-success"


def festivals(request):
    """Список фестивалей в порядке дат проведения."""
    _, _, festivals_list = load_all(settings.DATA_DIR)
    items = ""
    for festival in sorted(festivals_list, key=lambda f: f.festival_date):
        status, badge = status_badge(festival)
        items += f"""
        <li class="list-group-item d-flex justify-content-between
                   align-items-center">
            <span>
                <a href="/festivals/{festival.id}/">
                    {escape(festival.title)}
                </a><br>
                <small class="text-muted">
                    {escape(festival.venue.name)},
                    {festival.festival_date:%d.%m.%Y}
                </small>
            </span>
            <span class="badge {badge}">{status}</span>
        </li>"""
    content = f"""
    <h1 class="mb-3">Фестивали</h1>
    <ul class="list-group shadow-sm">{items}</ul>
    """
    return HttpResponse(page("FestCity – фестивали", content))


def festival_detail(request, festival_id):
    """Карточка фестиваля со связанными площадкой и организатором."""
    _, _, festivals_list = load_all(settings.DATA_DIR)
    festival = find_festival_by_id(festivals_list, festival_id)
    if festival is None:
        content = """
        <h1 class="text-danger">Фестиваль не найден</h1>
        <a href="/festivals/" class="btn btn-outline-secondary">
            ← к списку фестивалей
        </a>
        """
        return HttpResponse(
            page("Фестиваль не найден", content),
            status=404,
        )
    status, badge = status_badge(festival)
    days = festival.days_until(date.today())
    when = f"через {days} дн." if days >= 0 else "уже прошёл"
    load = round(festival.expected_visitors / festival.venue.capacity * 100)
    content = f"""
    <div class="card shadow-sm">
        <div class="card-body">
            <h1 class="card-title h3">{escape(festival.title)}</h1>
            <p class="card-text">
                <strong>Площадка:</strong>
                <a href="/venues/{festival.venue.id}/">
                    {escape(festival.venue.name)}
                </a>
            </p>
            <p class="card-text">
                <strong>Дата:</strong>
                {festival.festival_date:%d.%m.%Y} ({when})
            </p>
            <p class="card-text">
                <strong>Организатор:</strong>
                {escape(str(festival.organizer))}
            </p>
            <p class="card-text">
                <strong>Ожидается посетителей:</strong>
                {festival.expected_visitors}
                (заполненность площадки {load}%)
            </p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
            <a href="/festivals/" class="btn btn-outline-secondary">
                ← к списку фестивалей
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(escape(festival.title), content))
