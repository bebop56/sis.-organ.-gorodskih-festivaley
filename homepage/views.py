from django.conf import settings
from django.http import HttpResponse

from models.festivals import festivals_statistics
from storage import load_all

BOOTSTRAP = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)


def page(title, content):
    """Собрать HTML-документ с общим каркасом и навигацией."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP}">
    <style>
        body {{ background: #f6f4ef; }}
        .navbar-brand {{ font-weight: 700; letter-spacing: .5px; }}
        main {{ padding-top: 2rem; padding-bottom: 3rem; }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">FestCity</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/venues/">Площадки</a>
                <a class="nav-link" href="/festivals/">Фестивали</a>
            </div>
        </div>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница: описание приложения и навигация."""
    venues, _, festivals = load_all(settings.DATA_DIR)
    stats = festivals_statistics(festivals)
    content = f"""
    <div class="p-5 mb-4 bg-white rounded-3 shadow-sm">
        <h1 class="display-5">FestCity</h1>
        <p class="lead">
            Система организации городских фестивалей: подбор площадок
            по вместимости и планирование мероприятий без накладок по датам.
        </p>
        <a href="/venues/" class="btn btn-primary me-2">Площадки</a>
        <a href="/festivals/" class="btn btn-outline-dark">Фестивали</a>
    </div>
    <div class="row g-3">
        <div class="col-sm-4">
            <div class="card text-center"><div class="card-body">
                <div class="display-6">{len(venues)}</div>
                <div class="text-muted">площадок в городе</div>
            </div></div>
        </div>
        <div class="col-sm-4">
            <div class="card text-center"><div class="card-body">
                <div class="display-6">{stats['festivals']}</div>
                <div class="text-muted">активных фестивалей</div>
            </div></div>
        </div>
        <div class="col-sm-4">
            <div class="card text-center"><div class="card-body">
                <div class="display-6">{stats['visitors']}</div>
                <div class="text-muted">ожидаемых посетителей</div>
            </div></div>
        </div>
    </div>
    """
    return HttpResponse(page("FestCity – городские фестивали", content))


def page_not_found(request, exception):
    """Собственная страница ошибки 404."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
