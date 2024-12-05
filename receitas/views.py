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

        if user.is_superuser:
            email = self.request.query_params.get('email')
            if email:
                try:
                    user_requested = Usuario.objects.get(email=email)
                    return Receita.objects.filter(paciente=user_requested)
                except Usuario.DoesNotExist:
                    return Receita.objects.none()
            return Receita.objects.all()
        
        if user.is_medico:
            # Médicos podem ver receitas que prescreveram e receitas prescritas para eles
            return Receita.objects.filter(medico=user) | Receita.objects.filter(paciente=user)

        # Pacientes podem ver apenas receitas que foram prescritas para eles
        return Receita.objects.filter(paciente=user)

    def perform_create(self, serializer):
        user = self.request.user

        if not user.is_medico:
            raise PermissionDenied("Apenas médicos podem criar receitas.")

        serializer.save(medico=user)

    def perform_update(self, serializer):
        user = self.request.user
        receita = self.get_object()

        if user.is_medico and receita.medico == user:
            # Médico pode atualizar receitas que prescreveu
            serializer.save()
        else:
            raise PermissionDenied("Você não tem permissão para editar esta receita.")

    @action(detail=False, methods=['get'], url_path='usuario')
    def usuario(self, request):
        user = request.user
        receitas = Receita.objects.filter(paciente=user)
        serializer = self.get_serializer(receitas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='receita-alarme')
    def receita_alarme(self, request):
        user = self.request.user

        if not user.is_medico:
            return Response({"detail": "Apenas médicos podem criar receitas."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        paciente_email = data.get('paciente')

        try:
            paciente = Usuario.objects.get(email=paciente_email)
        except Usuario.DoesNotExist:
            return Response({"detail": "Paciente não encontrado ou não é um usuário válido."}, status=status.HTTP_400_BAD_REQUEST)

        for campo in ['paciente', 'medicamento', 'dose', 'alarme', 'recomendacao']:
            if campo not in data:
                return Response({"detail": f"Campo ausente ou inválido: {campo}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            alarme_data = data['alarme']
            for campo in ['inicio', 'intervalo_horas', 'duracao_dias', 'medicamento']:
                if campo not in alarme_data:
                    return Response({"detail": f"Campo ausente ou inválido no alarme: {campo}"}, status=status.HTTP_400_BAD_REQUEST)

            alarme_data['medicamento'] = data['medicamento']
            alarme = Alarme.objects.create(**alarme_data)
        except Exception as e:
            return Response({"detail": f"Erro ao criar alarme: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

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
        except Exception as e:
            return Response({"detail": f"Erro ao criar receita: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "receita": {
                    "id": receita.id,
                    "medico": receita.medico.id,
                    "paciente": {
                        "first_name": receita.paciente.first_name
                    },
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

    @action(detail=False, methods=['get'], url_path='preescritas')
    def preescritas(self, request):
        user = self.request.user

        if not user.is_medico:
            return Response({"detail": "Apenas médicos podem acessar receitas prescritas."}, status=status.HTTP_403_FORBIDDEN)

        receitas = Receita.objects.filter(medico=user)
        serializer = self.get_serializer(receitas, many=True)
        return Response(serializer.data)
