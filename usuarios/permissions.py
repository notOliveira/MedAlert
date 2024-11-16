from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permite que apenas o usuário que é o dono do objeto ou um admin possa editar ou deletar o objeto.
    """

    def has_object_permission(self, request, view, obj):
        # Apenas admins têm acesso total
        if request.user.is_staff:
            return True
        # Permite que o próprio usuário faça alterações em seu perfil

        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return obj == request.user