from django.urls import path
from apps.agenda.views import \
    index, listar_agendas, cadastrar_agenda, editar_agenda, deletar_agenda
  

urlpatterns = [
    path("", index, name='index'), 
    path("inicio/", listar_agendas, name='listar_agendas'),
    path("cadastrar/", cadastrar_agenda, name='cadastrar_agenda'),
    path("editar_agenda/<int:agenda_id>/", editar_agenda, name='editar_agenda'),
    path("deletar_agenda/<int:agenda_id>/", deletar_agenda, name="deletar_agenda"),
]