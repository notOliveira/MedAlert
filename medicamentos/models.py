from django.db import models

class Medicamento(models.Model):
    nome = models.CharField(max_length=100, help_text="Nome do medicamento")
    descricao = models.TextField(null=True, blank=True, help_text="Descrição do medicamento")

    def __str__(self):
        return self.nome
