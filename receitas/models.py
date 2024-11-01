from django.db import models
from medicamentos.models import Medicamento
from usuarios.models import Usuario

class Receita(models.Model):
    medico = models.ForeignKey(Usuario, related_name='receitas_medico', on_delete=models.CASCADE)
    paciente = models.ForeignKey(Usuario, related_name='receitas_paciente', on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    dosagem = models.CharField(max_length=50) # Quantos comprimidos o paciente deve tomar
    duracao_dias = models.IntegerField() # Quantos dias o paciente deve tomar o medicamento
    recomendacoes = models.TextField(null=True, blank=True)  # Ex: "Tomar com 1L de água"
    data_prescricao = models.DateTimeField(auto_now_add=True)
    data_validade = models.DateField(null=True) # Até quando a receita é válida