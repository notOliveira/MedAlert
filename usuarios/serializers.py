from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from usuarios.models import Usuario, Paciente, Medico
from .constants import ESPECIALIDADES, ESTADOS_BRASIL

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'username', 'first_name', 'last_name']

class MedicoSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=ESTADOS_BRASIL)
    especialidade = serializers.ChoiceField(choices=ESPECIALIDADES)

    class Meta:
        model = Medico
        fields = ['id', 'user', 'crm', 'estado', 'especialidade']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        usuario = Usuario.objects.create(**user_data)
        medico = Medico.objects.create(user=usuario, **validated_data)
        return medico

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id', 'user', 'idade']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        usuario = Usuario.objects.create(**user_data)
        paciente = Paciente.objects.create(user=usuario, **validated_data)
        return paciente

class UsuarioCriadoComSucesso(Exception):
    pass

class RegistroSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    user_type = serializers.ChoiceField(choices=['medico', 'paciente'])
    idade = serializers.IntegerField(required=False)  # Campo opcional
    crm = serializers.CharField(required=False)
    estado = serializers.CharField(required=False)
    especialidade = serializers.CharField(required=False)
    

    class Meta:
        model = Usuario
        fields = ['email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'user_type', 'idade', 'crm', 'estado', 'especialidade']
        extra_kwargs = {
            'email': {'validators': [UniqueValidator(queryset=Usuario.objects.all())]},
            'username': {'validators': [UniqueValidator(queryset=Usuario.objects.all())]},
        }

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return data
    
    def create(self, validated_data):
        # Remover a senha de confirmação antes de criar o usuário
        validated_data.pop('password2')

        # Criar o usuário
        usuario = Usuario(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        usuario.set_password(validated_data['password1'])
        usuario.save()

        user_type = validated_data.pop('user_type')

        if user_type == 'paciente':
            # Criar paciente
            idade = validated_data.pop('idade', None)  # Retirar idade do validated_data
            Paciente.objects.create(user=usuario, idade=idade)
            raise UsuarioCriadoComSucesso("Usuário criado com sucesso!")  # Levanta a exceção de sucesso

        # Se necessário, adicione aqui o código para criar médicos
        elif user_type == 'medico':
            # Aqui, você pode adicionar a lógica para criar um médico, se necessário
            crm = validated_data.pop('crm')  # Exemplo de como pegar o CRM
            estado = validated_data.pop('estado')  # Exemplo de como pegar o estado
            especialidade = validated_data.pop('especialidade')  # Exemplo de como pegar a especialidade
            Medico.objects.create(user=usuario, crm=crm, estado=estado, especialidade=especialidade)
            raise UsuarioCriadoComSucesso("Usuário criado com sucesso!")  # Levanta a exceção de sucesso

        raise serializers.ValidationError("Tipo de usuário inválido.")
