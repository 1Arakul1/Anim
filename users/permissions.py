# users/permissions.py
from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    """
    Разрешает доступ только суперпользователям.
    """
    def has_permission(self, request, view):
        """
        Проверяет, является ли пользователь суперпользователем.
        """
        return request.user and request.user.is_superuser

class IsSelf(permissions.BasePermission):
    """
    Разрешает доступ только к своей собственной информации ИЛИ если пользователь - суперпользователь.
    """
    def has_object_permission(self, request, view, obj):
        """
        Проверяет, является ли пользователь владельцем объекта (своим профилем) ИЛИ суперпользователем.
        """
        return request.user.is_superuser or obj == request.user