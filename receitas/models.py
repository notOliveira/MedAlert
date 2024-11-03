from django.db import models
from medicamentos.models import Medicamento
from usuarios.models import Medico, Paciente
from alarmes.models import Alarme

class Receita(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, help_text="Médico que irá preescrever a receita")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, help_text="Paciente que irá receber a receita")
    recomendacao = models.TextField(null=True, blank=True, help_text="Recomendações livres e adicionais sobre os medicamentos que foram receitados") # Recomendação do médico
    dose = models.CharField(max_length=50, help_text="Dosagem (Ex: 20mg / 1 comprimido / 20 gotas)")
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, help_text="Medicamento que foi receitado")
    alarme = models.OneToOneField(Alarme, on_delete=models.CASCADE, null=True, blank=True, help_text="Alarme para lembrar o paciente de tomar o medicamento")