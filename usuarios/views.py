from rest_framework import viewsets, status, generics
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer, RegistroSerializer
from usuarios.permissions import IsOwnerOrAdmin

class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    permission_classes = [IsOwnerOrAdmin]

    # Apenas superusuários podem listar todos os usuários
    # Usuários comuns só podem listar a si mesmos
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            email = self.request.query_params.get('email')
            if email:
                return Usuario.objects.filter(email=email)
            return Usuario.objects.all()
        return Usuario.objects.filter(id=user.id)
    
    # Médicos podem buscar pacientes pelo email
    @action(detail=False, methods=['get'], url_path='busca-paciente-email')
    def busca_paciente_email(self, request):
        user = self.request.user

        # Permitir apenas médicos
        if not user.is_medico:
            raise PermissionDenied("Você não tem permissão para acessar esse recurso.")

        # Buscar paciente pelo email
        email = self.request.query_params.get('email')
        if not email:
            return Response(
                {"detail": "O parâmetro 'email' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            paciente = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            raise NotFound("Paciente não encontrado com o email fornecido.")

        serializer = self.get_serializer(paciente)
        return Response(serializer.data)

# class UsuarioDetailView(generics.RetrieveAPIView):
#     queryset = Usuario.objects.all()
#     serializer_class = UsuarioSerializer
#     lookup_field = 'id'
#     # permission_classes = [IsOwnerOrAdmin]

#     def get_queryset(self):
#         user_request = self.request.user
#         print(user_request)

#         if not user_request.is_medico:
#             raise PermissionDenied("Você não tem permissão para acessar esse recurso.")
        
#         email = self.request.query_params.get('email')

#         user_email = Usuario.objects.filter(email=email)
        
#         return self.queryset.filter(email=user_email)

class RegistroUsuario(generics.CreateAPIView):
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