from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from usuarios.models import Usuario
from alarmes.models import Alarme
from receitas.models import Receita
from receitas.serializers import ReceitaSerializer

class ReceitaViewSet(viewsets.ModelViewSet):
    queryset = Receita.objects.all()
    serializer_class = ReceitaSerializer

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
            return Response({"detail": "Apenas médicos podem criar receitas."}, status=status.HTTP_403_FORBIDDEN)
        
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