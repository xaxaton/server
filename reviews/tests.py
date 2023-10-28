from django.urls import reverse

from rest_framework.test import APITestCase


class ReviewTest(APITestCase):
    def test_get(self):
        url = reverse("reviews:all")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_post(self):
        url = reverse("reviews:all")
        data = {"review": {"text": "тест"}}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn("text", response.data["review"])
        self.assertEqual(None, response.data["review"]["video"])
        self.assertEqual(None, response.data["review"]["image"])
