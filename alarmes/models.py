from django.db import models

class Alarme(models.Model):
    inicio = models.DateTimeField()
    intervalo_horas = models.IntegerField(help_text="Intervalo entre doses em horas.")
    duracao_dias = models.IntegerField(help_text="Duração do tratamento em dias")
    medicamento = models.CharField(max_length=50, help_text="Nome do medicamento")

    def __str__(self):
        return f"Alarme para {self.medicamento.nome}"
