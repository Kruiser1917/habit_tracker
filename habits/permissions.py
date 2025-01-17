from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Позволяет редактировать объект только его владельцу.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем только просмотр публичных привычек или привычек текущего пользователя
        if request.method in ('GET', 'HEAD', 'OPTIONS') and obj.is_public:
            return True
        return obj.creator == request.user
