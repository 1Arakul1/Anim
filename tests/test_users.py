# tests/test_users.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from tests.utils import create_user, create_superuser, get_admin_user, create_member_user  # utils.py находится в папке tests
from users.serializers import UserSerializer  # serializers.py находится в папке users
from users.permissions import IsSuperUser, IsSelf  # permissions.py находится в папке users

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        # Создаем суперпользователя и обычного пользователя
        self.admin_user = get_admin_user()
        self.member_user = create_member_user(username="member_test", password="password123", email="member@example.com")

    def test_user_list_superuser_access(self):
        """Проверяем, что суперпользователь может получить список пользователей."""
        self.client.force_authenticate(user=self.admin_user)  # Аутентифицируем клиента как суперпользователя
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_member_access_denied(self):
        """Проверяем, что обычный пользователь не может получить список пользователей."""
        self.client.force_authenticate(user=self.member_user)  # Аутентифицируем клиента как обычного пользователя
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Обычному пользователю должно быть отказано в доступе

    def test_user_detail_superuser_access(self):
        """Проверяем, что суперпользователь может получить информацию о пользователе."""
        self.client.force_authenticate(user=self.admin_user)  # Аутентифицируем клиента как суперпользователя
        url = reverse('user-detail', args=[self.member_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.member_user.username)

    def test_user_detail_self_access(self):
        """Проверяем, что пользователь может получить информацию о себе."""
        self.client.force_authenticate(user=self.member_user)  # Аутентифицируем клиента как обычного пользователя
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
        self.client.force_authenticate(user=self.admin_user)  # Аутентифицируем клиента как суперпользователя
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

    def test_user_creation_by_superuser(self):
        """Проверяем, что суперпользователь может создать пользователя."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('user-list')
        data = {
            'username': 'new_user_api',
            'email': 'new_api@example.com',
            'password': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='new_user_api').exists())

    def test_user_update_self(self):
        """Проверяем, что пользователь может обновить свою информацию."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse('user-detail', args=[self.member_user.pk])
        data = {'username': 'updated_username', 'email': self.member_user.email}  # Обязательно включаем email
        response = self.client.patch(url, data, format='json') # Добавляем format='json'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.member_user.pk).username, 'updated_username')

    def test_user_update_other_denied(self):
        """Проверяем, что пользователь не может обновить информацию другого пользователя."""
        other_user = create_user(username="other_user", password="password123", email="other@example.com")
        self.client.force_authenticate(user=self.member_user)
        url = reverse('user-detail', args=[other_user.pk])
        data = {'username': 'updated_username', 'email': other_user.email}  # Обязательно включаем email
        response = self.client.patch(url, data, format='json') # Добавляем format='json'
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_self(self):
        """Проверяем, что пользователь может удалить свой профиль."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse('user-detail', args=[self.member_user.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.member_user.pk).exists())

    def test_user_delete_other_denied(self):
        """Проверяем, что пользователь не может удалить профиль другого пользователя."""
        other_user = create_user(username="other_user", password="password123", email="other@example.com")
        self.client.force_authenticate(user=self.member_user)
        url = reverse('user-detail', args=[other_user.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
