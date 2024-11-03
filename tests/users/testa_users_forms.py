from django.test import TestCase
from apps.users.forms import UserProfileCreationForm, UserProfileLoginForm
from apps.users.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileFormTest(TestCase):

    def test_user_profile_creation_form_valid(self):
        form_data = {
            'username': 'Joaosilva',
            'email': 'joao@example.com',
            'document': '12345678901',
            'postal_code': '12345678',
            'phone': '11987654321',
            'birth_date': '2000-01-01',
            'full_address': 'Rua Exemplo, 123, Bairro, Cidade, Estado',
            'password1': 'Teste@123!',
            'password2': 'Teste@123!',
            'is_professor': True,
        }
        form = UserProfileCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'Joaosilva')
        self.assertEqual(user.email, 'joao@example.com')

    def test_user_profile_creation_form_invalid_email(self):
        UserProfile.objects.create_user(
            username='testuser', email='joao@example.com', password='testpassword',
            document='12345678901', postal_code='12345678',
            phone='11987654321', birth_date='2000-01-01', full_address='Rua Exemplo, 123, Bairro, Cidade, Estado'
        )
        form_data = {
            'username': 'Joaosilva',
            'email': 'joao@example.com',  # E-mail duplicado
            'document': '12345678901',
            'postal_code': '12345678',
            'phone': '11987654321',
            'birth_date': '2000-01-01',
            'full_address': 'Rua Exemplo, 123, Bairro, Cidade, Estado',
            'password1': 'Teste@123!',
            'password2': 'Teste@123!',
            'is_professor': True,
        }
        form = UserProfileCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Este e-mail já está em uso.', form.errors['email'])

    def test_user_profile_creation_form_invalid_cpf(self):
        form_data = {
            'username': 'Joaosilva',
            'email': 'joao@example.com',
            'document': '1234567890',  # CPF inválido
            'postal_code': '12345678',
            'phone': '11987654321',
            'birth_date': '2000-01-01',
            'full_address': 'Rua Exemplo, 123, Bairro, Cidade, Estado',
            'password1': 'Teste@123!',
            'password2': 'Teste@123!',
            'is_professor': True,
        }
        form = UserProfileCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'O CPF deve ter exatamente 11 dígitos numéricos.', form.errors['document'])

    def test_user_profile_creation_form_invalid_postal_code(self):
        form_data = {
            'username': 'Joaosilva',
            'email': 'joao@example.com',
            'document': '12345678901',
            'postal_code': '1234567',  # CEP inválido
            'phone': '11987654321',
            'birth_date': '2000-01-01',
            'full_address': 'Rua Exemplo, 123, Bairro, Cidade, Estado',
            'password1': 'Teste@123!',
            'password2': 'Teste@123!',
            'is_professor': True,
        }
        form = UserProfileCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('O CEP deve ter exatamente 8 dígitos numéricos.',
                      form.errors['postal_code'])

    def test_user_profile_creation_form_invalid_phone(self):
        form_data = {
            'username': 'Joaosilva',
            'email': 'joao@example.com',
            'document': '12345678901',
            'postal_code': '12345678',
            'phone': '1198765432',  # Telefone inválido
            'birth_date': '2000-01-01',
            'full_address': 'Rua Exemplo, 123, Bairro, Cidade, Estado',
            'password1': 'Teste@123!',
            'password2': 'Teste@123!',
            'is_professor': True,
        }
        form = UserProfileCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'O telefone deve ter exatamente 11 dígitos, incluindo o DDD.', form.errors['phone'])

    def test_user_profile_creation_form_missing_birth_date(self):
        form_data = {
            'username': 'Joaosilva',
            'email': 'joao@example.com',
            'document': '12345678901',
            'postal_code': '12345678',
            'phone': '11987654321',
            'birth_date': '',  # Deixa o birth_date vazio para testar a validação
            'full_address': 'Rua Exemplo, 123, Bairro, Cidade, Estado',
            'password1': 'Teste@123!',
            'password2': 'Teste@123!',
            'is_professor': True,
        }

        form_data.pop('birth_date')

        form = UserProfileCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Este campo é obrigatório.', form.errors['birth_date'])


class UserProfileLoginFormTest(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            document='12345678901',
            postal_code='12345678',
            phone='11987654321',
            birth_date='2000-01-01',
            full_address='Rua Exemplo, 123, Bairro, Cidade, Estado',
        )

    def test_login_form_valid(self):
        form_data = {
            'username': 'testuser@example.com',
            'password': 'testpassword'
        }
        form = UserProfileLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.get_user()
        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)

    def test_login_form_empty_fields(self):
        form_data = {
            'username': '',
            'password': ''
        }
        form = UserProfileLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Este campo é obrigatório.', form.errors['username'])
        self.assertIn('Este campo é obrigatório.', form.errors['password'])

    def test_login_form_missing_username(self):
        form_data = {
            'username': '',
            'password': 'testpassword'
        }
        form = UserProfileLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Este campo é obrigatório.', form.errors['username'])

    def test_login_form_missing_password(self):
        form_data = {
            'username': 'testuser@example.com',
            'password': ''
        }
        form = UserProfileLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Este campo é obrigatório.', form.errors['password'])

