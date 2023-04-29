from rest_framework import permissions


class IsAuthorPermission(permissions.BasePermission):
    """Проверка пользователя на роль автора."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminPermission(permissions.BasePermission):
    """Проверка пользователя на роль Администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsModeratorPermission(permissions.BasePermission):
    """Проверка пользователя на роль Модератора."""

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_moderator or user.is_staff

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and user.is_moderator or user.is_staff


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsValidOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_superuser
            or request.user.is_moderator
        )
