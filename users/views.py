# users/views.py
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .permissions import IsSuperUser, IsSelf
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class UserList(generics.ListCreateAPIView):
    """
    API view для просмотра списка пользователей и создания новых пользователей.
    Доступно только для суперпользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]  # Только суперпользователи могут просматривать и создавать

    def perform_create(self, serializer):
        """
        Сохраняет нового пользователя.
        """
        serializer.save()

    def get(self, request, *args, **kwargs):
        """
        Логирует заголовок Authorization для отладки.
        """
        logger.debug(f"Authorization header: {request.META.get('HTTP_AUTHORIZATION')}")
        return super().get(request, *args, **kwargs)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view для просмотра, обновления и удаления информации о конкретном пользователе.
    Доступно только самому пользователю ИЛИ суперпользователю.
    """
    serializer_class = UserSerializer
    # IsSelf проверяет, что пользователь запрашивает свой собственный профиль,
    # ИЛИ является суперпользователем.
    permission_classes = [IsSelf]  # Разрешения определяются в IsSelf

    def get_object(self):
        """
        Возвращает объект пользователя по primary key (pk).
        Если пользователь не является суперпользователем и не пытается получить
        доступ к своему профилю, возвращает 404 ошибку.
        """
        pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)

        #  Добавляем проверку здесь:
        if not self.request.user.is_superuser and user != self.request.user:
             #  Если пользователь пытается получить чужой профиль и он не суперпользователь,
             #  возвращаем 404.  Это важный момент для security.
            raise PermissionDenied() # Или Http404, если не хотите использовать PermissionDenied

        return user

    def perform_update(self, serializer):
        """
        Сохраняет обновленную информацию о пользователе.
        """
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Удаляет пользователя.
        Так как permission_classes = [IsSelf], проверка прав доступа происходит автоматически,
        и здесь нет необходимости дублировать проверку вручную.
        """
        instance = self.get_object()  # Получаем объект пользователя для удаления
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# users/serializers.py и users/permissions.py без изменений