import pytest
from apps.agenda.models import Agenda
from freezegun import freeze_time
from apps.agenda.forms import AgendaForm
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_agenda():
    # lógica do teste aqui
    assert Agenda.objects.count() == 0  # exemplo de verificação

# Data fixa para todos os testes, pra o teste dar verdadeiro no caso da data fixa + 1
@freeze_time("2024-10-27")
@pytest.mark.django_db
# Teste da funcao clean_data com dia permitido, maior que o dia atual
def test_next_data_allowed():
    agenda = AgendaForm()
    agenda.data = "2024-10-28"
    assert AgendaForm.clean_data(agenda) == agenda
@freeze_time("2024-10-27")
@pytest.mark.django_db
# Teste da funcao clean_data com dia permitido, dia atual
def test_same_data_allowed():
    agenda = AgendaForm()
    agenda.data = "2024-10-27"
    assert AgendaForm.clean_data(agenda) == agenda
@freeze_time("2024-10-27")
@pytest.mark.django_db
# Teste da funcao clean_data com dia anterior
def test_data_not_allowed():
    agenda = AgendaForm()
    agenda.data = "2024-10-26"
    with pytest.raises(ValidationError, match='A data do treino não pode ser no passado.'):
        AgendaForm.clean_data(agenda)

@freeze_time("2024-10-27")
@pytest.mark.django_db
# Teste da funcao clean_data com data invalida
def test_invalid_data():
    agenda = AgendaForm()
    agenda.data = "invalid-date"
    with pytest.raises(ValidationError, match='A data do treino não pode ser no passado.'):
        AgendaForm.clean_data(agenda)

@pytest.mark.django_db
#Teste da funcao clean_data com data preenchida com espaco
def test_empty_data():
    agenda = AgendaForm()
    agenda.data = " "
    with pytest.raises(ValidationError, match='A data do treino não pode ser no passado.'):
        AgendaForm.clean_data(agenda)

@pytest.mark.django_db
#teste da funcao clean_valor com valor negativo
def test_negative_valor():
    agenda = AgendaForm()
    agenda.valor = -10,9
    with pytest.raises(ValidationError, match='O valor da aula deve ser maior que zero.'):
        AgendaForm.clean_valor(agenda)

@pytest.mark.django_db
#Teste da funcao clean_valor com valor preenchido com espaco
def test_empty_valor():
    agenda = AgendaForm()
    agenda.valor = " "
    with pytest.raises(ValidationError, match='A data do treino não pode ser no passado.'):
        AgendaForm.clean_valor(agenda)
