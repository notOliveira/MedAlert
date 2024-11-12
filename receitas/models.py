from django.db import models
from usuarios.models import Usuario
from alarmes.models import Alarme

class Receita(models.Model):
    medico = models.ForeignKey(Usuario, on_delete=models.CASCADE, help_text="Médico que irá prescrever a receita", related_name='medico_receitas')
    paciente = models.ForeignKey(Usuario, on_delete=models.CASCADE, help_text="Paciente que irá receber a receita", related_name='paciente_receitas')
    alarme = models.OneToOneField(Alarme, on_delete=models.CASCADE, null=True, blank=True, help_text="Alarme para lembrar o paciente de tomar o medicamento")
    recomendacao = models.TextField(null=True, blank=True, help_text="Recomendações livres e adicionais sobre os medicamentos que foram receitados")
    dose = models.CharField(max_length=50, help_text="Dosagem (Ex: 20mg / 1 comprimido / 20 gotas)")
    medicamento = models.CharField(max_length=50, help_text="Nome do medicamento")

    def __str__(self):
        return f"{self.medico} - {self.paciente} - {self.medicamento}"