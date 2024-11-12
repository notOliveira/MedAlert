from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from usuarios.models import Usuario, Paciente, Medico

class UsuarioViewSetTest(APITestCase):

    def setUp(self):
        # Cria um usuário de teste
        self.usuario = Usuario.objects.create_user(
            email="user@example.com",
            username="user",
            password="password123",
            first_name="User",
            last_name="Example"
        )

    def test_get_usuarios(self):
        # Testa o endpoint GET para listar usuários
        url = reverse('usuario-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_usuario(self):
        # Testa o endpoint POST para criar um novo usuário
        url = reverse('registro-usuario')
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "password123",
            "first_name": "New",
            "last_name": "User"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 2)


class PacienteViewSetTest(APITestCase):

    def setUp(self):
        # Cria um usuário e um paciente
        self.usuario = Usuario.objects.create_user(
            email="paciente@example.com",
            username="paciente",
            password="password123"
        )
        self.paciente = Paciente.objects.create(user=self.usuario, idade=30)

    def test_get_pacientes(self):
        # Testa o endpoint GET para listar pacientes
        url = reverse('paciente-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MedicoViewSetTest(APITestCase):

    def setUp(self):
        # Cria um usuário e um médico
        self.usuario = Usuario.objects.create_user(
            email="medico@example.com",
            username="medico",
            password="password123"
        )
        self.medico = Medico.objects.create(
            user=self.usuario,
            crm="123456",
            estado="SP",
            especialidade="CAR"
        )

    def test_get_medicos(self):
        # Testa o endpoint GET para listar médicos
        url = reverse('medico-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_medico(self):
        # Testa o endpoint POST para criar um novo médico
        url = reverse('medico-list')
        data = {
            "user": self.usuario.id,
            "crm": "654321",
            "estado": "RJ",
            "especialidade": "PED"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medico.objects.count(), 2)
