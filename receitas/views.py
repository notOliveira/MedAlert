from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from receitas.models import Receita
from receitas.serializers import ReceitaSerializer

# Create your views here.

class ReceitaViewSet(viewsets.ModelViewSet):
    queryset = Receita.objects.all()
    serializer_class = ReceitaSerializer

    @action(detail=False, methods=['get'])
    def usuario(self, request):
        user = request.user
        receitas = Receita.objects.filter(paciente=user)
        serializer = self.get_serializer(receitas, many=True)
        return Response(serializer.data)