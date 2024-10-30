import pytest
from apps.agenda.forms import AgendaForm
from freezegun import freeze_time

@pytest.mark.django_db

@freeze_time("2024-10-27")
def test_next_data_allowed():
    form = AgendaForm(data={
        'professor': 'Professor Teste',
        'aluno': 'Aluno Teste',
        'valor': 100.0,
        'data': '2024-10-28',  # Data futura permitida
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })
    assert form.is_valid()  # O formulário deve ser válido

@freeze_time("2024-10-27")
@pytest.mark.django_db
def test_same_data_allowed():
    form = AgendaForm(data={
        'professor': 'Professor Teste',
        'aluno': 'Aluno Teste',
        'valor': 100.0,
        'data': '2024-10-27',  # Data atual permitida
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })
    assert form.is_valid()  # O formulário deve ser válido

@freeze_time("2024-10-27")
@pytest.mark.django_db
def test_data_not_allowed():
    form = AgendaForm(data={
        'professor': 'Professor Teste',
        'aluno': 'Aluno Teste',
        'valor': 100.0,
        'data': '2024-10-26',  # Data passada não permitida
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })
    assert not form.is_valid()  # O formulário deve ser inválido
    assert 'data' in form.errors  # A mensagem de erro deve estar no campo data

@freeze_time("2024-10-27")
@pytest.mark.django_db
def test_invalid_data():
    form = AgendaForm(data={
        'professor': 'Professor Teste',
        'aluno': 'Aluno Teste',
        'valor': 100.0,
        'data': 'invalid-date',  # Data inválida
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })
    assert not form.is_valid()  # O formulário deve ser inválido
    assert 'data' in form.errors  # A mensagem de erro deve estar no campo data

@pytest.mark.django_db
def test_empty_data():
    form = AgendaForm(data={
        'professor': 'Professor Teste',
        'aluno': 'Aluno Teste',
        'valor': 100.0,
        'data': '',  # Data vazia
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })
    assert not form.is_valid()  # O formulário deve ser inválido
    assert 'data' in form.errors  # A mensagem de erro deve estar no campo data

@pytest.mark.django_db
def test_negative_valor():
    form = AgendaForm(data={
        'professor': 'Professor Teste',
        'aluno': 'Aluno Teste',
        'valor': -10.9,  # Valor negativo não permitido
        'data': '2024-10-28',
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })
    assert not form.is_valid()  # O formulário deve ser inválido
    assert 'valor' in form.errors  # A mensagem de erro deve estar no campo valor

@pytest.mark.django_db
def test_empty_valor():
    form = AgendaForm(data={
        'professor': 'Professor Teste',
        'aluno': 'Aluno Teste',
        'valor': '',  # Valor vazio
        'data': '2024-10-28',
        'hora': '10:00',
        'descricao': 'Descrição do treino',
    })
    assert not form.is_valid()  # O formulário deve ser inválido
    assert 'valor' in form.errors  # A mensagem de erro deve estar no campo valor
