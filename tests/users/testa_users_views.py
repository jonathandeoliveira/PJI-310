import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.users.forms import UserProfileCreationForm, UserProfileLoginForm
from django.contrib.auth import SESSION_KEY
from datetime import date

User = get_user_model()

# Fixture para criar um usuário de teste com os campos obrigatórios


@pytest.fixture
def create_user(db):
    # Criando o usuário apenas com os campos obrigatórios
    user = User.objects.create_user(
        username='testuser',
        email= 'testuser2@example.com',
        document= '12345678901',
        postal_code= '12345678',
        phone='21987654321',
        birth_date='1990-01-01',
        full_address='Rua de Teste, 123',
        password1='Str0ngP@ssw0rd!',
        password2='Str0ngP@ssw0rd!',
        is_professor=True,
    )

    
    return user

# Teste GET para o formulário de registro


@pytest.mark.django_db
def test_register_view_get(client):
    # Testa o acesso à página de registro (GET)
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], UserProfileCreationForm)
    assert 'users/register.html' in [t.name for t in response.templates]

# Teste POST para registro com dados válidos


@pytest.mark.django_db
def test_register_view_post_valid_data(client):
    # Testa o registro de um novo usuário com dados válidos
    url = reverse('register')
    data = {
        'username': 'testuser2',
        'email': 'testuser2@example.com',
        'document': '12345678901',
        'postal_code': '12345678',
        'phone': '21987654321',
        'birth_date': '1990-01-01',
        'full_address': 'Rua de Teste, 123',
        'password1': 'Str0ngP@ssw0rd!',
        'password2': 'Str0ngP@ssw0rd!',
        'is_professor': True,
    }
    response = client.post(url, data)

    # Verifica os erros do formulário, caso haja
    if response.status_code == 200:
        print(response.context['form'].errors)

    assert response.status_code == 302  # Verifica redirecionamento após registro
    # Redireciona para a página inicial
    assert response.url == reverse('index')

# Teste POST para registro com dados inválidos (exemplo de email inválido)


@pytest.mark.django_db
def test_register_view_post_invalid_data(client):
    # Testa o registro com dados inválidos (email incorreto)
    url = reverse('register')
    data = {
        'username': 'testuser',
        'email': 'invalid-email',  # Email inválido
        'password1': 'Str0ngP@ssw0rd!',
        'password2': 'Str0ngP@ssw0rd!',
    }
    response = client.post(url, data)
    assert response.status_code == 200  # Fica na mesma página devido a erro
    assert 'form' in response.context
    # Verifica que há erros no formulário
    assert response.context['form'].errors

# Teste GET para o formulário de login


@pytest.mark.django_db
def test_custom_login_view_get(client):
    # Testa o acesso à página de login (GET)
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], UserProfileLoginForm)
    assert 'users/login.html' in response.template_name

# Teste POST para login com credenciais válidas


@pytest.mark.django_db
def test_custom_login_view_post_valid_credentials(client, create_user):
    # Testa o login com credenciais válidas
    url = reverse('login')
    response = client.post(
        url, {'username': 'testuser2@example.com',
              'password1': 'Str0ngP@ssw0rd!',
              'password2': 'Str0ngP@ssw0rd!'}
    )
    assert response.status_code == 302  # Redireciona após login bem-sucedido
    assert response.url == reverse('index')  # Redireciona para 'index'
    assert SESSION_KEY in client.session  # Confirma que o usuário está autenticado

# Teste POST para login com credenciais inválidas


@pytest.mark.django_db
def test_custom_login_view_post_invalid_credentials(client):
    # Testa o login com credenciais inválidas
    url = reverse('login')
    response = client.post(
        url, {'username': 'wronguser', 'password': 'wrongpassword'}
    )
    assert response.status_code == 200  # Fica na mesma página devido a erro
    assert 'form' in response.context
    # Verifica que há erros no formulário
    assert response.context['form'].errors

# Teste para logout de um usuário autenticado


@pytest.mark.django_db
def test_logout_view(client, create_user):
    # Testa o logout de um usuário autenticado
    client.login(username=create_user.username, password='Str0ngP@ssw0rd!')
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302  # Redireciona após logout
    assert response.url == reverse('login')  # Redireciona para 'login'
    # Confirma que o usuário foi desconectado
    assert SESSION_KEY not in client.session
