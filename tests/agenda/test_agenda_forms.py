import pytest
from apps.agenda.models import Agenda
from freezegun import freeze_time
from apps.agenda.forms import AgendaForm

@pytest.mark.django_db
def test_agenda():
    # lógica do teste aqui
    assert Agenda.objects.count() == 0  # exemplo de verificação

# Data fixa para todos os testes, pra o teste dar verdadeiro no caso da data fixa + 1
@freeze_time("2024-10-27")
@pytest.mark.django_db
# Teste com dia permitido, maior que o dia atual
def test_next_day_allowed():
    agenda = AgendaForm()
    agenda.data = "2024-10-28"
    assert AgendaForm.clean_data(agenda) == True
@freeze_time("2024-10-27")
@pytest.mark.django_db
# Teste com dia permitido, dia atual
def test_same_day_allowed():
    agenda = AgendaForm()
    agenda.data = "2024-10-27"
    assert AgendaForm.clean_data(agenda) == True
@freeze_time("2024-10-27")
@pytest.mark.django_db
# Teste com dia anterior
def test_day_not_allowed():
    agenda = AgendaForm()
    agenda.data = "2024-10-26"
    assert AgendaForm.clean_data(agenda) == False

@freeze_time("2024-10-27")
@pytest.mark.django_db
def test_invalid_dates():
    agenda = AgendaForm()
    agenda.data = "invalid-date"
    assert AgendaForm.clean_data(agenda) == False
