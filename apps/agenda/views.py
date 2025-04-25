from django.shortcuts import render, redirect, get_object_or_404
from apps.agenda.models import Agenda
from apps.agenda.forms import AgendaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from bokeh.plotting import figure, show
import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta 
from bokeh.embed import components
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Sum



def index(request):
    return render(request, "agenda/index.html")


@login_required
def cadastrar_agenda(request):
    if request.method == "POST":
        form = AgendaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Agenda cadastrada com sucesso!")
            return redirect("listar_agendas")
        else:
            messages.error(request, "Corrija os erros do formulário.")
    else:
        form = AgendaForm()
    return render(request, "agenda/cadastrar_agenda.html", {"form": form})


@login_required
def listar_agendas(request):
    user = request.user
    agendas = Agenda.objects.filter(Q(professor=user) | Q(aluno=user))
    return render(request, "agenda/listar_agendas.html", {"agendas": agendas})


@login_required
def editar_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    if request.user != agenda.professor and request.user != agenda.aluno:
        messages.error(request, "Você não tem permissão para editar este treino.")
        return redirect("listar_agendas")

    form = AgendaForm(request.POST or None, instance=agenda)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Treino editado com sucesso!")
        return redirect("listar_agendas")

    return render(
        request, "agenda/editar_agenda.html", {"form": form, "agenda": agenda}
    )


@login_required
def deletar_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    if request.user != agenda.professor and request.user != agenda.aluno:
        messages.error(request, "Você não tem permissão para deletar este treino.")
        return redirect("listar_agendas")

    agenda.delete()
    messages.success(request, "Treino deletado com sucesso!")
    return redirect("listar_agendas")

@login_required
def analytics_view(request):
    # Filtrar as aulas da professora logada
    professor = request.user
    data_limite = datetime.today() - relativedelta(months=3)
    aulas = Agenda.objects.filter(professor=professor,data__gte=data_limite)
      
    #somar os valores por mês
    aulas_por_mes = (
        aulas.annotate(mes=ExtractMonth('data'),ano=ExtractYear('data'))
        .values('mes','ano')
        .annotate(total=Sum('valor'))
        .order_by('ano','mes')
    )
    
    
    # Extrair os dados para o gráfico
    valores = [aula['total'] for aula in aulas_por_mes]
    
    #Bokeh não aceita decimal, então é necessário converter para float
    v=[float(v) for v in valores]
   
    #Código específico para mostrar os últimos 3 meses, no formato mês/ano.
    ultimos_meses = [
    (datetime.today() - relativedelta(months=2)).replace(day=1),
    (datetime.today() - relativedelta(months=1)).replace(day=1),
     datetime.today().replace(day=1),
    ]
    
    dados_reais = {
    (aula['mes'], aula['ano']): float(aula['total'])
    for aula in aulas_por_mes
    }
    
    meses_formatados = []
    valores_formatados = []

    for data in ultimos_meses:
        mes = data.month
        ano = data.year
        total = dados_reais.get((mes, ano), 0)  # Pega valor real ou 0
        label = f"{calendar.month_abbr[mes]}/{ano}"  
        meses_formatados.append(label)
        valores_formatados.append(total)
      
    # Criar o gráfico com Bokeh
    p = figure(#title="Relatório Financeiro (últimos 3 meses)",
        #title_location="above",
        x_axis_label="Mês",
        y_axis_label="Total (R$)",
        #x_range=[str(mes) for mes in meses_nomes],
        x_range=meses_formatados,
        y_range=(0, max(v) + 20),
        width=800,
        height=400,
        active_drag=None, 
        active_scroll=None,
        active_inspect=None,
        toolbar_location=None,
        )
    
    # Configurações do grafico
    p.vbar(x=meses_formatados, top=valores_formatados, width=0.5, color="blue")
    p.title.align = "left"
    p.title.text_font_size = "24px"
    p.title.text_color = "Blue"
    p.background_fill_color = "#F0F0FF"
    p.border_fill_color = "#F0F0FF" 
    p.xaxis.major_label_text_font_size = "14pt"
    p.yaxis.major_label_text_font_size = "14pt"
    p.xaxis.axis_label_text_font_size = "16pt"
    p.yaxis.axis_label_text_font_size = "16pt"   

        

    script, div = components(p)
    
    #print(script[:300])
    #print(div[:300])

    #Consulta aos alunos do professor.
    #user = request.user
    agendas = Agenda.objects.filter(Q(professor=professor) | Q(aluno=professor))
        
    return render(request, "agenda/analytics.html", {"script": script, "div": div, "agendas": agendas})
