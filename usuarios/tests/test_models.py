from django.test import TestCase
from usuarios.models import Usuario

class UsuarioModelTest(TestCase):
    """
    Testes para o modelo Usuario.
    """

    def setUp(self):

        # Criando usuário médico
        self.medico = Usuario.objects.create_user(
            email="medico@example.com",
            username="medico01",
            password="securepassword",
            user_type="MED",
            crm="123456",
            estado="SP",
            especialidade=1
        )

        # Criando usuário paciente
        self.paciente = Usuario.objects.create_user(
            email="paciente@example.com",
            username="paciente01",
            password="securepassword",
            user_type="PAC",
            idade=18
        )

        # Criando usuário administrador
        self.admin = Usuario.objects.create_superuser(
            email="admin@example.com",
            username="admin01",
            password="securepassword",
            user_type="ADM"
        )

    def test_usuario_criacao_medico(self):
        """Testa se um médico foi criado corretamente"""
        self.assertEqual(self.medico.email, "medico@example.com")
        self.assertEqual(self.medico.crm, "123456")
        self.assertEqual(self.medico.estado, "SP")
        self.assertEqual(self.medico.especialidade, 1)
        self.assertTrue(self.medico.is_medico)
        self.assertFalse(self.medico.is_paciente)
        self.assertFalse(self.medico.is_admin)

    def test_usuario_criacao_paciente(self):
        """\Testa se um paciente foi criado corretamente"""
        self.assertEqual(self.paciente.email, "paciente@example.com")
        self.assertEqual(self.paciente.idade, 18)
        self.assertTrue(self.paciente.is_paciente)
        self.assertFalse(self.paciente.is_medico)
        self.assertFalse(self.paciente.is_admin)

    def test_usuario_criacao_admin(self):
        """Testa se um administrador foi criado corretamente"""
        self.assertEqual(self.admin.email, "admin@example.com")
        self.assertTrue(self.admin.is_admin)
        self.assertFalse(self.admin.is_medico)
        self.assertFalse(self.admin.is_paciente)

    def test_usuario_str_representation(self):
        """Testa a representação de string do modelo"""
        self.assertEqual(str(self.medico), "Médico - medico@example.com - CRM123456/SP")
        self.assertEqual(str(self.paciente), "Paciente - paciente@example.com")
        self.assertEqual(str(self.admin), "Administrador - admin@example.com")

    def test_usuario_campo_obrigatorio_email(self):
        """Testa se a criação de usuário sem email falha"""
        with self.assertRaises(ValueError):
            Usuario.objects.create_user(email=None, username="noemail", password="password")

    def test_usuario_tipo_medico_campos_obrigatorios(self):
        """Testa se um médico precisa de CRM, estado e especialidade"""
        with self.assertRaises(Exception):
            Usuario.objects.create_user(
                email="medico_invalido@example.com",
                username="medico02",
                password="password",
                user_type="MED"
            )
    
    def test_usuario_tipo_paciente_idade_obrigatoria(self):
        """Testa se um paciente precisa de idade"""
        with self.assertRaises(ValueError):
            Usuario.objects.create_user(
                email="paciente_invalido@example.com",
                username="paciente02",
                password="password",
                user_type="PAC"
            )
