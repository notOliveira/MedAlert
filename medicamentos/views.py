from rest_framework import viewsets
from medicamentos.models import Medicamento
from medicamentos.serializers import MedicamentoSerializer

class MedicamentosViewSet(viewsets.ModelViewSet):
    serializer_class = MedicamentoSerializer
    
    def get_queryset(self):
        return Medicamento.objects.filter(usuario=self.request.user)