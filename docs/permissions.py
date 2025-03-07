from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir que solo los propietarios de un objeto puedan editarlo.
    """

    def has_object_permission(self, request, view, obj):
        # Permitir métodos de solo lectura (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Los administradores siempre tienen permiso
        if request.user.is_staff:
            return True

        # Verificar si el usuario es el propietario del objeto
        return obj.uploaded_by == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir que solo los administradores puedan crear/editar objetos.
    """

    def has_permission(self, request, view):
        # Permitir métodos de solo lectura (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Solo permitir escritura a administradores
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Permitir métodos de solo lectura (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Solo permitir escritura a administradores
        return request.user.is_staff 