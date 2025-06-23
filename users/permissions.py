from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Проверка пользователя на статус владельца объекта."""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == "Администратор"
