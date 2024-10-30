from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from usuarios.models import Usuario, Paciente, Medico
from usuarios.serializers import UsuarioSerializer, PacienteSerializer, MedicoSerializer, RegistroSerializer, UsuarioCriadoComSucesso
from .permissions import IsOwnerOrAdmin

class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_permissions(self):
        # Permite acesso público para o método GET e restringe os outros métodos
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

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [IsOwnerOrAdmin]

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    permission_classes = [IsOwnerOrAdmin]

class RegistroUsuario(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Chama o método create do serializer
            serializer.save()
        except Exception as e:  # Captura qualquer exceção gerada
            if isinstance(e, UsuarioCriadoComSucesso):
                return Response({'detail': str(e)}, status=status.HTTP_201_CREATED)
            raise  # Relevanta outras exceções

        return Response({'detail': 'Usuário criado com sucesso!'}, status=status.HTTP_201_CREATED)
