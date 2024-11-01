from django.db import models
from medicamentos.models import Medicamento
from usuarios.models import Medico, Paciente
from alarmes.models import Alarme

class Receita(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE) # Médico que receitou
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE) # Paciente que irá fazer uso dos medicammentos
    recomendacao = models.TextField(null=True, blank=True) # Recomendação do médico
    dose = models.CharField(max_length=50) # Quantidade de medicamento a ser tomado (ex: 1 comprimido)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE) # Medicamento que será tomado
    alarme = models.OneToOneField(Alarme, on_delete=models.CASCADE, null=True, blank=True) # Alarme para lembrar o paciente de tomar o medicamento