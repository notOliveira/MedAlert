# Generated by Django 4.2.1 on 2024-11-26 14:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(help_text='Endereço de e-mail', max_length=254, unique=True)),
                ('username', models.CharField(help_text='Nome de usuário', max_length=150, unique=True)),
                ('user_type', models.CharField(choices=[('ADM', 'Administrador'), ('PAC', 'Paciente'), ('MED', 'Médico')], default='PAC', help_text='Tipo de usuário', max_length=3)),
                ('idade', models.IntegerField(blank=True, null=True)),
                ('crm', models.CharField(blank=True, max_length=10, null=True)),
                ('estado', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, null=True)),
                ('especialidade', models.IntegerField(blank=True, choices=[(1, 'Acupuntura'), (2, 'Alergia e Imunologia'), (3, 'Anestesiologia'), (4, 'Angiologia'), (5, 'Cardiologia'), (6, 'Cirurgia Cardiovascular'), (7, 'Cirurgia da Mão'), (8, 'Cirurgia de Cabeça e Pescoço'), (9, 'Cirurgia do Aparelho Digestivo'), (10, 'Cirurgia Geral'), (11, 'Cirurgia Oncológica'), (12, 'Cirurgia Pediátrica'), (13, 'Cirurgia Plástica'), (14, 'Cirurgia Torácica'), (15, 'Cirurgia Vascular'), (16, 'Clínica Médica'), (17, 'Coloproctologia'), (18, 'Dermatologia'), (19, 'Endocrinologia e Metabologia'), (20, 'Endoscopia'), (21, 'Gastroenterologia'), (22, 'Genética Médica'), (23, 'Geriatria'), (24, 'Ginecologia e Obstetrícia'), (25, 'Hematologia e Hemoterapia'), (26, 'Homeopatia'), (27, 'Infectologia'), (28, 'Mastologia'), (29, 'Medicina de Emergência'), (30, 'Medicina de Família e Comunidade'), (31, 'Medicina do Trabalho'), (32, 'Medicina de Tráfego'), (33, 'Medicina Esportiva'), (34, 'Medicina Física e Reabilitação'), (35, 'Medicina Intensiva'), (36, 'Medicina Legal e Perícia Médica'), (37, 'Medicina Nuclear'), (38, 'Medicina Preventiva e Social'), (39, 'Nefrologia'), (40, 'Neurocirurgia'), (41, 'Neurologia'), (42, 'Nutrologia'), (43, 'Oftalmologia'), (44, 'Oncologia Clínica'), (45, 'Ortopedia e Traumatologia'), (46, 'Otorrinolaringologia'), (47, 'Patologia'), (48, 'Patologia Clínica/ Medicina Laboratorial'), (49, 'Pediatria'), (50, 'Pneumologia'), (51, 'Psiquiatria'), (52, 'Radiologia e Diagnóstico por Imagem'), (53, 'Radioterapia'), (54, 'Reumatologia'), (55, 'Urologia')], null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
