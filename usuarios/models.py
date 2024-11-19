from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from usuarios.constants import SPECIALITIES, BRAZIL_STATES, USER_TYPES

class Usuario(AbstractUser):
    email = models.EmailField(unique=True, help_text="E-mail do usuário")
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