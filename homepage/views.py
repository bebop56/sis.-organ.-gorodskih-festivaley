from django.conf import settings
from django.shortcuts import render

from models.festivals import festivals_statistics
from storage import load_all


def index(request):
    """Главная страница: описание приложения и статистика."""
    venues, _, festivals = load_all(settings.DATA_DIR)
    context = {
        "venues_count": len(venues),
        "stats": festivals_statistics(festivals),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request, exception):
    """Собственная страница ошибки 404."""
    return render(request, "homepage/404.html", status=404)
