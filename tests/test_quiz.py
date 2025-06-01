#test_quiz.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from quiz.models import QuestionCategory, Question, Answer
from django.core.management import call_command
from rest_framework import permissions
import logging
import time

logger = logging.getLogger(__name__)

User = get_user_model()

class QuizTests(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.admin_user = User.objects.create_superuser(username="admin_test", password="password123", email="admin@example.com")
        self.member_user = User.objects.create_user(username="member_test", password="password123", email="member@example.com")
        self.client.force_authenticate(user=self.member_user)  # Аутентифицируем member_user

        # Загружаем данные викторины
        call_command('load_quiz_data')

        # Убедимся, что данные загружены
        self.assertGreater(Question.objects.count(), 0, "Не удалось загрузить данные викторины")  # Добавлена проверка

        # Получаем первый вопрос и ответы
        self.question = Question.objects.first()
        self.correct_answer = Answer.objects.filter(question=self.question, is_correct=True).first()
        self.incorrect_answer = Answer.objects.filter(question=self.question, is_correct=False).first()

    def test_check_answer_correct(self):
        """Проверяем, что эндпоинт проверки ответа возвращает правильный результат для правильного ответа."""
        self.client.force_authenticate(user=self.member_user)
        if not self.question or not self.correct_answer:
            self.skipTest("Не найден вопрос или правильный ответ. Убедитесь, что данные викторины загружены.")

        url = reverse('check_answer')
        data = {'question_id': self.question.pk, 'answer_id': self.correct_answer.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_correct'], True)
        self.assertEqual(response.data['question_text'], self.question.text)

    def test_check_answer_incorrect(self):
        """Проверяем, что эндпоинт проверки ответа возвращает правильный результат для неправильного ответа."""
        self.client.force_authenticate(user=self.member_user)
        if not self.question or not self.incorrect_answer:
            self.skipTest("Не найден вопрос или неправильный ответ. Убедитесь, что данные викторины загружены.")

        url = reverse('check_answer')
        data = {'question_id': self.question.pk, 'answer_id': self.incorrect_answer.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_correct'], False)
        self.assertEqual(response.data['question_text'], self.question.text)

    def test_check_answer_question_not_found(self):
        """Проверяем, что эндпоинт проверки ответа возвращает ошибку, если вопрос не найден."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse('check_answer')
        data = {'question_id': 99999, 'answer_id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_check_answer_answer_not_found(self):
        """Проверяем, что эндпоинт проверки ответа возвращает ошибку, если ответ не найден или не связан с вопросом."""
        self.client.force_authenticate(user=self.member_user)
        if not self.question:
            self.skipTest("Не найден вопрос. Убедитесь, что данные викторины загружены.")

        url = reverse('check_answer')
        data = {'question_id': self.question.pk, 'answer_id': 99999}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_question_category_list_create_by_member_forbidden(self):
        """Проверяем, что обычный пользователь не может создать категорию."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse('category-list-create')
        data = {'name': 'New category'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Обычному пользователю должно быть отказано

    def test_question_category_list_create_by_admin(self):
        """Проверяем создание и получение QuestionCategory только админом"""
        self.client.force_authenticate(user=self.admin_user) # Аутентифицируем как админ
        url = reverse('category-list-create')
        initial_count = QuestionCategory.objects.count()
        data = {'name': 'New category'}
        response_post = self.client.post(url, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), initial_count + 1)
        self.assertEqual(response_get.data[-1]['name'], 'New category')