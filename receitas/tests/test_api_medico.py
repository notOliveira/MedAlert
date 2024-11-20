from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from usuarios.models import Usuario
from alarmes.models import Alarme
from receitas.models import Receita
from colorama import Fore, init

init(autoreset=True)

class ReceitaMedicoAPITestCase(TestCase):

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
            {"email": self.medico.email, "password": "password"},
            format='json',
        )
        self.token_medico = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_medico}')

        test_name = self._testMethodName

        print(f"\n\n{Fore.YELLOW}==================== INÍCIO DO TESTE {test_name} ====================\n")

    def tearDown(self):
        """Executa após cada teste."""
        test_name = self._testMethodName
        print(f"\n\n{Fore.GREEN}==================== FINAL DO TESTE {test_name} ====================\n\n")

    # Teste no endpoint /receitas/receita-alarme/
    def test_criar_receita_e_alarme(self):
        """Testa a criação de uma receita e um alarme como médico."""
        url = reverse('api-receitas-receita-alarme')
        data = {
            "paciente": self.paciente.email,
            "medicamento": "Paracetamol",
            "dose": "500mg",
            "recomendacao": "Tomar após as refeições",
            "alarme": {
                "inicio": "2024-11-21T08:00:00Z",
                "intervalo_horas": 8,
                "duracao_dias": 5,
                "medicamento": "Paracetamol",
            },
        }

        response = self.client.post(url, data, format='json')

        print(f'\nResponse: {response.data}')

        self.assertEqual(response.status_code, 201)
        self.assertIn('receita', response.data)
        self.assertIn('alarme', response.data)

        receita = Receita.objects.get(id=response.data['receita']['id'])

        print(f'\nReceita: {receita}')
        
        self.assertEqual(receita.medicamento, "Paracetamol")
        self.assertEqual(receita.paciente, self.paciente)
        self.assertEqual(receita.medico, self.medico)

        alarme = receita.alarme
        self.assertIsNotNone(alarme)
        self.assertEqual(alarme.medicamento, "Paracetamol")

    # Testes no endpoint /receitas/
    def test_visualizar_receitas_como_medico(self):
        """Testa se o médico consegue visualizar as receitas que prescreveu."""
        # Criar uma receita para o paciente
        
        url = reverse('api-receitas-receita-alarme')
        data = {
            "paciente": self.paciente.email,
            "medicamento": "Paracetamol",
            "dose": "500mg",
            "recomendacao": "Tomar após as refeições",
            "alarme": {
                "inicio": "2024-11-21T08:00:00Z",
                "intervalo_horas": 8,
                "duracao_dias": 5,
                "medicamento": "Paracetamol",
            },
        }

        response = self.client.post(url, data, format='json')

        print(f'\nResponse: {response.data}')

        self.assertEqual(response.status_code, 201)

        # Listar receitas
        url = reverse('api-receitas-preescritas')
        response = self.client.get(url, format='json')

        print(f"\nReceitas prescritas: {response.data}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['medicamento'], "Paracetamol")
        self.assertEqual(response.data[0]['paciente']['email'], self.paciente.email)
        self.assertEqual(response.data[0]['medico']['email'], self.medico.email)
        self.assertEqual(response.data[0]['recomendacao'], "Tomar após as refeições")

    def test_editar_receita_como_medico(self):
        """Testa se o médico consegue editar uma receita."""
        # Criar uma receita
        url = reverse('api-receitas-receita-alarme')
        data = {
            "paciente": self.paciente.email,
            "medicamento": "Paracetamol",
            "dose": "500mg",
            "recomendacao": "Tomar após as refeições",
            "alarme": {
                "inicio": "2024-11-21T08:00:00Z",
                "intervalo_horas": 8,
                "duracao_dias": 5,
                "medicamento": "Paracetamol",
            },
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('receita', response.data)
        self.assertIn('alarme', response.data)

        receita = Receita.objects.get(id=response.data['receita']['id'])

        print(f'\nReceita: {receita}')

        # Atualizar a receita
        url = reverse('api-receitas-detail', args=[receita.id])
        data = {
            "recomendacao": "Tomar com leite para evitar dor de estômago",
            "dose": "300mg",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        nova_receta = Receita.objects.get(id=receita.id)

        print(f'\nNova receita: {nova_receta}')

        receita.refresh_from_db()
        self.assertEqual(receita.recomendacao, "Tomar com leite para evitar dor de estômago")
        self.assertEqual(receita.dose, "300mg")
