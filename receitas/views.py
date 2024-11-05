from rest_framework import viewsets
from receitas.models import Receita
from receitas.serializers import ReceitaSerializer

# Create your views here.

class ReceitaViewSet(viewsets.ModelViewSet):
    queryset = Receita.objects.all()
    serializer_class = ReceitaSerializer
