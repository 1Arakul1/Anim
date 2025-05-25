# tests/test_users.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from tests.utils import create_user, get_admin_user, create_member_user  # utils.py находится в папке tests
from users.serializers import UserSerializer  # serializers.py находится в папке users
from users.permissions import IsSuperUser, IsSelf  # permissions.py находится в папке users

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.admin_user = get_admin_user()  # Создаем суперпользователя
        self.member_user = create_member_user(username="member_test", password="password123", email="member@example.com")
        self.client.force_authenticate(user=self.admin_user)  # Аутентифицируем клиента как суперпользователя

    def test_user_list_superuser_access(self):
        """Проверяем, что суперпользователь может получить список пользователей."""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_member_access_denied(self):
        """Проверяем, что обычный пользователь не может получить список пользователей."""
        self.client.force_authenticate(user=self.member_user) # Аутентифицируем клиента как обычного пользователя
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Обычному пользователю должно быть отказано в доступе

    def test_user_detail_superuser_access(self):
        """Проверяем, что суперпользователь может получить информацию о пользователе."""
        url = reverse('user-detail', args=[self.member_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.member_user.username)

    def test_user_detail_self_access(self):
        """Проверяем, что пользователь может получить информацию о себе."""
        self.client.force_authenticate(user=self.member_user) # Аутентифицируем клиента как обычного пользователя
        url = reverse('user-detail', args=[self.member_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.member_user.username)

    def test_user_detail_other_user_access_denied(self):
        """Проверяем, что пользователь не может получить информацию о другом пользователе."""
        other_user = create_user(username="other_user", password="password123", email="other@example.com")
        self.client.force_authenticate(user=self.member_user)  # Аутентифицируем клиента как обычного пользователя
        url = reverse('user-detail', args=[other_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_serializer(self):
        """Проверяем создание пользователя через сериализатор."""
        data = {
            'username': 'new_user',
            'email': 'new@example.com',
            'password': 'password123',
            'password2': 'password123'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'new_user')
        self.assertTrue(user.check_password('password123'))