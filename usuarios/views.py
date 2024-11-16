from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer, RegistroSerializer
from usuarios.permissions import IsOwnerOrAdmin

class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_permissions(self):
        """
            Permite acesso público para o método GET e restringe os outros métodos (POST, PUT, DELETE)
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        return Usuario.objects.all()

class UsuarioDetailView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

class RegistroUsuario(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Chama o método create do serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Cria o usuário
        user = serializer.save()

        # Retorna a resposta personalizada
        return Response(
            {"message": "Usuário criado com sucesso!"},
            status=status.HTTP_201_CREATED
        )