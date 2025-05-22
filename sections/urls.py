from django.urls import path
from .views import SectionListCreateAPIView, SectionRetrieveUpdateDestroyAPIView, \
                   ContentListCreateAPIView, ContentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('sections/', SectionListCreateAPIView.as_view(), name='section-list-create'),
    path('sections/<int:pk>/', SectionRetrieveUpdateDestroyAPIView.as_view(), name='section-detail'),
    path('contents/', ContentListCreateAPIView.as_view(), name='content-list-create'),
    path('contents/<int:pk>/', ContentRetrieveUpdateDestroyAPIView.as_view(), name='content-detail'),
]