from django.urls import path
from .views import QuestionCategoryListCreateAPIView, QuestionCategoryRetrieveUpdateDestroyAPIView, \
                   QuestionListCreateAPIView, QuestionRetrieveUpdateDestroyAPIView, \
                   AnswerListCreateAPIView, AnswerRetrieveUpdateDestroyAPIView, check_answer


urlpatterns = [
    path('categories/', QuestionCategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', QuestionCategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
    path('questions/', QuestionListCreateAPIView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionRetrieveUpdateDestroyAPIView.as_view(), name='question-detail'),
    path('answers/', AnswerListCreateAPIView.as_view(), name='answer-list-create'),
    path('answers/<int:pk>/', AnswerRetrieveUpdateDestroyAPIView.as_view(), name='answer-detail'),
    path('check_answer/', check_answer, name='check_answer'), # Добавляем URL для проверки ответа
]