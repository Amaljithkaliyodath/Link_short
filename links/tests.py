from django.test import TestCase
from django.urls import reverse
from .models import ShortURL

class ShortenerTests(TestCase):
    def test_create_and_redirect(self):
        s = ShortURL.objects.create(original_url="https://example.com", code="ex", clicks=0)
        r = self.client.get(reverse("go", args=["ex"]))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r["Location"], "https://example.com")

    def test_expired(self):
        from django.utils import timezone
        s = ShortURL.objects.create(original_url="https://a.co", code="old", clicks=0, expires_at=timezone.now())
        r = self.client.get(reverse("go", args=["old"]))
        self.assertEqual(r.status_code, 404)
