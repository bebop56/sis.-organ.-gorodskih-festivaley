# FestCity – система организации городских фестивалей

## Назначение

FestCity – приложение для планирования городских фестивалей.
Оно помогает организаторам подобрать городскую площадку подходящей
вместимости и закрепить её за фестивалем на нужную дату так, чтобы
на одной площадке в один день не проходило два мероприятия.

Консольная версия (ПР1–ПР3) дополнена веб-интерфейсом на Django (ПР5),
страницы которого построены на системе шаблонов Django (ПР6).
С ПР7 веб-страницы получают данные из базы SQLite с помощью SQL-запросов
(модуль `sqlite3` стандартной библиотеки, без Django ORM).

Как установить и запустить проект на Windows – см. раздел
[«Запуск на Windows (пошагово)»](#запуск-на-windows-пошагово).

## Целевая аудитория

- организаторы фестивалей (творческие коллективы, НКО, ивент-агентства);
- сотрудники городского отдела культуры, распределяющие площадки;
- жители города, которые хотят узнать, где и когда пройдёт фестиваль.

## Предметная область

Город располагает набором площадок (парки, набережные, площади,
концертные залы). У каждой площадки есть вместимость. Организатор
планирует фестиваль: указывает название, дату и ожидаемое число
посетителей и выбирает площадку. Площадка подходит, если её
вместимость не меньше ожидаемого числа посетителей и на эту дату она
не занята другим фестивалем. Запланированный фестиваль можно отменить –
тогда площадка снова становится свободной.

## Основные сущности

- **Площадка** (Venue) – место проведения: название, адрес, вместимость;
- **Организатор** (Organizer) – пользователь системы: имя, e-mail;
- **Фестиваль** (Festival) – мероприятие: название, дата, площадка,
  организатор, ожидаемое число посетителей, признак отмены.

## Основные функции

- проверка вместимости площадки для ожидаемого числа посетителей;
- проверка, свободна ли площадка на выбранную дату;
- расчёт количества дней до начала фестиваля;
- планирование (бронирование площадки) фестиваля;
- отмена фестиваля;
- просмотр и поиск площадок и фестивалей.

## Возможности консольной версии

- просмотр площадок (с сортировкой по вместимости) и поиск по названию;
- подбор площадок по вместимости;
- проверка, свободна ли площадка на дату;
- планирование фестиваля с проверкой вместимости и занятости;
- отмена фестиваля (отменённый фестиваль не блокирует площадку);
- добавление площадок и организаторов, поиск организаторов;
- статистика по активным фестивалям;
- хранение данных между запусками в JSON-файлах.

## Используемые технологии

- Python 3.11+;
- Django 5.2 – веб-фреймворк;
- Django Template Language (DTL) – шаблоны страниц;
- HTML – разметка страниц;
- CSS (собственный `style.css`) и Bootstrap 5.3 – оформление страниц;
- JavaScript (`main.js`) – небольшое поведение интерфейса;
- SQLite и SQL (`sqlite3`) – реляционное хранение данных;
- pytest – автоматизированные тесты;
- flake8 – проверка качества кода.

## Страницы веб-интерфейса

| URL | Имя маршрута | View-функция | Шаблон |
|-----|--------------|--------------|--------|
| `/` | `homepage:index` | `homepage.views.index` | `homepage/index.html` |
| `/venues/` | `venues:list` | `venues.views.venues` | `venues/venue_list.html` |
| `/venues/?min_capacity=N` | `venues:list` | `venues.views.venues` | `venues/venue_list.html` |
| `/venues/available/?date=&visitors=` | `venues:available` | `venues.views.available_venues` | `venues/available.html` |
| `/venues/<int:venue_id>/` | `venues:detail` | `venues.views.venue_detail` | `venues/venue_detail.html` |
| `/festivals/` | `festivals:list` | `festivals.views.festivals` | `festivals/festival_list.html` |
| `/festivals/?status=active` | `festivals:list` | `festivals.views.festivals` | `festivals/festival_list.html` |
| `/festivals/statistics/` | `festivals:statistics` | `festivals.views.statistics` | `festivals/statistics.html` |
| `/festivals/<int:festival_id>/` | `festivals:detail` | `festivals.views.festival_detail` | `festivals/festival_detail.html` |

Если площадка или фестиваль не найдены, шаблон выводит сообщение
(`{% if %}` / `{% else %}`), а `render()` возвращает код 404.
Для неизвестных адресов подключён `handler404 = "homepage.views.page_not_found"`
(шаблон `homepage/404.html`, работает при `DEBUG = False`).

## Шаблоны Django (ПР6)

HTML больше не формируется в Python: функция `page()` из ПР5 удалена,
все view-функции подготавливают данные и вызывают
`render(request, "<шаблон>", context)`.

- **Базовый шаблон** `templates/base.html` (каталог уровня проекта,
  подключён через `TEMPLATES["DIRS"] = [BASE_DIR / "templates"]`):
  HTML-каркас, Bootstrap, собственный CSS, навигация, подвал, JavaScript;
  блоки `{% block title %}` и `{% block content %}`.
- **Наследование**: все страницы начинаются с `{% extends "base.html" %}`.
- **Включаемые шаблоны** (`{% include %}`):
  `templates/includes/navigation.html` – меню сайта,
  `venues/includes/venue_card.html` – карточка площадки,
  `festivals/includes/festival_status.html` – статус фестиваля
  (используется в списке фестивалей, карточке фестиваля и на странице площадки).
- **Контекст**: например, `{"venues": sort_venues(...)}` →
  `{% for venue in venues %}`.
- **Циклы и условия**: `{% for %}` с `{% empty %}` для пустых списков,
  `{% if festival.is_cancelled %}` для статуса, `{% if available %}` для
  доступности площадки.
- **Именованные URL и пространства имён**: в каждом `urls.py` задан
  `app_name`; ссылки строятся через `{% url 'venues:detail' venue.id %}`,
  жёстко заданных адресов в шаблонах нет.
- **Фильтры**: `|length` (количество площадок и фестивалей),
  `|default:"Без названия"`, `|date:"d.m.Y"` (даты фестивалей), `|lower`
  (e-mail организатора); тег `{% now "d.m.Y" %}` выводит текущую дату.
- **Статические файлы** (`homepage/static/homepage/`):
  `css/style.css` – собственные стили (шапка, карточки, статусы, подвал),
  `js/main.js` – текущий год в подвале и подсветка фестивалей,
  до которых осталось меньше 30 дней,
  `img/logo.png` – логотип в навигации. Подключаются через
  `{% load static %}` и `{% static '...' %}`.

В ПР6 view-функции получали данные из JSON через `storage.load_all()`;
в ПР7 источником данных веб-части стала база SQLite (см. ниже).

## База данных SQLite (ПР7)

Данные предметной области перенесены из JSON в реляционную базу
`data/festcity.sqlite`. JSON-файлы и консольная версия сохранены как
предыдущая реализация; Django ORM на этом этапе не используется.

### Структура таблиц

`venues` – площадки:

| Поле | Тип | Назначение |
|------|-----|------------|
| `id` | INTEGER | первичный ключ |
| `name` | TEXT NOT NULL | название |
| `address` | TEXT | адрес (может отсутствовать) |
| `capacity` | INTEGER NOT NULL, CHECK > 0 | вместимость |

`organizers` – организаторы:

| Поле | Тип | Назначение |
|------|-----|------------|
| `id` | INTEGER | первичный ключ |
| `name` | TEXT NOT NULL | имя |
| `email` | TEXT NOT NULL UNIQUE | e-mail |

`festivals` – фестивали:

| Поле | Тип | Назначение |
|------|-----|------------|
| `id` | INTEGER | первичный ключ |
| `title` | TEXT NOT NULL | название |
| `venue_id` | INTEGER NOT NULL | внешний ключ → `venues.id` |
| `organizer_id` | INTEGER NOT NULL | внешний ключ → `organizers.id` |
| `festival_date` | TEXT NOT NULL | дата в формате `YYYY-MM-DD` |
| `expected_visitors` | INTEGER NOT NULL, CHECK > 0 | ожидаемое число посетителей |
| `is_cancelled` | INTEGER NOT NULL DEFAULT 0 | 0 – активен, 1 – отменён |

```text
festivals
 ├── venue_id     → venues.id
 └── organizer_id → organizers.id
```

### Файлы слоя базы данных

- `sql/schema.sql` – команды `CREATE TABLE IF NOT EXISTS` (повторный запуск безопасен);
- `sql/queries.sql` – 16 проверенных запросов с комментариями;
- `db/database.py` – `get_connection()` (`sqlite3.connect`,
  `PRAGMA foreign_keys = ON`, `row_factory = sqlite3.Row`),
  `create_schema()`, `fetch_all()` / `fetch_one()` для параметризованных
  запросов (поля `*_date` преобразуются в `date` для фильтра `|date`);
- `db/import_json.py` – перенос данных из JSON: создаёт схему, очищает
  таблицы и вставляет записи через `executemany()` с параметрами `?`
  (сначала площадки и организаторы, затем фестивали), `commit()` /
  `rollback()`.

Создание базы и перенос данных (из корня проекта):

```powershell
python -m db.import_json
```

### SQL-запросы (`sql/queries.sql`)

| № | Вид | Задача | Где используется |
|---|-----|--------|------------------|
| 1 | список | площадки по вместимости | `/venues/` |
| 2 | список | организаторы по алфавиту | проверка в CLI |
| 3 | список, LIMIT | три ближайших фестиваля | `/` |
| 4 | WHERE | площадки вместимостью не менее N | `/venues/?min_capacity=N` |
| 5 | WHERE | активные фестивали | `/festivals/?status=active` |
| 6 | WHERE, LIKE | поиск фестиваля по части названия | проверка в CLI |
| 7 | WHERE, подзапрос NOT IN | свободные на дату площадки нужной вместимости | `/venues/available/` |
| 8 | JOIN | фестивали с площадкой и организатором | `/festivals/` |
| 9 | JOIN | полная информация о фестивале, заполненность | `/festivals/<id>/` |
| 10 | JOIN | фестивали на площадке | `/venues/<id>/` |
| 11 | COUNT, SUM, AVG, MIN, MAX | сводка по активным фестивалям | `/`, `/festivals/statistics/` |
| 12 | COUNT, SUM | число площадок и суммарная вместимость | `/` |
| 13 | LEFT JOIN, GROUP BY | загрузка площадок | `/festivals/statistics/` |
| 14 | LEFT JOIN, GROUP BY | фестивали и отмены по организаторам | `/festivals/statistics/` |
| 15 | GROUP BY, HAVING | площадки с более чем одним активным фестивалем | `/festivals/statistics/` |
| 16 | GROUP BY | фестивали по месяцам | `/festivals/statistics/` |

Все значения, полученные от пользователя (дата, вместимость, id из URL),
передаются в запросы параметрами `?`; f-строки и конкатенация для
подстановки значений не используются.

### Сопоставление с предыдущей реализацией

| ПР3–ПР6 (JSON + Python) | ПР7 (SQLite + SQL) |
|-------------------------|--------------------|
| `find_venue_by_id()` | `WHERE id = ?` |
| `sort_venues()` | `ORDER BY capacity DESC` |
| `filter_venues_by_capacity()` | `WHERE capacity >= ?` |
| `is_venue_available()` | подзапрос `NOT IN` по дате и `is_cancelled = 0` |
| связи `festival.venue`, `festival.organizer` | `JOIN venues`, `JOIN organizers` |
| `festivals_statistics()` | `COUNT()`, `SUM()`, `GROUP BY` |

### Отложено до следующих работ

Операции, изменяющие данные (планирование и отмена фестиваля,
добавление площадок и организаторов, поиск), работают в консольной версии
и появятся в вебе вместе с формами и POST-запросами.

## Классы предметной области (ПР3)

### Entity – базовая сущность (`models/base.py`)

Общий предок всех классов. Хранит идентификатор `id` (свойство только
для чтения) и объявляет метод `to_data()`, который каждый наследник
переопределяет по-своему. Благодаря этому `storage.save_entities()`
сохраняет площадки, организаторов и фестивали одним и тем же кодом
(наследование и полиморфизм).

### Venue – площадка (`models/venues.py`)

- атрибуты: `id`, `name`, `address`, `capacity`;
- `capacity` – свойство (`@property`) с проверкой значения (инкапсуляция);
- методы: `is_suitable_for(visitors)`, `validate_capacity()`
  (`@staticmethod`), `from_data()` (`@classmethod`), `to_data()`, `__str__()`.

### Organizer – организатор (`models/organizers.py`)

- атрибуты: `id`, `name`, `email` (e-mail проверяется в конструкторе);
- методы: `from_data()` (`@classmethod`), `to_data()`, `__str__()`.

### Festival – фестиваль (`models/festivals.py`)

- атрибуты: `id`, `title`, `venue` (объект `Venue`), `festival_date`,
  `organizer` (объект `Organizer`), `expected_visitors`, `is_cancelled`;
- методы: `cancel()`, `blocks(venue, date)`, `days_until(today)`,
  `to_data()`, `__str__()`.

### Взаимодействие объектов

```text
Festival
 ├── venue     → Venue
 └── organizer → Organizer
```

Фестиваль хранит ссылки на объекты площадки и организатора.
В JSON вместо ссылок записываются `venue_id` и `organizer_id`;
при загрузке `storage.load_festivals()` находит объекты по id
и восстанавливает связи. Одна площадка не может иметь два активных
фестиваля в один день; отменённый фестиваль остаётся в списке,
но площадку не занимает.

## Структура проекта

```text
city_festivals/
├── README.md
├── requirements.txt
├── setup.cfg            – настройки flake8 и pytest
├── manage.py            – управление Django-проектом
├── main.py              – консольная версия (меню и сценарии)
├── storage.py           – JSON ⇄ объекты, load_all()
├── utils.py             – безопасный ввод чисел и дат
├── festcity/            – пакет настроек Django-проекта
│   ├── settings.py
│   ├── urls.py          – корневые маршруты и handler404
│   ├── asgi.py
│   └── wsgi.py
├── templates/           – шаблоны уровня проекта
│   ├── base.html        – базовый шаблон
│   └── includes/
│       └── navigation.html
├── homepage/            – главная страница и страница 404
│   ├── templates/homepage/
│   │   ├── index.html
│   │   └── 404.html
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/logo.png
│   ├── urls.py
│   ├── views.py
│   └── tests.py         – тесты страниц (python manage.py test)
├── venues/              – веб-страницы площадок
│   ├── templates/venues/
│   │   ├── venue_list.html
│   │   ├── available.html
│   │   ├── venue_detail.html
│   │   └── includes/venue_card.html
│   ├── urls.py
│   └── views.py
├── festivals/           – веб-страницы фестивалей
│   ├── templates/festivals/
│   │   ├── festival_list.html
│   │   ├── festival_detail.html
│   │   ├── statistics.html
│   │   └── includes/festival_status.html
│   ├── urls.py
│   └── views.py
├── models/              – классы предметной области (ПР3)
│   ├── base.py          – Entity
│   ├── venues.py        – Venue и функции площадок
│   ├── organizers.py    – Organizer и функции организаторов
│   └── festivals.py     – Festival и функции фестивалей
├── db/                  – слой базы данных (ПР7)
│   ├── __init__.py
│   ├── database.py      – подключение к SQLite
│   └── import_json.py   – перенос данных из JSON
├── sql/
│   ├── schema.sql       – создание таблиц
│   └── queries.sql      – SQL-запросы проекта
├── data/
│   ├── venues.json
│   ├── organizers.json
│   ├── festivals.json
│   └── festcity.sqlite  – база данных SQLite
└── tests/               – тесты pytest (в т.ч. test_database.py)
```

## Запуск на Windows (пошагово)

Инструкция для Windows 10/11. Все команды выполняются в **PowerShell**
(Пуск → «PowerShell») или во встроенном терминале VS Code.

### Шаг 1. Установить Python и Git

1. **Python 3.11 или новее** – скачать с https://www.python.org/downloads/windows/.
   В первом окне установщика обязательно отметить
   **«Add python.exe to PATH»**, затем нажать «Install Now».
2. **Git** – скачать с https://git-scm.com/download/win и установить
   с настройками по умолчанию.
3. Закрыть и заново открыть PowerShell, проверить установку:

```powershell
python --version
git --version
```

Должны вывестись версии, например `Python 3.12.x` и `git version 2.x`.

> Если вместо версии Python открывается Microsoft Store – Python не
> добавлен в PATH. Используйте команду `py` вместо `python`
> (например, `py -m venv venv`) или переустановите Python с галочкой
> «Add python.exe to PATH».

### Шаг 2. Скачать проект

```powershell
cd $HOME\Desktop
git clone https://github.com/bebop56/sis.-organ.-gorodskih-festivaley.git
cd sis.-organ.-gorodskih-festivaley
```

Без Git: на странице репозитория нажать **Code → Download ZIP**,
распаковать архив и перейти в распакованную папку командой `cd`.
Если в пути есть пробелы, путь берётся в кавычки:
`cd "C:\Users\Имя\Desktop\моя папка\sis.-organ.-gorodskih-festivaley"`.

Все дальнейшие команды выполняются **из этой папки** (в ней лежит
`manage.py`).

### Шаг 3. Создать и активировать виртуальное окружение

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

После активации в начале строки появится `(venv)`.

> Если PowerShell пишет, что выполнение сценариев отключено
> (`running scripts is disabled on this system`), один раз выполните
> команду ниже и повторите активацию:
>
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
>
> В обычной командной строке (cmd) окружение активируется командой
> `venv\Scripts\activate.bat`.

### Шаг 4. Установить зависимости

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Устанавливаются Django 5.2, pytest и flake8. Проверка:

```powershell
python -m django --version
```

### Шаг 5. Создать базу данных SQLite

Файл `data/festcity.sqlite` уже есть в репозитории, но его можно
пересоздать из JSON-файлов в любой момент (команда безопасна
при повторном запуске):

```powershell
python -m db.import_json
```

Ожидаемый вывод:

```text
venues: 4
organizers: 3
festivals: 7
```

### Шаг 6. Запустить веб-версию

```powershell
python manage.py check
python manage.py runserver
```

`check` должен вывести `System check identified no issues (0 silenced).`
Сообщение runserver о непримененных миграциях (`unapplied migration(s)`)
можно игнорировать: таблицы Django ORM в проекте пока не используются,
данные берутся из `data/festcity.sqlite`.

Открыть в браузере http://127.0.0.1:8000/ и проверить страницы:

| Адрес | Что открывается |
|-------|-----------------|
| http://127.0.0.1:8000/ | главная: сводка и ближайшие фестивали |
| http://127.0.0.1:8000/venues/ | список площадок, фильтр по вместимости |
| http://127.0.0.1:8000/venues/1/ | карточка площадки |
| http://127.0.0.1:8000/venues/available/ | поиск свободных площадок на дату |
| http://127.0.0.1:8000/festivals/ | список фестивалей (кнопка «Только активные») |
| http://127.0.0.1:8000/festivals/1/ | карточка фестиваля |
| http://127.0.0.1:8000/festivals/statistics/ | статистика |

Остановить сервер – **Ctrl+C** в окне PowerShell.

### Шаг 7. Консольная версия (по желанию)

```powershell
python main.py
```

Работа ведётся через меню из пунктов 0–12; данные консольной версии
хранятся в `data/*.json` и сохраняются при выходе (пункт 0).
Чтобы изменения из консольной версии появились на сайте, после неё
выполните `python -m db.import_json`.

### Шаг 8. Тесты и проверка кода (по желанию)

```powershell
pytest -v
python manage.py test
flake8 . --extend-exclude=venv
```

### Повторный запуск

При следующем запуске достаточно открыть PowerShell в папке проекта и
выполнить:

```powershell
venv\Scripts\Activate.ps1
python manage.py runserver
```

Выйти из виртуального окружения – команда `deactivate`.

### Частые проблемы

| Проблема | Решение |
|----------|---------|
| `python` открывает Microsoft Store или «не является командой» | использовать `py` вместо `python` или переустановить Python с галочкой «Add python.exe to PATH» |
| `running scripts is disabled on this system` | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| `No module named 'django'` | не активировано окружение: `venv\Scripts\Activate.ps1`, затем `pip install -r requirements.txt` |
| `can't open file 'manage.py'` | команда выполняется не из папки проекта – перейдите в неё через `cd` |
| `no such table: venues` | база не создана: `python -m db.import_json` |
| `Error: That port is already in use` | порт 8000 занят: `python manage.py runserver 8001` и открыть http://127.0.0.1:8001/ |
| в консоли вместо русских букв «кракозябры» | выполнить `chcp 65001` перед запуском `python main.py` |

## Запуск тестов

Тесты проверяют классы (атрибуты, `__str__`, проверки значений),
функции коллекций, запрет двойного бронирования площадки, отмену
фестиваля и восстановление связей при загрузке из JSON, а также
создание базы SQLite, импорт данных, проверку внешних ключей
и SQL-запрос поиска свободных площадок (`tests/test_database.py`).

```powershell
pytest -v
python manage.py test
```

## Проверка качества кода

```powershell
flake8 . --extend-exclude=venv
```

## Текущее состояние и план развития

Реализовано:

- ПР1 – начальный сценарий проверки площадки;
- ПР2 – модули, коллекции, JSON-хранилище, исключения, тесты;
- ПР3 – объектная модель (Entity, Venue, Organizer, Festival);
- ПР5 – Django-проект, три приложения, маршрутизация, страницы на Bootstrap;
- ПР6 – шаблоны Django (наследование, include, контекст, циклы, условия,
  фильтры, именованные URL), собственные CSS, JavaScript и изображение;
- ПР7 – база данных SQLite, перенос данных из JSON, SQL-запросы,
  страницы поиска свободных площадок и статистики на данных из базы.

На следующих этапах планируется:

- переход от SQL-запросов к моделям Django ORM;
- формы планирования и отмены фестивалей;
- регистрация и вход организаторов;
- разработка API;
- контейнеризация приложения;
- настройка CI/CD.
