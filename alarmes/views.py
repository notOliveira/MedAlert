from rest_framework import viewsets
from alarmes.models import Alarme
from alarmes.serializers import AlarmeSerializer

class AlarmeViewSet(viewsets.ModelViewSet):
    queryset = Alarme.objects.all()
    serializer_class = AlarmeSerializer
