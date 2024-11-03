from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from alarmes.models import Alarme
from alarmes.serializers import AlarmeSerializer
from usuarios.permissions import IsOwnerOrAdmin

class AlarmeViewSet(viewsets.ModelViewSet):
    queryset = Alarme.objects.all()
    serializer_class = AlarmeSerializer
    permission_classes = [IsOwnerOrAdmin]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def ativos(self, request):
        alarmes = Alarme.objects.filter(ativo=True)
        serializer = self.get_serializer(alarmes, many=True)
        return Response(serializer.data)

