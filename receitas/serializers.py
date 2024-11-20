from rest_framework import serializers
from receitas.models import Receita
from alarmes.serializers import AlarmeSerializer
from usuarios.serializers import UsuarioReceitaSerializer

class ReceitaSerializer(serializers.ModelSerializer):
    alarme = AlarmeSerializer(read_only=True)
    medico = UsuarioReceitaSerializer(read_only=True)
    paciente = UsuarioReceitaSerializer(read_only=True)

    class Meta:
        model = Receita
        fields = '__all__'