-- ==========================================
-- FestCity: SQL-запросы проекта
-- Проверка: sqlite3 data/festcity.sqlite
-- Конкретные значения (даты, вместимость) приведены для проверки в CLI;
-- в Django-представлениях они передаются параметрами "?".
-- ==========================================


-- ------------------------------------------
-- Выборка списков
-- ------------------------------------------

-- 1. Список площадок по убыванию вместимости (страница «Площадки»)
SELECT
    id,
    name,
    address,
    capacity
FROM venues
ORDER BY capacity DESC;

-- 2. Список организаторов по алфавиту (страница «Статистика»)
SELECT
    id,
    name,
    email
FROM organizers
ORDER BY name;

-- 3. Три ближайших фестиваля (главная страница): ORDER BY + LIMIT/OFFSET
SELECT
    id,
    title,
    festival_date
FROM festivals
WHERE is_cancelled = 0
  AND festival_date >= '2026-10-26'
ORDER BY festival_date
LIMIT 3 OFFSET 0;


-- ------------------------------------------
-- Фильтрация WHERE
-- ------------------------------------------

-- 4. Площадки, вмещающие не менее 2000 посетителей (поиск по вместимости)
SELECT
    id,
    name,
    capacity
FROM venues
WHERE capacity >= 2000
ORDER BY capacity;

-- 5. Активные (не отменённые) фестивали
SELECT
    id,
    title,
    festival_date,
    expected_visitors
FROM festivals
WHERE is_cancelled = 0
ORDER BY festival_date;

-- 6. Поиск фестиваля по части названия (LIKE).
--    В SQLite LIKE без учёта регистра работает только для латиницы,
--    поэтому «Фестиваль уличной еды» (с заглавной Ф) в результат не входит.
SELECT
    id,
    title,
    festival_date
FROM festivals
WHERE title LIKE '%фестиваль%'
ORDER BY title;

-- 7. Свободные на дату площадки нужной вместимости (несколько условий
--    и подзапрос NOT IN): на 2026-11-14 занят Парк Горького
SELECT
    venues.id,
    venues.name,
    venues.capacity
FROM venues
WHERE venues.capacity >= 1000
  AND venues.id NOT IN (
      SELECT festivals.venue_id
      FROM festivals
      WHERE festivals.festival_date = '2026-11-14'
        AND festivals.is_cancelled = 0
  )
ORDER BY venues.capacity DESC;


-- ------------------------------------------
-- Соединение таблиц JOIN
-- ------------------------------------------

-- 8. Все фестивали с названием площадки и организатором (страница «Фестивали»)
SELECT
    festivals.id,
    festivals.title,
    festivals.festival_date,
    festivals.is_cancelled,
    venues.name AS venue_name,
    organizers.name AS organizer_name
FROM festivals
JOIN venues
    ON festivals.venue_id = venues.id
JOIN organizers
    ON festivals.organizer_id = organizers.id
ORDER BY festivals.festival_date;

-- 9. Полная информация о фестивале с заполненностью площадки
--    (страница фестиваля)
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
WHERE festivals.id = 1;

-- 10. Фестивали на выбранной площадке (страница площадки)
SELECT
    festivals.id,
    festivals.title,
    festivals.festival_date,
    festivals.is_cancelled,
    organizers.name AS organizer_name
FROM festivals
JOIN organizers
    ON festivals.organizer_id = organizers.id
WHERE festivals.venue_id = 1
ORDER BY festivals.festival_date;


-- ------------------------------------------
-- Агрегатные функции
-- ------------------------------------------

-- 11. Сводка по активным фестивалям: количество, посетители, средний,
--     минимальный и максимальный размер (главная и «Статистика»)
SELECT
    COUNT(*) AS festivals_count,
    SUM(expected_visitors) AS visitors_total,
    ROUND(AVG(expected_visitors)) AS visitors_avg,
    MIN(expected_visitors) AS visitors_min,
    MAX(expected_visitors) AS visitors_max,
    MIN(festival_date) AS first_date,
    MAX(festival_date) AS last_date
FROM festivals
WHERE is_cancelled = 0;

-- 12. Количество площадок и их суммарная вместимость
SELECT
    COUNT(*) AS venues_count,
    SUM(capacity) AS capacity_total,
    MAX(capacity) AS capacity_max
FROM venues;


-- ------------------------------------------
-- Группировка GROUP BY и фильтрация групп HAVING
-- ------------------------------------------

-- 13. Количество активных фестивалей и посетителей по площадкам;
--     LEFT JOIN сохраняет площадки без фестивалей (count = 0)
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
ORDER BY festivals_count DESC, venues.name;

-- 14. Нагрузка на организаторов: число фестивалей (включая отменённые)
--     и число отменённых
SELECT
    organizers.id,
    organizers.name AS organizer_name,
    COUNT(festivals.id) AS festivals_count,
    SUM(festivals.is_cancelled) AS cancelled_count
FROM organizers
LEFT JOIN festivals
    ON organizers.id = festivals.organizer_id
GROUP BY organizers.id, organizers.name
ORDER BY festivals_count DESC, organizers.name;

-- 15. Популярные площадки: более одного активного фестиваля (HAVING)
SELECT
    venues.name AS venue_name,
    COUNT(festivals.id) AS festivals_count
FROM venues
JOIN festivals
    ON venues.id = festivals.venue_id
WHERE festivals.is_cancelled = 0
GROUP BY venues.id, venues.name
HAVING COUNT(festivals.id) > 1
ORDER BY festivals_count DESC;

-- 16. Активные фестивали по месяцам проведения
SELECT
    strftime('%Y-%m', festival_date) AS month,
    COUNT(*) AS festivals_count,
    SUM(expected_visitors) AS visitors_total
FROM festivals
WHERE is_cancelled = 0
GROUP BY month
ORDER BY month;
