from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from usuarios.models import Usuario
from receitas.models import Receita
from colorama import Fore, init

init(autoreset=True)


class ReceitaMedicoAPITestCase(TestCase):

    def setUp(self):
        """Configuração inicial para cada teste."""
        self.client = APIClient()

        # Criar médico
        self.medico = Usuario.objects.create_user(
            email="medico@example.com",
            username="medico01",
            user_type="MED",
            crm="123456",
            especialidade=1,
            estado="SP",
            password="password",
        )

        # Criar paciente
        self.paciente = Usuario.objects.create_user(
            email="paciente@example.com",
            username="paciente01",
            user_type="PAC",
            idade=30,
            password="password",
        )

        # Autenticar o médico
        response = self.client.post(
            reverse("login"),
            {"email": self.medico.email, "password": "password"},
            format="json",
        )
        self.token_medico = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token_medico}")

        test_name = self._testMethodName
        print(f"\n\n{Fore.YELLOW}==================== INÍCIO DO TESTE {test_name} ====================\n")

    def tearDown(self):
        """Executa após cada teste."""
        test_name = self._testMethodName
        print(f"\n\n{Fore.GREEN}==================== FINAL DO TESTE {test_name} ====================\n\n")

    def criar_receita_e_alarme(self):
        """Função utilitária para criar uma receita com alarme."""
        url = reverse("api-receitas-receita-alarme")
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
        response = self.client.post(url, data, format="json")

        print(f"\nResponse: {response.data}")
        return response

    def test_criar_receita_e_alarme(self):
        """Testa a criação de uma receita com alarme por um médico."""
        response = self.criar_receita_e_alarme()
        self.assertEqual(response.status_code, 201)
        self.assertIn("receita", response.data)
        self.assertIn("alarme", response.data)

        receita = Receita.objects.get(id=response.data["receita"]["id"])

        print(f"\nReceita: {receita}")
        self.assertEqual(receita.medicamento, "Paracetamol")
        self.assertEqual(receita.paciente, self.paciente)
        self.assertEqual(receita.medico, self.medico)

    def test_visualizar_receitas_como_medico(self):
        """Testa se o médico consegue visualizar receitas que prescreveu."""
        # Criar receita
        response = self.criar_receita_e_alarme()
        self.assertEqual(response.status_code, 201)

        # Listar receitas prescritas
        url = reverse("api-receitas-preescritas")
        response = self.client.get(url, format="json")

        print(f"\nReceitas prescritas: {response.data}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        receita = response.data[0]
        self.assertEqual(receita["medicamento"], "Paracetamol")
        self.assertEqual(receita["paciente"]["email"], self.paciente.email)
        self.assertEqual(receita["medico"]["email"], self.medico.email)

    def test_editar_receita_como_medico(self):
        """Testa se o médico consegue editar uma receita que prescreveu."""
        # Criar receita
        response = self.criar_receita_e_alarme()
        self.assertEqual(response.status_code, 201)
        receita_id = response.data["receita"]["id"]

        receita = Receita.objects.get(id=receita_id)
        print(f"\nReceita: {receita}")

        # Atualizar a receita
        url = reverse("api-receitas-detail", args=[receita_id])
        data = {
            "recomendacao": "Tomar com leite para evitar dor de estômago",
            "dose": "300mg",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, 200)

        receita.refresh_from_db()
        print(f"\nNova receita: {receita}")
        self.assertEqual(receita.recomendacao, "Tomar com leite para evitar dor de estômago")
        self.assertEqual(receita.dose, "300mg")
