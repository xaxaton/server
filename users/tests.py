from django.urls import reverse

from rest_framework.test import APITestCase

from users.models import User


CORRECT_DATA_EXAMPLE = {
    "user": {
        "email": "test@mail.ru",
        "name": "Cristiano",
        "surname": "Ronaldo",
        "middle_name": "Dos Santos Aveiro",
        "password": "verygoodpassword123",
    }
}

UNCORRECT_DATA_EXAMPLE = {
    "user": {
        "email": "test@mail.ru",
        "name": "Cristiano",
        "surname": "Ronaldo",
        "middle_name": "Dos Santos Aveiro",
        "password": "badpas",
    }
}


class RegistrationTest(APITestCase):
    def test_registration(self):
        url = reverse("users:register")
        data = UNCORRECT_DATA_EXAMPLE
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        data = CORRECT_DATA_EXAMPLE
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(
            set(response.data.keys()),
            {"email", "name", "surname", "middle_name", "token"},
        )


class LoginTest(APITestCase):
    def setUp(self):
        url = reverse("users:register")
        data = CORRECT_DATA_EXAMPLE
        self.client.post(url, data, format="json")
        user = User.objects.get(email=CORRECT_DATA_EXAMPLE["user"]["email"])
        user.is_active = True
        user.save()

    def test_login(self):
        url = reverse("users:login")
        data = {
            "user": {
                "email": CORRECT_DATA_EXAMPLE["user"]["email"],
                "password": UNCORRECT_DATA_EXAMPLE["user"]["password"],
            }
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        url = reverse("users:login")
        data = {
            "user": {
                "email": CORRECT_DATA_EXAMPLE["user"]["email"],
                "password": CORRECT_DATA_EXAMPLE["user"]["password"],
            }
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.data)
        self.assertIn("token", response.data)
