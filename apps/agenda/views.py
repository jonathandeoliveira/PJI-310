from django.shortcuts import render, redirect, get_object_or_404
from apps.agenda.models import Agenda
from apps.agenda.forms import AgendaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


#@login_required
def index(request):
    return render(request, "agenda/index.html")


#@login_required
def cadastrar_agenda(request):
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agenda cadastrada com sucesso!')
            return redirect('listar_agendas')
        else:
            messages.error(request, 'Corrija os erros do formulário.')
    else:
        form = AgendaForm()
    return render(request, "agenda/cadastrar_agenda.html", {'form': form})


#@login_required
def listar_agendas(request):
    user = request.user
    agendas = Agenda.objects.filter(Q(professor=user) | Q(aluno=user))
    return render(request, "agenda/listar_agendas.html", {'agendas': agendas})


#@login_required
def editar_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    if request.user != agenda.professor and request.user != agenda.aluno:
        messages.error(
            request, "Você não tem permissão para editar este treino.")
        return redirect('listar_agendas')

    form = AgendaForm(request.POST or None, instance=agenda)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Treino editado com sucesso!')
        return redirect('listar_agendas')

    return render(request, 'agenda/editar_agenda.html', {'form': form, 'agenda': agenda})


#@login_required
def deletar_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    if request.user != agenda.professor and request.user != agenda.aluno:
        messages.error(
            request, "Você não tem permissão para deletar este treino.")
        return redirect('listar_agendas')

    agenda.delete()
    messages.success(request, 'Treino deletado com sucesso!')
    return redirect('listar_agendas')
