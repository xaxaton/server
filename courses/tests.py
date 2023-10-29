from django.urls import reverse

from rest_framework.test import APITestCase

from users.models import Tariff


class ReviewTest(APITestCase):
    def test_get_0(self):
        url = reverse("courses:tariffs")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_get_1(self):
        Tariff.objects.create(name="бесплатный", users_count=1, tests_count=1)
        url = reverse("courses:tariffs")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1, response.data)
