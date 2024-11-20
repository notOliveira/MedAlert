from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from usuarios.models import Usuario
from alarmes.models import Alarme
from receitas.models import Receita
from receitas.serializers import ReceitaSerializer

class ReceitaViewSet(viewsets.ModelViewSet):
    serializer_class = ReceitaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Administradores têm acesso a todas as receitas ou podem filtrar por email
        if user.is_superuser:
            email = self.request.query_params.get('email')
            if email:
                try:
                    user_requested = Usuario.objects.get(email=email)
                    return Receita.objects.filter(paciente=user_requested)
                except Usuario.DoesNotExist:
                    return Receita.objects.none()
            return Receita.objects.all()

        # Usuário logado como paciente visualiza suas receitas
        return Receita.objects.filter(paciente=user)

    def perform_create(self, serializer):
        user = self.request.user

        # Apenas médicos podem criar receitas
        if not user.is_medico:
            raise PermissionDenied("Apenas médicos podem criar receitas.")
        
        serializer.save(medico=user)

    # Visualizar receitas do usuário logado como paciente
    @action(detail=False, methods=['get'], url_path='user')
    def usuario(self, request):
        user = request.user
        receitas = Receita.objects.filter(paciente=user)

        # Adiciona validação se o usuário não tiver receitas
        if not receitas.exists():
            return Response({"detail": "Nenhuma receita encontrada para o usuário."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(receitas, many=True)
        return Response(serializer.data)

    # Criar receita e alarme no mesmo endpoint
    @action(detail=False, methods=['post'], url_path='receita-alarme')
    def receita_alarme(self, request):
        user = request.user

        # Apenas médicos podem criar receitas
        if user.user_type != 'MED':
            return PermissionDenied("Apenas médicos podem criar receitas.")

        data = request.data
        paciente_email = data.get('paciente')

        # Validar existência do paciente
        try:
            paciente = Usuario.objects.get(email=paciente_email)
        except Usuario.DoesNotExist:
            return Response({"detail": "Paciente não encontrado ou não é um usuário válido."}, status=status.HTTP_400_BAD_REQUEST)

        # Criar o alarme
        try:
            alarme_data = data.pop('alarme')
            alarme_data['medicamento'] = data['medicamento']
            alarme = Alarme.objects.create(**alarme_data)
        except KeyError as e:
            return Response({"detail": f"Campo ausente ou inválido: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Criar a receita
        try:
            receita_data = {
                'medico': user,
                'paciente': paciente,
                'alarme': alarme,
                'recomendacao': data.get('recomendacao', ''),
                'dose': data['dose'],
                'medicamento': data['medicamento'],
            }
            receita = Receita.objects.create(**receita_data)
        except KeyError as e:
            return Response({"detail": f"Campo ausente ou inválido: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Retornar os dados criados
        return Response(
            {
                "receita": {
                    "id": receita.id,
                    "medico": receita.medico.id,
                    "paciente": receita.paciente.email,
                    "recomendacao": receita.recomendacao,
                    "dose": receita.dose,
                    "medicamento": receita.medicamento,
                },
                "alarme": {
                    "id": alarme.id,
                    "inicio": alarme.inicio,
                    "intervalo_horas": alarme.intervalo_horas,
                    "duracao_dias": alarme.duracao_dias,
                    "medicamento": alarme.medicamento,
                },
            },
            status=status.HTTP_201_CREATED,
        )

    # Action para visualizar receitas prescritas por um médico específico
    @action(detail=False, methods=['get'], url_path='preescritos')
    def preescritos(self, request):
        user = self.request.user

        # Apenas médicos podem acessar essa action
        if not user.is_medico:
            return Response({"detail": "Apenas médicos podem acessar receitas prescritas."}, status=status.HTTP_403_FORBIDDEN)
        
        # Retornar receitas prescritas pelo médico logado
        receitas = Receita.objects.filter(medico=user)
        if not receitas.exists():
            return Response({"detail": "Nenhuma receita encontrada para o médico logado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(receitas, many=True)
        return Response(serializer.data)
