from django.test import TestCase
from django.urls import reverse
from usuarios.models import Usuario
from colorama import Fore, init

init(autoreset=True)

class UsuarioAPITestCase(TestCase):

    def setUp(self):
        """Executa antes de cada teste."""
        test_name = self._testMethodName
        print(f"\n\n\n{Fore.YELLOW}==================== INÍCIO DO TESTE: {test_name} ====================")

    def tearDown(self):
        """Executa após cada teste."""
        test_name = self._testMethodName
        print(f"\n{Fore.GREEN}==================== FINAL DO TESTE: {test_name} ====================\n\n\n")
        
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
        

    def test_registro_paciente_sem_idade(self):
        """Testa a criação de paciente sem o campo idade."""
        url = reverse('registro')
        data = {
            "email": "paciente_sem_idade@example.com",
            "username": "paciente01",
            "password1": "password",
            "password2": "password",
            "user_type": "PAC",
        }

        response = self.client.post(url, data, format='json')
        print(f'\nResponse: {response.data}')

        # Verifica se a resposta é 400 devido à falta de idade
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)
        

    def test_login_usuario(self):
        """Testa o login de usuário via API"""

        # Criando um paciente
        url = reverse('registro')
        data = {
            "email": "novo_paciente_login@example.com",
            "username": "paciente01_login",
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
        usuario = Usuario.objects.get(email="novo_paciente_login@example.com")
        self.assertEqual(usuario.email, "novo_paciente_login@example.com")
        
        url = reverse('login')
        data = {
            "email": "novo_paciente_login@example.com",
            "password": "password"
        }

        response = self.client.post(url, data, format='json')
        print(f'\nResponse: {response.data}')

        # Verificando se o login foi bem-sucedido
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        

    def test_login_usuario_invalido(self):
        """Testa o login de usuário com senha inválida"""
        
        url = reverse('login')
        data = {
            "email": "teste_invalido@example.com",
            "password": "senhaerrada"
        }

        response = self.client.post(url, data, format='json')
        print(f'\nResponse: {response.data}')

        # Verificando se o login falhou
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        

    def test_registro_medico_sem_crm(self):
        """Testa a criação de médico sem o campo CRM."""
        
        url = reverse('registro')
        data = {
            "email": "medico_sem_crm@example.com",
            "username": "medico03",
            "password1": "password",
            "password2": "password",
            "user_type": "MED",
            "estado": "SP",
            "especialidade": 1,
        }

        response = self.client.post(url, data, format='json')
        print(f'\nResponse: {response.data}')

        # Verifica se a resposta é 400 devido à falta de CRM
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)
        

    def test_registro_medico_sem_estado(self):
        """Testa a criação de médico sem o campo estado."""
        
        url = reverse('registro')
        data = {
            "email": "medico_sem_estado@example.com",
            "username": "medico04",
            "password1": "password",
            "password2": "password",
            "user_type": "MED",
            "crm": "892448",
            "especialidade": 1,
        }

        response = self.client.post(url, data, format='json')
        print(f'\nResponse: {response.data}')

        # Verifica se a resposta é 400 devido à falta de estado
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)
        

    def test_registro_medico_sem_especialidade(self):
        """Testa a criação de médico sem o campo especialidade."""
        
        url = reverse('registro')
        data = {
            "email": "medico_sem_especialidade@example.com",
            "username": "medico05",
            "password1": "password",
            "password2": "password",
            "user_type": "MED",
            "crm": "985154",
            "estado": "SP",
        }

        response = self.client.post(url, data, format='json')
        print(f'\nResponse: {response.data}')

        # Verifica se a resposta é 400 devido à falta de especialidade
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)
