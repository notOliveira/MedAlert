from django.db import models
from medicamentos.models import Medicamento

class Alarme(models.Model):
    inicio = models.DateTimeField()
    intervalo_horas = models.IntegerField(help_text="Intervalo entre doses em horas.")
    duracao_dias = models.IntegerField(help_text="Duração do tratamento em dias")
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)

    def __str__(self):
        return f"Alarme para {self.medicamento.nome}"
