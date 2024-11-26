# Generated by Django 4.2.1 on 2024-11-26 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alarme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateTimeField()),
                ('intervalo_horas', models.IntegerField(help_text='Intervalo entre doses em horas.')),
                ('duracao_dias', models.IntegerField(help_text='Duração do tratamento em dias')),
                ('medicamento', models.CharField(help_text='Nome do medicamento', max_length=50)),
            ],
        ),
    ]
