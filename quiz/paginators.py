from rest_framework.pagination import PageNumberPagination

class QuizResultsSetPagination(PageNumberPagination):
    page_size = 5 # 5 вопросов на странице
    page_size_query_param = 'page_size'
    max_page_size = 100