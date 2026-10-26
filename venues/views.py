from datetime import date

from django.shortcuts import render

from db.database import fetch_all, fetch_one


def parse_positive_int(value):
    """Число из GET-параметра или None, если значение не задано/неверно."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number if number > 0 else None


def venues(request):
    """Список площадок; при ?min_capacity=N – только вмещающие N человек."""
    min_capacity = parse_positive_int(request.GET.get("min_capacity"))
    if min_capacity is None:
        venues_list = fetch_all(
            """
            SELECT id, name, address, capacity
            FROM venues
            ORDER BY capacity DESC
            """
        )
    else:
        venues_list = fetch_all(
            """
            SELECT id, name, address, capacity
            FROM venues
            WHERE capacity >= ?
            ORDER BY capacity DESC
            """,
            [min_capacity],
        )
    context = {
        "venues": venues_list,
        "min_capacity": min_capacity,
    }
    return render(request, "venues/venue_list.html", context)


def venue_detail(request, venue_id):
    """Карточка площадки, её доступность сегодня и фестивали на ней."""
    venue = fetch_one(
        """
        SELECT id, name, address, capacity
        FROM venues
        WHERE id = ?
        """,
        [venue_id],
    )
    context = {"venue": venue}
    if venue is not None:
        busy_today = fetch_one(
            """
            SELECT COUNT(*) AS festivals_count
            FROM festivals
            WHERE venue_id = ?
              AND festival_date = ?
              AND is_cancelled = 0
            """,
            [venue_id, date.today().isoformat()],
        )
        context["available"] = busy_today["festivals_count"] == 0
        context["festivals"] = fetch_all(
            """
            SELECT
                festivals.id,
                festivals.title,
                festivals.festival_date,
                festivals.is_cancelled,
                organizers.name AS organizer_name
            FROM festivals
            JOIN organizers
                ON festivals.organizer_id = organizers.id
            WHERE festivals.venue_id = ?
            ORDER BY festivals.festival_date
            """,
            [venue_id],
        )
    return render(
        request,
        "venues/venue_detail.html",
        context,
        status=404 if venue is None else 200,
    )


def available_venues(request):
    """Поиск площадок, свободных на дату и вмещающих нужное число гостей."""
    festival_date = request.GET.get("date", "")
    visitors = parse_positive_int(request.GET.get("visitors")) or 1
    error = None
    venues_list = []
    if festival_date:
        try:
            date.fromisoformat(festival_date)
        except ValueError:
            error = "Укажите дату в формате ГГГГ-ММ-ДД."
        else:
            venues_list = fetch_all(
                """
                SELECT
                    venues.id,
                    venues.name,
                    venues.address,
                    venues.capacity
                FROM venues
                WHERE venues.capacity >= ?
                  AND venues.id NOT IN (
                      SELECT festivals.venue_id
                      FROM festivals
                      WHERE festivals.festival_date = ?
                        AND festivals.is_cancelled = 0
                  )
                ORDER BY venues.capacity DESC
                """,
                [visitors, festival_date],
            )
    context = {
        "festival_date": festival_date,
        "visitors": visitors,
        "venues": venues_list,
        "error": error,
    }
    return render(request, "venues/available.html", context)
