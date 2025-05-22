# users/permissions.py
from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    """
    Разрешает доступ только суперпользователям.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsSelf(permissions.BasePermission):
    """
    Разрешает доступ только к своей собственной информации.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user