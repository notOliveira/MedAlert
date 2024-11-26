from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.provider import GoogleProvider
from usuarios.models import Usuario
from receitas.models import Receita
from alarmes.models import Alarme
from random import randint



class Command(BaseCommand):
    help = 'Cria médicos, pacientes, receitas, alarmes e configurações de login social no banco de dados'

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
                    password='admin',
                    user_type='ADM'
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
            for i in range(6):
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
                    alarme=alarmes[i * 2],
                    recomendacao='Tomar em jejum',
                    dose='1 comprimido',
                    medicamento=f'Medicamento {i * 2 + 1}'
                )
                Receita.objects.create(
                    medico=medicos[i],
                    paciente=pacientes[i],
                    alarme=alarmes[i * 2 + 1],
                    recomendacao='Após refeições',
                    dose='2 comprimidos',
                    medicamento=f'Medicamento {i * 2 + 2}'
                )

            # Criando aplicativo social para Google Login
            if not SocialApp.objects.filter(provider=GoogleProvider.id).exists():
                
                app = SocialApp.objects.create(
                    provider=GoogleProvider.id,
                    name="Google Login",
                    client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                    secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                    settings={
                        "scope": ["profile", "email"]
                    }
                )

                # Vincular ao site (Django contrib.sites)
                site = Site.objects.get(pk=1)  # Certifique-se de que o Site existe no banco de dados
                app.sites.add(site)

            self.stdout.write(self.style.SUCCESS('Médicos, pacientes, receitas, alarmes e login social criados com sucesso.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao criar os objetos!\n{e}'))
