from django.contrib import admin
from .models import Medicamento

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'nome', 'data', 'horario')
    list_display_links = ('id', 'usuario', 'nome')
    search_fields = ('id', 'usuario', 'nome')