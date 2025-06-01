#test_sections.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from sections.models import Section, Content
from rest_framework.test import force_authenticate  # Import force_authenticate

User = get_user_model()

class SectionTests(APITestCase):
    def setUp(self):
        # Создаем пользователей (суперпользователя и обычного)
        self.admin_user = User.objects.create_superuser(username="admin_test", password="password123", email="admin@example.com")
        self.member_user = User.objects.create_user(username="member_test", password="password123", email="member@example.com")

    def test_section_list_returns_users_sections(self):
        """Проверяем, что пользователь может получить список *своих* разделов."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-list-create')

        # Создаем раздел после аутентификации, чтобы проверить список
        Section.objects.create(title="Section 1", owner=self.member_user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Теперь 1 раздел

    def test_section_create_access(self):
        """Проверяем, что пользователь может создать раздел."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-list-create')
        data = {'title': 'New Section', 'description': 'test'}
        response = self.client.post(url, data, format='json') # format='json'
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Section.objects.count(), 1)  # Cчитаем разделы только для этого теста
        self.assertEqual(Section.objects.last().owner, self.member_user)

    def test_section_detail_owner_access(self):
        """Проверяем, что владелец может получить информацию о *своем* разделе."""
        self.client.force_authenticate(user=self.member_user)
        section = Section.objects.create(title="Section 1", owner=self.member_user, description='test')
        url = reverse('section-detail', args=[section.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], section.title)

    def test_section_detail_other_user_access_denied(self):
        """Проверяем, что другой пользователь не может получить информацию о чужом разделе."""
        other_user = User.objects.create_user(username="other", password="password123", email="other@example.com")  # Создаем другого пользователя
        self.client.force_authenticate(user=self.member_user)  # Аутентифицируем как member
        admin_section = Section.objects.create(title="Section 2", owner=other_user, description='test')  # Раздел другого пользователя
        url = reverse('section-detail', args=[admin_section.pk])  # Пытаемся получить доступ к чужому разделу
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_section_update_owner_access(self):
        """Проверяем, что владелец может обновить информацию о *своем* разделе."""
        self.client.force_authenticate(user=self.member_user)
        section = Section.objects.create(title="Section 1", owner=self.member_user, description='test')
        url = reverse('section-detail', args=[section.pk])
        data = {'title': 'Updated Section', 'description': 'test'} # Добавляем поле description
        response = self.client.patch(url, data, format='json') # format='json'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Section.objects.get(pk=section.pk).title, 'Updated Section')

    def test_section_update_other_user_access_denied(self):
        """Проверяем, что другой пользователь не может обновить информацию о чужом разделе."""
        other_user = User.objects.create_user(username="other", password="password123", email="other@example.com")
        self.client.force_authenticate(user=self.member_user)
        admin_section = Section.objects.create(title="Section 2", owner=other_user, description='test')
        url = reverse('section-detail', args=[admin_section.pk])
        data = {'title': 'Updated Section', 'description': 'test'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_section_delete_owner_access(self):
        """Проверяем, что владелец может удалить *свой* раздел."""
        self.client.force_authenticate(user=self.member_user)
        section = Section.objects.create(title="Section 1", owner=self.member_user, description='test')
        url = reverse('section-detail', args=[section.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Section.objects.filter(pk=section.pk).exists())

    def test_section_delete_other_user_access_denied(self):
        """Проверяем, что другой пользователь не может удалить чужой раздел."""
        other_user = User.objects.create_user(username="other", password="password123", email="other@example.com")
        self.client.force_authenticate(user=self.member_user)
        admin_section = Section.objects.create(title="Section 2", owner=other_user, description='test')
        url = reverse('section-detail', args=[admin_section.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)