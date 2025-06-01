#test_config.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ConfigTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаем пользователя для теста
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")

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
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(url, data)  # Используем POST-запрос
        self.assertEqual(response.status_code, 200)
        # Проверяем, что в ответе есть access token
        self.assertIn('access', response.data)