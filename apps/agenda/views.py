from django.shortcuts import render, redirect
from .models import Agenda
from .forms import AgendaForm

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
