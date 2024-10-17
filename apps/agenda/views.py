from django.shortcuts import render, redirect, get_object_or_404
from .models import Agenda
from apps.agenda.forms import AgendaForm
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, "agenda/index.html")

# View para cadastrar uma nova agenda
def cadastrar_agenda(request):
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('listar_agendas') 
    else:
        form = AgendaForm()

    return render(request, "agenda/cadastrar_agenda.html", {'form': form})

# View para exibir todas as agendas cadastradas
def listar_agendas(request):
    agendas = Agenda.objects.all()  
    return render(request, "agenda/listar_agendas.html", {'agendas': agendas})

# View para editar agenda
def editar_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    form = AgendaForm(request.POST or None, instance=agenda)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Treino editado com sucesso!')
            return redirect('listar_agendas')
    return render(request, 'agenda/editar_agenda.html', {'form': form, 'agenda': agenda})
    
# View para deletar agenda
def deletar_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    agenda.delete()
    messages.success(request, 'Treino deletado com sucesso!')
    return redirect('listar_agendas')
