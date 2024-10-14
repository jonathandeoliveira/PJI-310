from django.urls import path
from apps.agenda.views import \
    index, listar_agendas, cadastrar_agenda

urlpatterns = [
    path("", index, name='index'), 
    path("inicio/", listar_agendas, name='listar_agendas'),
    path("cadastrar/", cadastrar_agenda, name='cadastrar_agenda'),
]