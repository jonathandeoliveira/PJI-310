import pytest
from django.urls import reverse
from apps.agenda.models import Agenda
from apps.users.models import UserProfile
from datetime import date
from decimal import Decimal


@pytest.mark.django_db
def test_cadastrar_agenda_view(client):
    # Cria o professor e o aluno com todos os campos obrigatórios
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

    # Autentica o professor
    logged_in = client.login(username="professor_teste", password="senha123")
    assert logged_in  # Confirma que o login foi bem-sucedido

    # Cadastra a agenda
    response = client.post(reverse('cadastrar_agenda'), {
        'professor': professor.id,
        'aluno': aluno.id,
        'valor': Decimal('100.0'),
        'data': '2024-10-28',
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })

    # Verifica o redirecionamento e criação da agenda
    assert response.status_code == 302
    assert Agenda.objects.count() == 1


@pytest.mark.django_db
def test_listar_agendas_view(client):
    # Configura o professor e o aluno
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

    # Cria a agenda
    Agenda.objects.create(
        professor=professor,
        aluno=aluno,
        valor=Decimal('100.0'),
        data='2024-10-28',
        hora='10:00',
        descricao='Descrição do treino',
    )

    # Autentica o professor
    logged_in = client.login(username="professor_teste", password="senha123")
    assert logged_in

    response = client.get(reverse('listar_agendas'))
    assert response.status_code == 200
    assert 'agendas' in response.context
    assert len(response.context['agendas']) == 1


@pytest.mark.django_db
def test_editar_agenda_view(client):
    # Configura o professor e o aluno
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

    agenda = Agenda.objects.create(
        professor=professor,
        aluno=aluno,
        valor=Decimal('100.0'),
        data='2024-10-28',
        hora='10:00',
        descricao='Descrição do treino',
    )

    logged_in = client.login(username="professor_teste", password="senha123")
    assert logged_in

    response = client.post(reverse('editar_agenda', args=[agenda.id]), {
        'professor': professor.id,
        'aluno': aluno.id,
        'valor': Decimal('150.0'),  # Usando Decimal diretamente
        'data': '2024-10-28',
        'hora': '11:00',
        'descricao': 'Descrição do treino editada',
    })

    assert response.status_code == 302
    agenda.refresh_from_db()
    assert agenda.valor == Decimal('150.0')
    assert agenda.hora == '11:00'


@pytest.mark.django_db
def test_deletar_agenda_view(client):
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

    agenda = Agenda.objects.create(
        professor=professor,
        aluno=aluno,
        valor=Decimal('100.0'),
        data='2024-10-28',
        hora='10:00',
        descricao='Descrição do treino',
    )

    logged_in = client.login(username="professor_teste", password="senha123")
    assert logged_in

    response = client.post(reverse('deletar_agenda', args=[agenda.id]))
    assert response.status_code == 302
    assert Agenda.objects.count() == 0
