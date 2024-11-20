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

    # Método que poderá ser usado apenas por administradores
    def get_queryset(self):
        user = self.request.user
        
        # Verifica se o usuário é um superusuário
        if user.is_superuser:
            email = self.request.query_params.get('email')

            # Verifica se foi passado um email como parâmetro
            if email:
                try:
                    user_requested = Usuario.objects.get(email=email)
                    return Receita.objects.filter(paciente=user_requested)
                except Usuario.DoesNotExist:
                    return Response({"detail": "Usuário não encontrado ou não é um usuário válido."}, status=status.HTTP_400_BAD_REQUEST)
                
            # Retorna todas as receitas caso não tenha sido passado um email
            return Receita.objects.all()
            
        return Receita.objects.filter(paciente=user)

    def perform_create(self, serializer):
        # Obtém o usuário autenticado (médico)
        user = self.request.user
        
        # Verifica se o usuário é realmente um médico antes de associá-lo
        if not user.is_medico:  # Supondo que há uma flag no User model
            raise PermissionDenied("Apenas médicos podem criar receitas.")
        
        # Adiciona automaticamente o campo 'medico' com o ID do usuário
        serializer.save(medico=user)

    # Visualizar receitas do usuário logado
    @action(detail=False, methods=['get'])
    def usuario(self, request):
        user = request.user
        receitas = Receita.objects.filter(paciente=user)
        serializer = self.get_serializer(receitas, many=True)
        return Response(serializer.data)
    
    # Criar receita e alarme no mesmo endpoint
    @action(detail=False, methods=['post'], url_path='receita-alarme')
    def receita_alarme(self, request):
        user = request.user
        
        # Verificar se o usuário é um médico
        if user.user_type != 'MED':
            return PermissionDenied("Apenas médicos podem criar receitas.")
        
        data = request.data
        paciente_email = data.get('paciente')
        
        # Validar existência do paciente
        try:
            paciente = Usuario.objects.get(email=paciente_email)
        except Usuario.DoesNotExist:
            return Response({"detail": "Paciente não encontrado ou não é um usuário válido."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Criar o alarme, inserir o mesmo nome em ambos caso um esteja errado 
        alarme_data = data.pop('alarme')
        alarme_data['medicamento'] = data['medicamento']
        alarme = Alarme.objects.create(**alarme_data)

        # Criar a receita
        receita_data = {
            'medico': user,
            'paciente': paciente,
            'alarme': alarme,
            'recomendacao': data['recomendacao'],
            'dose': data['dose'],
            'medicamento': data['medicamento'],
        }
        receita = Receita.objects.create(**receita_data)

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