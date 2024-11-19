from django.contrib import admin
from usuarios.models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_medico', 'is_paciente', 'is_superuser')
    list_display_links = ('id', 'email')
    search_fields = ('id', 'email', 'username')
    list_filter = ('user_type', 'is_superuser' )
