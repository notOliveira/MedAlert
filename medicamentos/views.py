from rest_framework import viewsets
from medicamentos.models import Medicamento
from medicamentos.serializers import MedicamentoSerializer

class MedicamentosViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer