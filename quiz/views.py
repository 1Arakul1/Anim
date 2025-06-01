# quiz\views.py
import logging
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import QuestionCategory, Question, Answer
from .serializers import QuestionCategorySerializer, QuestionSerializer, AnswerSerializer, CheckAnswerSerializer
from .paginators import QuizResultsSetPagination
from users.permissions import IsSuperUser  # Импортируйте IsSuperUser

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def check_answer(request):
    """Проверяет, является ли данный ответ правильным для данного вопроса."""

    serializer = CheckAnswerSerializer(data=request.data)
    if serializer.is_valid():
        question_id = serializer.validated_data['question_id']
        answer_id = serializer.validated_data['answer_id']

        logger.debug(f"Проверяем ответ на вопрос ID: {question_id}, ответ ID: {answer_id}")

        try:
            question = Question.objects.get(id=question_id)
            answer = Answer.objects.get(id=answer_id)

            if answer.question != question:
                logger.warning(f"Ответ ID {answer_id} не принадлежит вопросу ID {question_id}")
                return Response(
                    {"error": "Этот ответ не принадлежит данному вопросу."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Дополнительная проверка: убедитесь, что ответ связан с вопросом (для надежности)
            if answer.question_id != question_id:
                logger.error(f"Несоответствие вопроса и ответа. Answer.question_id: {answer.question_id}, question_id: {question_id}")
                return Response(
                    {"error": "Несоответствие вопроса и ответа."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    "question_text": question.text,
                    "is_correct": answer.is_correct,
                },
                status=status.HTTP_200_OK,
            )

        except Question.DoesNotExist:
            logger.warning(f"Вопрос с ID {question_id} не найден.")
            return Response({"error": "Вопрос не найден"}, status=status.HTTP_404_NOT_FOUND)
        except Answer.DoesNotExist:
            logger.warning(f"Ответ с ID {answer_id} не найден.")
            return Response({"error": "Ответ не найден"}, status=status.HTTP_404_NOT_FOUND)

    else:
        logger.warning(f"Неверные входные данные: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionCategoryListCreateAPIView(generics.ListCreateAPIView):
    """
    Создание и просмотр списка категорий вопросов.
    Только суперпользователи могут создавать категории, аутентифицированные пользователи могут просматривать.
    """
    queryset = QuestionCategory.objects.all()
    serializer_class = QuestionCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]  # Только суперпользователи могут создавать
    #  Переопределяем get-метод, чтобы пускать аутентифицированных пользователей
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsSuperUser()]  # Для остальных методов нужен IsSuperUser


class QuestionCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление конкретной категории вопросов. Требуется аутентификация."""
    queryset = QuestionCategory.objects.all()
    serializer_class = QuestionCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser] # Только суперпользователь может менять/удалять


class QuestionListCreateAPIView(generics.ListCreateAPIView):
    """Создание и просмотр списка вопросов. Требуется аутентификация."""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = QuizResultsSetPagination  # Подключаем QuizResultsSetPagination
    permission_classes = [permissions.IsAuthenticated] # Только аутентифицированный пользователь

class QuestionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление конкретного вопроса. Требуется аутентификация."""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser] # Только суперпользователь может менять/удалять


class AnswerListCreateAPIView(generics.ListCreateAPIView):
    """Создание и просмотр списка ответов. Требуется аутентификация."""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]  # Только аутентифицированный пользователь


class AnswerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление конкретного ответа. Требуется аутентификация."""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser] # Только суперпользователь может менять/удалять