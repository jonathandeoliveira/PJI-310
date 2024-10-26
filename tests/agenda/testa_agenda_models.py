import pytest
from apps.agenda.models import Agenda

@pytest.mark.django_db
def test_agenda():
    # lógica do teste aqui
    assert Agenda.objects.count() == 0  # exemplo de verificação
