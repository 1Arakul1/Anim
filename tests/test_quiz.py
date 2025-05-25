from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from tests.utils import create_user, get_admin_user, create_member_user
from quiz.models import QuestionCategory, Question, Answer
import logging
from rest_framework.test import force_authenticate

User = get_user_model()

logger = logging.getLogger(__name__)

class QuizTests(APITestCase):
    def setUp(self):
        logger.debug("setUp is running")
        # QuestionCategory.objects.all().delete()  # Не удаляем!
        # logger.debug(f"Number of categories after delete: {QuestionCategory.objects.count()}")

        self.admin_user = get_admin_user()
        self.member_user = create_member_user(username="member_test", password="password123", email="member@example.com")
        # self.client.force_authenticate(user=self.member_user)  # Аутентификация не нужна в setUp, делаем в каждом тесте отдельно

        # self.category = QuestionCategory.objects.create(name="Test Category") # Не создаем категории!
        # self.question = Question.objects.create(category=self.category, text="Test Question", difficulty="easy") # Не создаем!
        # self.correct_answer = Answer.objects.create(question=self.question, text="Correct Answer", is_correct=True) # Не создаем!
        # self.incorrect_answer = Answer.objects.create(question=self.question, text="Correct Answer", is_correct=False) # Не создаем!

    def test_check_answer_correct(self):
        """Проверяем, что эндпоинт проверки ответа возвращает правильный результат для правильного ответа."""
        category = QuestionCategory.objects.create(name="Test Category")
        question = Question.objects.create(category=category, text="Test Question", difficulty="easy")
        correct_answer = Answer.objects.create(question=question, text="Correct Answer", is_correct=True)

        self.client.force_authenticate(user=self.member_user)  # Аутентификация здесь
        url = reverse('check_answer')
        data = {'question_id': question.pk, 'answer_id': correct_answer.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_correct'], True)
        self.assertEqual(response.data['question_text'], question.text)

    def test_check_answer_incorrect(self):
        """Проверяем, что эндпоинт проверки ответа возвращает правильный результат для неправильного ответа."""
        category = QuestionCategory.objects.create(name="Test Category")
        question = Question.objects.create(category=category, text="Test Question", difficulty="easy")
        incorrect_answer = Answer.objects.create(question=question, text="Incorrect Answer", is_correct=False)

        self.client.force_authenticate(user=self.member_user)  # Аутентификация здесь
        url = reverse('check_answer')
        data = {'question_id': question.pk, 'answer_id': incorrect_answer.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_correct'], False)
        self.assertEqual(response.data['question_text'], question.text)

    def test_check_answer_question_not_found(self):
        """Проверяем, что эндпоинт проверки ответа возвращает ошибку, если вопрос не найден."""
        self.client.force_authenticate(user=self.member_user)  # Аутентификация здесь
        url = reverse('check_answer')
        data = {'question_id': 999, 'answer_id': 1} # answer_id не важен, так как вопрос не найден
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_check_answer_answer_not_found(self):
        """Проверяем, что эндпоинт проверки ответа возвращает ошибку, если ответ не найден или не связан с вопросом."""
        category = QuestionCategory.objects.create(name="Test Category")
        question = Question.objects.create(category=category, text="Test Question", difficulty="easy")

        self.client.force_authenticate(user=self.member_user)  # Аутентификация здесь
        url = reverse('check_answer')
        data = {'question_id': question.pk, 'answer_id': 999}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_question_category_list_create(self):
        """Проверяем создание и получение QuestionCategory"""
        self.client.force_authenticate(user=self.admin_user) # Аутентифицируем админа!
        url = reverse('category-list-create')
        data = {'name': 'New category'}
        response_post = self.client.post(url, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), 1)
        self.assertEqual(response_get.data[0]['name'], 'New category')