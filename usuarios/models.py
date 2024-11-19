from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from usuarios.constants import SPECIALITIES, BRAZIL_STATES, USER_TYPES

class UsuarioManager(BaseUserManager):
    """
    Gerenciador personalizado para o modelo Usuario.
    """
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("O campo 'email' é obrigatório.")
        # Validar os campos obrigatórios em cada tipo
        # Caso o user_type seja 'MED', verificar se crm e estado estão preenchidos
        if extra_fields.get('user_type') == 'MED':
            if not extra_fields.get('crm') or not extra_fields.get('estado') or not extra_fields.get('especialidade'):
                raise ValueError("Os campos 'crm', 'estado' e 'especialidade' são obrigatórios para médicos.")
        # Caso o user_type seja 'PAC', verificar se idade está preenchido
        if extra_fields.get('user_type') == 'PAC':
            if not extra_fields.get('idade'):
                raise ValueError("O campo 'idade' é obrigatório para pacientes.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superusuários devem ter is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superusuários devem ter is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class Usuario(AbstractUser):
    objects = UsuarioManager()
    email = models.EmailField(unique=True, null=False, blank=False, help_text="Endereço de e-mail")
    username = models.CharField(max_length=150, unique=True, help_text="Nome de usuário")
    user_type = models.CharField(max_length=3, choices=USER_TYPES, default='PAC', help_text="Tipo de usuário")
    idade = models.IntegerField(null=True, blank=True)
    crm = models.CharField(max_length=10, null=True, blank=True)
    estado = models.CharField(max_length=2, choices=BRAZIL_STATES, null=True, blank=True)
    especialidade = models.IntegerField(choices=SPECIALITIES, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    @property
    def is_medico(self):
        return self.user_type == 'MED'

    @property
    def is_paciente(self):
        return self.user_type == 'PAC'
    
    @property
    def is_admin(self):
        return self.user_type == 'ADM'

    def __str__(self):
        if self.is_medico:
            return f'Médico - {self.email} - CRM{self.crm}/{self.estado}'
        
        elif self.is_paciente:
            return f'Paciente - {self.email}'
        
        elif self.is_admin:
            return f'Administrador - {self.email}'