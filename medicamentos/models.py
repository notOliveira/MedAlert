from django.db import models

class Medicamento(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, help_text="Nome do medicamento")
    dosagem = models.CharField(max_length=100, help_text="Dosagem do medicamento")
    unidade = models.CharField(max_length=100, help_text="Unidade de dosagens do medicamento")
    frequencia = models.CharField(max_length=100, help_text="Frequência de uso do medicamento")
    data = models.DateField(help_text="Data de início do uso do medicamento")
    alarme = models.BooleanField(default=False, help_text="Ativar alarme para o medicamento")
    imagem = models.ImageField(upload_to='medicamentos/', blank=True, null=True, help_text="Imagem do medicamento")

    def __str__(self):
        return f"{self.usuario.username} - {self.nome}"
