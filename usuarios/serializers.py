from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, force_str, smart_bytes, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from usuarios.models import Usuario
from usuarios.constants import USER_TYPES, SPECIALITIES, BRAZIL_STATES

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'user_type']

class UsuarioReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name']

class RegistroSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    user_type = serializers.ChoiceField(choices=USER_TYPES)
    idade = serializers.IntegerField(required=False)
    crm = serializers.CharField(required=False)
    estado = serializers.ChoiceField(choices=BRAZIL_STATES, required=False)
    especialidade = serializers.ChoiceField(choices=SPECIALITIES, required=False)

    class Meta:
        model = Usuario
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'user_type', 'idade', 'crm', 'estado', 'especialidade']
        extra_kwargs = {
            'email': {'validators': [UniqueValidator(queryset=Usuario.objects.all())]},
            'username': {'validators': [UniqueValidator(queryset=Usuario.objects.all())]},
        }

    def validate(self, data):
        # Validar senhas
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("As senhas não coincidem.")
        
        # Validações de acordo com o tipo de usuário
        if data['user_type'] == 'MED':
            if not all([data.get('crm'), data.get('estado'), data.get('especialidade')]):
                raise serializers.ValidationError("CRM, estado e especialidade são obrigatórios para médicos.")
        elif data['user_type'] == 'PAC' and not data.get('idade'):
            raise serializers.ValidationError("A idade é obrigatória para pacientes.")
        
        return data

    def create(self, validated_data):
        # Remover password1 e password2 do validated_data
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        # Criar o usuário com os dados básicos
        usuario = Usuario(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            user_type=validated_data.get('user_type', 'PAC')
        )
        usuario.set_password(password)
        usuario.save()

        # Verificar o tipo de usuário e criar campos adicionais se necessário
        if usuario.user_type == 'PAC':
            usuario.idade = validated_data.get('idade')
        elif usuario.user_type == 'MED':
            usuario.crm = validated_data.get('crm')
            usuario.estado = validated_data.get('estado')
            usuario.especialidade = validated_data.get('especialidade')

        usuario.save()
        return usuario
    
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=5)

    class Meta:
        fields = ['email']

    def validate(self, data):
        try:
            email = data.get('email')
            if not Usuario.objects.filter(email=email).exists():
                raise serializers.ValidationError("Não existe usuário com o email fornecido.")

            # Obter o usuário associado ao email
            user_email = Usuario.objects.get(email=email)

            # Gerar token de redefinição de senha
            token = PasswordResetTokenGenerator().make_token(user_email)

            # Parâmetros para o email
            email_template_name = "usuarios/reset_password.txt"
            subject = 'Redefinir sua senha - MedAlert'
            parameters = {
                'name': user_email.first_name,
                'domain': self.context['request'].get_host(),
                'site_name': 'MedAlert',
                'uid': urlsafe_base64_encode(force_bytes(user_email.pk)),
                'token': token,
                'protocol': self.context['request'].scheme
            }

            # Renderizar o conteúdo do email
            email_content = render_to_string(email_template_name, parameters)

            # Enviar o email
            send_mail(
                subject=subject,
                message=email_content,
                from_email=None,  # Substitua por um email válido se necessário
                recipient_list=[user_email.email],
                fail_silently=False
            )

            return data

        except Exception as e:
            # Retornar o erro como uma mensagem de validação
            raise serializers.ValidationError("Usuário não encontrado com o email fornecido.")