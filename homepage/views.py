from datetime import date

from django.shortcuts import render

from db.database import fetch_all, fetch_one


def index(request):
    """Главная страница: описание, сводка и ближайшие фестивали."""
    venues_info = fetch_one(
        """
        SELECT
            COUNT(*) AS venues_count,
            SUM(capacity) AS capacity_total
        FROM venues
        """
    )
    stats = fetch_one(
        """
        SELECT
            COUNT(*) AS festivals,
            COALESCE(SUM(expected_visitors), 0) AS visitors
        FROM festivals
        WHERE is_cancelled = 0
        """
    )
    upcoming = fetch_all(
        """
        SELECT id, title, festival_date
        FROM festivals
        WHERE is_cancelled = 0
          AND festival_date >= ?
        ORDER BY festival_date
        LIMIT ?
        """,
        [date.today().isoformat(), 3],
    )
    context = {
        "venues_count": venues_info["venues_count"],
        "capacity_total": venues_info["capacity_total"],
        "stats": stats,
        "upcoming": upcoming,
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request, exception):
    """Собственная страница ошибки 404."""
    return render(request, "homepage/404.html", status=404)
