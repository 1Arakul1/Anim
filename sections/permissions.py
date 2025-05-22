from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Разрешает доступ только владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsSectionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем суперпользователю или владельцу раздела
        return request.user.is_superuser or obj.section.owner == request.user