from django.core.management.base import BaseCommand
from django.utils import timezone
from usuarios.models import Usuario
from receitas.models import Receita
from alarmes.models import Alarme
from random import randint


class Command(BaseCommand):
    help = 'Cria médicos, pacientes, receitas e alarmes de exemplo no banco de dados'

    def handle(self, *args, **options):
        try:
            # Criando superusuário
            admin_email = 'admin@medalert.com'
            if not Usuario.objects.filter(email=admin_email).exists():
                Usuario.objects.create_superuser(
                    email=admin_email,
                    username='admin',
                    first_name='Admin',
                    last_name='User',
                    password='admin'
                )

            # Criando médicos
            medicos = []
            for i in range(1, 4):
                medico = Usuario.objects.create_user(
                    email=f'medico{i}@example.com',
                    username=f'medico{i}',
                    first_name=f'Médico {i}',
                    last_name='Sobrenome',
                    password='senhaSegura123',
                    user_type='MED',
                    crm=f'{1000+i}',
                    estado='SP',
                    especialidade=randint(1, 55)
                )
                medicos.append(medico)

            # Criando pacientes
            pacientes = []
            for i in range(1, 4):
                paciente = Usuario.objects.create_user(
                    email=f'paciente{i}@example.com',
                    username=f'paciente{i}',
                    first_name=f'Paciente {i}',
                    last_name='Sobrenome',
                    password='senhaSegura123',
                    user_type='PAC',
                    idade=randint(1, 80)
                )
                pacientes.append(paciente)

            # Criando alarmes
            alarmes = []
            for i in range(3):
                alarme = Alarme.objects.create(
                    inicio=timezone.now(),
                    intervalo_horas=6,
                    duracao_dias=randint(1, 7),
                    medicamento=f'Medicamento {i+1}'
                )
                alarmes.append(alarme)

            # Criando receitas
            for i in range(3):
                Receita.objects.create(
                    medico=medicos[i],
                    paciente=pacientes[i],
                    alarme=alarmes[i],
                    recomendacao='Tomar em jejum',
                    dose='1 comprimido',
                    medicamento=f'Medicamento {i+1}'
                )

            self.stdout.write(self.style.SUCCESS('Médicos, pacientes, receitas e alarmes criados com sucesso.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao criar os objetos!\n{e}'))