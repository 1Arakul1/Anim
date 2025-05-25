from django.test import TestCase, Client
from django.urls import reverse

class ConfigTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_swagger_ui_accessible(self):
        """Проверяем, что UI Swagger доступен."""
        url = reverse('schema-swagger-ui')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_redoc_ui_accessible(self):
        """Проверяем, что UI Redoc доступен."""
        url = reverse('schema-redoc')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_token_obtain_pair_accessible(self):
        """Проверяем, что эндпоинт получения токена доступен."""
        url = reverse('token_obtain_pair')
        response = self.client.get(url)  # GET is not allowed
        self.assertEqual(response.status_code, 405)  # Method Not Allowed