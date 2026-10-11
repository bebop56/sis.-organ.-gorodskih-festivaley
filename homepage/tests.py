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
