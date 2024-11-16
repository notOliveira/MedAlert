from rest_framework import serializers
from alarmes.models import Alarme

class AlarmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarme
        fields = '__all__'

class AlarmeReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarme
        fields = ['id', 'inicio', 'intervalo_horas', 'duracao_dias', 'medicamento']