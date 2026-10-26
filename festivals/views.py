from datetime import date

from django.shortcuts import render

from db.database import fetch_all, fetch_one


def festivals(request):
    """Фестивали с площадкой и организатором; ?status=active – без отмен."""
    only_active = request.GET.get("status") == "active"
    festivals_list = fetch_all(
        """
        SELECT
            festivals.id,
            festivals.title,
            festivals.festival_date,
            festivals.expected_visitors,
            festivals.is_cancelled,
            venues.name AS venue_name,
            organizers.name AS organizer_name
        FROM festivals
        JOIN venues
            ON festivals.venue_id = venues.id
        JOIN organizers
            ON festivals.organizer_id = organizers.id
        WHERE ? = 0 OR festivals.is_cancelled = 0
        ORDER BY festivals.festival_date
        """,
        [int(only_active)],
    )
    context = {
        "festivals": festivals_list,
        "only_active": only_active,
    }
    return render(request, "festivals/festival_list.html", context)


def festival_detail(request, festival_id):
    """Карточка фестиваля со связанными площадкой и организатором."""
    festival = fetch_one(
        """
        SELECT
            festivals.id,
            festivals.title,
            festivals.festival_date,
            festivals.expected_visitors,
            festivals.is_cancelled,
            venues.id AS venue_id,
            venues.name AS venue_name,
            venues.capacity,
            organizers.name AS organizer_name,
            organizers.email AS organizer_email,
            ROUND(festivals.expected_visitors * 100.0 / venues.capacity)
                AS load_percent
        FROM festivals
        JOIN venues
            ON festivals.venue_id = venues.id
        JOIN organizers
            ON festivals.organizer_id = organizers.id
        WHERE festivals.id = ?
        """,
        [festival_id],
    )
    context = {"festival": festival}
    if festival is not None:
        context["days_left"] = (festival["festival_date"] - date.today()).days
    return render(
        request,
        "festivals/festival_detail.html",
        context,
        status=404 if festival is None else 200,
    )


def statistics(request):
    """Статистика по площадкам, организаторам и месяцам."""
    summary = fetch_one(
        """
        SELECT
            COUNT(*) AS festivals_count,
            COALESCE(SUM(expected_visitors), 0) AS visitors_total,
            ROUND(AVG(expected_visitors)) AS visitors_avg,
            MIN(expected_visitors) AS visitors_min,
            MAX(expected_visitors) AS visitors_max,
            MIN(festival_date) AS first_date,
            MAX(festival_date) AS last_date
        FROM festivals
        WHERE is_cancelled = 0
        """
    )
    by_venue = fetch_all(
        """
        SELECT
            venues.id,
            venues.name AS venue_name,
            COUNT(festivals.id) AS festivals_count,
            COALESCE(SUM(festivals.expected_visitors), 0) AS visitors_total
        FROM venues
        LEFT JOIN festivals
            ON venues.id = festivals.venue_id
           AND festivals.is_cancelled = 0
        GROUP BY venues.id, venues.name
        ORDER BY festivals_count DESC, venues.name
        """
    )
    by_organizer = fetch_all(
        """
        SELECT
            organizers.id,
            organizers.name AS organizer_name,
            organizers.email,
            COUNT(festivals.id) AS festivals_count,
            COALESCE(SUM(festivals.is_cancelled), 0) AS cancelled_count
        FROM organizers
        LEFT JOIN festivals
            ON organizers.id = festivals.organizer_id
        GROUP BY organizers.id, organizers.name, organizers.email
        ORDER BY festivals_count DESC, organizers.name
        """
    )
    popular_venues = fetch_all(
        """
        SELECT
            venues.name AS venue_name,
            COUNT(festivals.id) AS festivals_count
        FROM venues
        JOIN festivals
            ON venues.id = festivals.venue_id
        WHERE festivals.is_cancelled = 0
        GROUP BY venues.id, venues.name
        HAVING COUNT(festivals.id) > ?
        ORDER BY festivals_count DESC
        """,
        [1],
    )
    by_month = fetch_all(
        """
        SELECT
            strftime('%Y-%m', festival_date) AS month,
            COUNT(*) AS festivals_count,
            SUM(expected_visitors) AS visitors_total
        FROM festivals
        WHERE is_cancelled = 0
        GROUP BY month
        ORDER BY month
        """
    )
    context = {
        "summary": summary,
        "by_venue": by_venue,
        "by_organizer": by_organizer,
        "popular_venues": popular_venues,
        "by_month": by_month,
    }
    return render(request, "festivals/statistics.html", context)
