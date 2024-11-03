import pytest
from apps.agenda.forms import AgendaForm
from apps.users.models import UserProfile
from freezegun import freeze_time
from datetime import date

@pytest.mark.django_db
# Teste para verificar se é possível criar uma agenda com informações válidas
@freeze_time("2024-10-27")
def test_next_data_allowed():
    # Criação de um professor com todos os campos necessários
    professor = UserProfile.objects.create_user(
        username="professor_teste",
        email="professor_teste@example.com",
        password="senha123",
        document="12345678901",
        postal_code="12345678",
        phone="11912341234",
        birth_date=date(1980, 1, 1),
        full_address="Endereço do Professor",
        is_professor=True,
    )

    # Criação de um aluno com todos os campos necessários
    aluno = UserProfile.objects.create_user(
        username="aluno_teste",
        email="aluno_teste@example.com",
        password="senha123",
        document="10987654321",
        postal_code="87654321",
        phone="21987654321",
        birth_date=date(2000, 5, 15),
        full_address="Endereço do Aluno",
        is_professor=False,
    )

    # Preenchimento do formulário de agendamento com dados válidos
    form = AgendaForm(data={
        'professor': professor.id,
        'aluno': aluno.id,
        'valor': 100.0,
        'data': '2024-10-28',  # Data futura
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })
    # Verifica se o formulário é válido
    assert form.is_valid()


@pytest.mark.django_db
@freeze_time("2024-10-27")
# Teste para verificar se é permitido agendar para o mesmo dia
def test_same_day_data_allowed():
    # Criação de um professor
    professor = UserProfile.objects.create_user(
        username="professor_teste",
        email="professor_teste@example.com",
        password="senha123",
        document="12345678901",
        postal_code="12345678",
        phone="11912341234",
        birth_date=date(1980, 1, 1),
        full_address="Endereço do Professor",
        is_professor=True,
    )

    # Criação de um aluno
    aluno = UserProfile.objects.create_user(
        username="aluno_teste",
        email="aluno_teste@example.com",
        password="senha123",
        document="10987654321",
        postal_code="87654321",
        phone="21987654321",
        birth_date=date(2000, 5, 15),
        full_address="Endereço do Aluno",
        is_professor=False,
    )

    # Preenchimento do formulário para agendar para a data atual
    form = AgendaForm(data={
        'professor': professor.id,
        'aluno': aluno.id,
        'valor': 100.0,
        'data': '2024-10-27',  # Data atual
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })
    # Verifica se o formulário é válido
    assert form.is_valid()


@pytest.mark.django_db
@freeze_time("2024-10-27")
# Teste para verificar se não é permitido agendar para uma data passada
def test_past_date_not_allowed():
    # Criação de um professor
    professor = UserProfile.objects.create_user(
        username="professor_teste",
        email="professor_teste@example.com",
        password="senha123",
        document="12345678901",
        postal_code="12345678",
        phone="11912341234",
        birth_date=date(1980, 1, 1),
        full_address="Endereço do Professor",
        is_professor=True,
    )

    # Criação de um aluno
    aluno = UserProfile.objects.create_user(
        username="aluno_teste",
        email="aluno_teste@example.com",
        password="senha123",
        document="10987654321",
        postal_code="87654321",
        phone="21987654321",
        birth_date=date(2000, 5, 15),
        full_address="Endereço do Aluno",
        is_professor=False,
    )

    # Preenchimento do formulário com uma data passada
    form = AgendaForm(data={
        'professor': professor.id,
        'aluno': aluno.id,
        'valor': 100.0,
        'data': '2024-10-26',  # Data passada
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })
    # Verifica que o formulário não é válido
    assert not form.is_valid()
    # Verifica se o erro está no campo de data
    assert 'data' in form.errors


@pytest.mark.django_db
# Teste para verificar se valores inválidos (negativos) são rejeitados
def test_invalid_value():
    # Criação de um professor
    professor = UserProfile.objects.create_user(
        username="professor_teste",
        email="professor_teste@example.com",
        password="senha123",
        document="12345678901",
        postal_code="12345678",
        phone="11912341234",
        birth_date=date(1980, 1, 1),
        full_address="Endereço do Professor",
        is_professor=True,
    )

    # Criação de um aluno
    aluno = UserProfile.objects.create_user(
        username="aluno_teste",
        email="aluno_teste@example.com",
        password="senha123",
        document="10987654321",
        postal_code="87654321",
        phone="21987654321",
        birth_date=date(2000, 5, 15),
        full_address="Endereço do Aluno",
        is_professor=False,
    )

    # Preenchimento do formulário com um valor negativo
    form = AgendaForm(data={
        'professor': professor.id,
        'aluno': aluno.id,
        'valor': -50.0,  # Valor negativo não permitido
        'data': '2024-10-28',
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })
    # Verifica que o formulário não é válido
    assert not form.is_valid()
    # Verifica se o erro está no campo de valor
    assert 'valor' in form.errors


@pytest.mark.django_db
# Teste para verificar se campos obrigatórios vazios são tratados corretamente
def test_empty_required_fields():
    # Criação de um professor
    professor = UserProfile.objects.create_user(
        username="professor_teste",
        email="professor_teste@example.com",
        password="senha123",
        document="12345678901",
        postal_code="12345678",
        phone="11912341234",
        birth_date=date(1980, 1, 1),
        full_address="Endereço do Professor",
        is_professor=True,
    )

    # Criação de um aluno
    aluno = UserProfile.objects.create_user(
        username="aluno_teste",
        email="aluno_teste@example.com",
        password="senha123",
        document="10987654321",
        postal_code="87654321",
        phone="21987654321",
        birth_date=date(2000, 5, 15),
        full_address="Endereço do Aluno",
        is_professor=False,
    )

    # Preenchimento do formulário deixando campos obrigatórios vazios
    form = AgendaForm(data={
        'professor': professor.id,
        'aluno': aluno.id,
        'valor': '',  # Valor vazio
        'data': '',  # Data vazia
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })
    # Verifica que o formulário não é válido
    assert not form.is_valid()
    # Verifica se o erro está no campo de valor
    assert 'valor' in form.errors
    # Verifica se o erro está no campo de data
    assert 'data' in form.errors
