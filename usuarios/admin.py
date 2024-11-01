from django.contrib import admin
from usuarios.models import Medico, Paciente, Usuario

admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Usuario)