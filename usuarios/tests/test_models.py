from django.test import TestCase
from usuarios.models import Usuario, Medico, Paciente

class UsuarioModelTest(TestCase):

    def setUp(self):
        # Cria um usuário para ser usado nos testes
        self.usuario = Usuario.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="password123",
            first_name="Test",
            last_name="User"
        )

    def test_usuario_str(self):
        # Verifica se o método __str__ está retornando o e-mail do usuário
        self.assertEqual(str(self.usuario), "testuser@example.com")


class MedicoModelTest(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email="medico@example.com",
            username="medico",
            password="password123"
        )
        # Cria um médico para ser testado
        self.medico = Medico.objects.create(
            user=self.usuario,
            crm="123456",
            estado="SP",
            especialidade="CAR"  # Exemplo de especialidade: Cardiologia
        )

    def test_medico_str(self):
        # Verifica se o método __str__ do médico está correto
        self.assertEqual(str(self.medico), "CRM/SP 123456")

class PacienteModelTest(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email="paciente@example.com",
            username="paciente",
            password="password123"
        )
        # Cria um paciente para ser testado
        self.paciente = Paciente.objects.create(
            user=self.usuario,
            idade=30
        )

    def test_paciente_str(self):
        # Verifica se o método __str__ do paciente está correto
        self.assertEqual(str(self.paciente), "Test User - (paciente@example.com)")
