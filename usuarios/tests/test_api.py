from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from usuarios.models import Usuario

class UsuarioAPITest(TestCase):
    def setUp(self):
        # Criando usuários para os testes
        self.medico = Usuario.objects.create_user(
            email="medico@example.com",
            username="medico01",
            password="securepassword",
            user_type="MED",
            crm="123456",
            estado="SP",
            especialidade=1
        )
        self.client = APIClient()

    def test_registro_paciente(self):
        """Testa a criação de um novo paciente via API"""

        url = reverse('registro')
        data = {
            "email": "novo_paciente@example.com",
            "username": "paciente01",
            "password1": "password",
            "password2": "password",
            "user_type": "PAC",
            "idade": 25
        }

        response = self.client.post(url, data, format='json')
        print(f'\nResponse: {response.data}')

        # Verificando se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 201)

        # Verificando se o usuário foi realmente criado
        usuario = Usuario.objects.get(email="novo_paciente@example.com")
        self.assertEqual(usuario.email, "novo_paciente@example.com")
    
    def test_registro_medico(self):
        """Testa a criação de um novo médico via API"""

        url = reverse('registro')
        data = {
            "email": "novo_medico@example.com",
            "username": "medico02",
            "password1": "password",
            "password2": "password",
            "user_type": "MED",
            "crm": "654321",
            "estado": "RJ",
            "especialidade": 2
        }

        response = self.client.post(url, data, format='json')
        print(f'\nResponse: {response.data}')

        # Verificando se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 201)

        # Verificando se o médico foi realmente criado
        medico = Usuario.objects.get(email="novo_medico@example.com")
        self.assertEqual(medico.email, "novo_medico@example.com")

    def test_usuario_sem_email(self):
        """Testa se a criação de usuário sem email falha"""

        url = reverse('registro')
        data = {
            "email": "",
            "username": "paciente_invalido",
            "password1": "password",
            "password2": "password",
            "user_type": "PAC",
        }

        response = self.client.post(url, data, format='json')
        print(f'\nResponse: {response.data}')

        # Espera-se que o campo email seja obrigatório e gere um erro
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)

    def test_login_usuario(self):
        """Testa o login de usuário via API"""

        url = reverse('login')
        data = {
            "email": "medico@example.com",
            "password": "securepassword"
        }

        response = self.client.post(url, data, format='json')
        print(f'\nResponse: {response.data}')

        # Verificando se o login foi bem-sucedido
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)