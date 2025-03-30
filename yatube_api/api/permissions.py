"""Разрешения для представлений приложения API."""
from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение "Автор или на чтение".

    Разрешение, позволяющее доступ для чтения
    или доступ к собственным записям для зарегистрированных пользователей.
    """

    def has_permission(self, request, view):
        """
        Разрешение в пределах запроса.

        Разрешения в пределах запроса для методов чтения
        или любому авторизованному пользователю.
        """
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Разрешение в пределах объекта.

        Разрешения в пределах объекта, разрешают чтение
        или полное взаимодействие для автора.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
