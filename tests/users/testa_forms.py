from django.test import TestCase
from django.utils import timezone
from apps.users.forms import UserProfileCreationForm
from apps.users.models import UserProfile

class UserProfileCreationFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'joaosilva',
            'email': 'joaosilva@example.com',
            'document': '12345678901',  # CPF com 11 dígitos
            'postal_code': '12345678',  # CEP com 8 dígitos
            'phone': '11987654321',  # Telefone com DDD
            'birth_date': '1990-01-01',
            'full_address': 'Rua Exemplo, 123, Bairro, Cidade, Estado',
            'password1': 'password123',  # senha para UserCreationForm
            'password2': 'password123',
            'is_professor': False,
        }

    def test_valid_form(self):
        form = UserProfileCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_duplicate_email(self):
        # Cria um usuário com o e-mail já existente
        UserProfile.objects.create_user(
            username='outro_user', email=self.valid_data['email'], password='senha456')
        
        form = UserProfileCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], "Este e-mail já está em uso.")

    def test_invalid_document(self):
        # CPF com menos de 11 dígitos
        self.valid_data['document'] = '12345678'
        form = UserProfileCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('document', form.errors)
        self.assertEqual(form.errors['document'][0], "O CPF deve ter exatamente 11 dígitos numéricos.")

    def test_duplicate_document(self):
        # Cria um usuário com o CPF já existente
        UserProfile.objects.create_user(
            username='outro_user', document=self.valid_data['document'], password='senha456')

        form = UserProfileCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('document', form.errors)
        self.assertEqual(form.errors['document'][0], "Este CPF já está cadastrado.")

    def test_invalid_postal_code(self):
        # CEP com menos de 8 dígitos
        self.valid_data['postal_code'] = '12345'
        form = UserProfileCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('postal_code', form.errors)
        self.assertEqual(form.errors['postal_code'][0], "O CEP deve ter exatamente 8 dígitos numéricos.")

    def test_invalid_phone(self):
        # Telefone com menos de 11 dígitos
        self.valid_data['phone'] = '119876543'
        form = UserProfileCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertEqual(form.errors['phone'][0], "O telefone deve ter exatamente 11 dígitos, incluindo o DDD.")

    def test_mismatched_passwords(self):
        # Senhas diferentes
        self.valid_data['password2'] = 'diferente123'
        form = UserProfileCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn('As duas senhas não coincidem.', form.errors['password2'][0])

    def test_birth_date_in_future(self):
        # Data de nascimento no futuro
        self.valid_data['birth_date'] = (timezone.now() + timezone.timedelta(days=1)).date()
        form = UserProfileCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)
