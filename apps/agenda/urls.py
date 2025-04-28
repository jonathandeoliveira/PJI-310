from django.urls import path
from apps.agenda.views import (
    index,
    listar_agendas,
    cadastrar_agenda,
    editar_agenda,
    deletar_agenda,
    analytics_view,
    analytics_details,
    cancelar_agenda,
)
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listar_agendas/", listar_agendas, name="listar_agendas"),
    path("cadastrar/", cadastrar_agenda, name="cadastrar_agenda"),
    path("editar_agenda/<int:agenda_id>/", editar_agenda, name="editar_agenda"),
    path("deletar_agenda/<int:agenda_id>/", deletar_agenda, name="deletar_agenda"),
    path("analytics/", analytics_view, name="analytics"),
    path("analytics_finance/", analytics_details, name="analytics_finance"),
    path("cancelar_agenda/<int:agenda_id>/", cancelar_agenda, name="cancelar_agenda"),
]
