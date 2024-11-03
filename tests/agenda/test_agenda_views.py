import pytest
from datetime import date, timedelta, time
from decimal import Decimal
from django.urls import reverse
from apps.users.models import UserProfile
from apps.agenda.models import Agenda

@pytest.mark.django_db
def test_cadastrar_agenda_view(client):
    # Criação de usuário professor e aluno
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

    # Autentica o professor pelo e-mail
    logged_in = client.login(
        email="professor_teste@example.com", password="senha123")
    assert logged_in, "Login falhou, verifique as credenciais"

    # Define a data do treino como amanhã
    data_treino = date.today() + timedelta(days=1)

    # Tenta cadastrar a agenda
    response = client.post(reverse('cadastrar_agenda'), {
        'professor': professor.id,
        'aluno': aluno.id,
        'valor': '100.0',
        'data': data_treino,
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })

    assert response.status_code == 302, "Redirecionamento após cadastro falhou"
    assert Agenda.objects.count() == 1


@pytest.mark.django_db
def test_editar_agenda_view(client):
    # Criação de usuário professor e aluno
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

    # Criação da agenda com data no futuro
    data_treino = date.today() + timedelta(days=1)
    agenda = Agenda.objects.create(
        professor=professor,
        aluno=aluno,
        valor=Decimal('100.0'),
        data=data_treino,
        hora=time(10, 0),
        descricao='Descrição do treino',
    )

    # Autentica o professor pelo e-mail
    logged_in = client.login(
        email="professor_teste@example.com", password="senha123")
    assert logged_in, "Login falhou, verifique as credenciais"

    # Tenta editar a agenda
    response = client.post(reverse('editar_agenda', args=[agenda.id]), {
        'professor': professor.id,
        'aluno': aluno.id,
        'valor': '150.0',
        'data': data_treino,
        'hora': '11:00',
        'descricao': 'Descrição do treino editada',
    })

    assert response.status_code == 302, "Redirecionamento após edição falhou"
    agenda.refresh_from_db()
    assert agenda.valor == Decimal('150.0')
    # Corrigido para comparar com datetime.time
    assert agenda.hora == time(11, 0)


@pytest.mark.django_db
def test_deletar_agenda_view(client):
    # Criação de usuário professor e aluno
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

    # Criação da agenda
    data_treino = date.today() + timedelta(days=1)
    agenda = Agenda.objects.create(
        professor=professor,
        aluno=aluno,
        valor=Decimal('100.0'),
        data=data_treino,
        hora=time(10, 0),
        descricao='Descrição do treino',
    )

    # Autentica o professor pelo e-mail
    client.login(email="professor_teste@example.com", password="senha123")

    # Tenta deletar a agenda
    response = client.post(reverse('deletar_agenda', args=[agenda.id]))
    assert response.status_code == 302, "Redirecionamento após deleção falhou"
    assert not Agenda.objects.filter(
        id=agenda.id).exists(), "Agenda não foi deletada"
