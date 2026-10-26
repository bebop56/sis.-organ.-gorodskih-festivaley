from django.test import TestCase


class PagesTests(TestCase):
    """Проверка страниц веб-интерфейса FestCity."""

    def test_index(self):
        self.assertContains(self.client.get("/"), "FestCity")

    def test_venues_list_and_detail(self):
        self.assertContains(self.client.get("/venues/"), "Парк Горького")
        self.assertContains(self.client.get("/venues/1/"), "Вместимость")

    def test_festivals_list_and_detail(self):
        self.assertContains(self.client.get("/festivals/"), "отменён")
        self.assertContains(self.client.get("/festivals/1/"), "Анна Смирнова")

    def test_missing_objects_return_404(self):
        self.assertEqual(self.client.get("/venues/999/").status_code, 404)
        self.assertEqual(self.client.get("/festivals/999/").status_code, 404)
        self.assertEqual(self.client.get("/nonexistent/").status_code, 404)

    def test_pages_use_templates(self):
        response = self.client.get("/venues/")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "venues/includes/venue_card.html")
        self.assertContains(response, "Найдено площадок: 4")
        self.assertContains(response, "homepage/css/style.css")
        response = self.client.get("/festivals/999/")
        self.assertTemplateUsed(response, "festivals/festival_detail.html")
        self.assertContains(response, "Фестиваль не найден", status_code=404)

    def test_available_venues_search(self):
        response = self.client.get(
            "/venues/available/", {"date": "2026-11-14", "visitors": 1000}
        )
        self.assertNotContains(response, "Парк Горького")
        self.assertContains(response, "Площадь Революции")
        response = self.client.get("/venues/available/", {"date": "oops"})
        self.assertContains(response, "ГГГГ-ММ-ДД")

    def test_capacity_filter_and_active_festivals(self):
        response = self.client.get("/venues/", {"min_capacity": 2000})
        self.assertContains(response, "Найдено площадок: 2")
        response = self.client.get("/festivals/", {"status": "active"})
        self.assertNotContains(response, "Фестиваль фейерверков")

    def test_statistics_page(self):
        response = self.client.get("/festivals/statistics/")
        self.assertTemplateUsed(response, "festivals/statistics.html")
        self.assertContains(response, "Популярные площадки")
        self.assertContains(response, "Анна Смирнова")
