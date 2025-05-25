#sections\views.py
from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Section, Content
from .serializers import SectionSerializer, ContentSerializer
from .permissions import IsOwner, IsSectionOwner
from .paginators import StandardResultsSetPagination
from django.core.exceptions import PermissionDenied

class SectionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Этот метод переопределяет queryset, чтобы возвращать только разделы,
        принадлежащие текущему пользователю.
        """
        return Section.objects.filter(owner=self.request.user)

class SectionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

class ContentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated, IsSectionOwner]  # Тут было только IsAuthenticated!
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        # Проверяем, что пользователь имеет право создавать контент в этом разделе
        section = serializer.validated_data['section']
        if section.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("Вы не можете добавлять контент в чужой раздел")
        serializer.save()

class ContentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated, IsSectionOwner]
