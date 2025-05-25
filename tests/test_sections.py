from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from tests.utils import create_user, get_admin_user, create_member_user
from sections.models import Section, Content
from sections.serializers import SectionSerializer, ContentSerializer

User = get_user_model()

class SectionTests(APITestCase):
    def setUp(self):
        self.admin_user = get_admin_user()
        self.member_user = create_member_user(username="member_test", password="password123", email="member@example.com")

        self.section1 = Section.objects.create(title="Section 1", owner=self.member_user)
        self.section2 = Section.objects.create(title="Section 2", owner=self.admin_user)

    def test_section_list_access(self):
        """Проверяем, что пользователь может получить список *своих* разделов."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Должен быть только 1 раздел, принадлежащий member_user

    def test_section_create_access(self):
        """Проверяем, что пользователь может создать раздел."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-list-create')
        data = {'title': 'New Section'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Section.objects.count(), 3)
        self.assertEqual(Section.objects.last().owner, self.member_user)

    def test_section_detail_owner_access(self):
        """Проверяем, что владелец может получить информацию о *своем* разделе."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-detail', args=[self.section1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.section1.title)

    def test_section_detail_other_user_access_denied(self):
        """Проверяем, что другой пользователь не может получить информацию о чужом разделе."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-detail', args=[self.section2.pk])  # Пытаемся получить доступ к разделу, принадлежащему админу
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)