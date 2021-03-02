from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    message = 'У данного пользователя нет прав на изменение объекта'

    def has_object_permission(self, request, view, obj):
        if request.method in ('DELETE', 'PUT', 'POST', 'PATCH'):
            return request.user == obj.author
        return True