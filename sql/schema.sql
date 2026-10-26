-- ==========================================
-- FestCity: структура базы данных
-- ==========================================

-- Площадки города
CREATE TABLE IF NOT EXISTS venues (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    capacity INTEGER NOT NULL CHECK (capacity > 0)
);

-- Организаторы фестивалей
CREATE TABLE IF NOT EXISTS organizers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Фестивали: каждый закреплён за площадкой и организатором
CREATE TABLE IF NOT EXISTS festivals (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    venue_id INTEGER NOT NULL,
    organizer_id INTEGER NOT NULL,
    festival_date TEXT NOT NULL,
    expected_visitors INTEGER NOT NULL CHECK (expected_visitors > 0),
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (venue_id) REFERENCES venues(id),
    FOREIGN KEY (organizer_id) REFERENCES organizers(id)
);
