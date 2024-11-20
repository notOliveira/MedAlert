from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from usuarios.models import Usuario
from alarmes.models import Alarme
from receitas.models import Receita
from colorama import Fore, init

init(autoreset=True)

class ReceitaAPITestCase(TestCase):

    def setUp(self):
        """Configuração inicial antes de cada teste."""
        self.client = APIClient()

        # Criar médico
        self.medico = Usuario.objects.create(
            email="medico@example.com",
            username="medico01",
            user_type="MED",
            crm="123456",
            especialidade=1,
            estado="SP",
        )
        self.medico.set_password("password")
        self.medico.save()

        # Criar paciente
        self.paciente = Usuario.objects.create(
            email="paciente@example.com",
            username="paciente01",
            user_type="PAC",
            idade=30,
        )
        self.paciente.set_password("password")
        self.paciente.save()

        # Autenticação do médico
        response = self.client.post(
            reverse('login'),
            {"email": self.paciente.email, "password": "password"},
            format='json',
        )
        self.token_pac = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_pac}')

        test_name = self._testMethodName
        print(f"\n\n\n{Fore.YELLOW}==================== INÍCIO DO TESTE {test_name} ====================")

    def tearDown(self):
        """Executa após cada teste."""
        test_name = self._testMethodName
        print(f"{Fore.GREEN}==================== FINAL DO TESTE {test_name} ====================\n\n\n")

    def test_criar_receita_e_alarme(self):
        """Testa a criação de uma receita e um alarme no mesmo endpoint."""
        url = reverse('api-receitas-receita-alarme')
        data = {
            "paciente": self.paciente.email,
            "medicamento": "Paracetamol",
            "dose": "500mg",
            "recomendacao": "Tomar após as refeições",
            "alarme": {
                "inicio": "2024-11-21T08:00:00Z",
                "intervalo_horas": 8,
                "duracao_dias": 5
            },
        }

        response = self.client.post(url, data, format='json')

        print(f'\nResponse: {response.data}')

        self.assertEqual(response.status_code, 201)
        self.assertIn('receita', response.data)
        self.assertIn('alarme', response.data)

        receita = Receita.objects.get(id=response.data['receita']['id'])
        self.assertEqual(receita.medicamento, "Paracetamol")
        self.assertEqual(receita.paciente, self.paciente)
        self.assertEqual(receita.medico, self.medico)

        alarme = receita.alarme
        self.assertIsNotNone(alarme)
        self.assertEqual(alarme.medicamento, "Paracetamol")

    def test_usuario_nao_medico_criar_receita(self):
        """Testa se um usuário não médico é impedido de criar uma receita."""
        # Autenticação do paciente
        self.client.credentials()  # Remove o token atual
        response = self.client.post(
            reverse('login'),
            {"email": self.paciente.email, "password": "password"},
            format='json',
        )
        token_paciente = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_paciente}')

        url = reverse('api-receitas-receita-alarme')
        data = {
            "paciente": self.paciente.email,
            "medicamento": "Ibuprofeno",
            "dose": "200mg",
            "recomendacao": "Tomar antes de dormir",
            "alarme": {
                "inicio": "2024-11-21T20:00:00Z",
                "intervalo_horas": 12,
                "duracao_dias": 3,
            },
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertIn("Apenas médicos podem criar receitas.", str(response.data))

    def test_visualizar_receitas_do_paciente(self):
        """Testa se o paciente pode visualizar apenas suas receitas."""
        # Criar uma receita para o paciente
        alarme = Alarme.objects.create(
            inicio="2024-11-21T08:00:00Z",
            intervalo_horas=8,
            duracao_dias=7,
            medicamento="Amoxicilina",
        )
        Receita.objects.create(
            medico=self.medico,
            paciente=self.paciente,
            alarme=alarme,
            recomendacao="Tomar com água",
            dose="500mg",
            medicamento="Amoxicilina",
        )

        # Autenticação do paciente
        self.client.credentials()  # Remove o token atual
        response = self.client.post(
            reverse('login'),
            {"email": self.paciente.email, "password": "password"},
            format='json',
        )
        token_paciente = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_paciente}')

        # Verificar receitas
        url = reverse('api-receitas-usuario')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['medicamento'], "Amoxicilina")
