from django.shortcuts import render, redirect, get_object_or_404
from apps.users.models import UserProfile
from apps.agenda.models import Agenda
from apps.agenda.forms import AgendaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from bokeh.embed import components
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Sum

from django.utils import timezone
from datetime import datetime
from datetime import timedelta

from apps.notificacoes.services import enviar_email

def index(request):
    return render(request, "agenda/index.html")


@login_required
def cadastrar_agenda(request):
    if request.method == "POST":
        form = AgendaForm(request.POST, user=request.user)
        if form.is_valid():
            agenda = form.save(commit=False)
            if request.user.is_professor:
                agenda.professor = request.user
            else:
                agenda.aluno = request.user
            agenda.save()

            # Envia notificação(e-mail) ao criar um treino
            enviar_email(
                destinatarios=[agenda.professor.email, agenda.aluno.email],
                assunto="Novo Treino Agendado!",
                mensagem=(
                    f"Olá {agenda.professor.email} e {agenda.aluno.email},\n\n"
                    f"Um novo treino foi agendado!\n\n"
                    f"Data: {agenda.data}\n"
                    f"Hora: {agenda.hora}\n"
                    f"Descrição: {agenda.descricao}\n\n"
                    f"Abraços,\nEquipe Agenda Fácil"
                )
            )

            messages.success(request, "Agenda cadastrada com sucesso!")
            return redirect("listar_agendas")

        else:
            messages.error(request, "Corrija os erros do formulário.")
    else:
        form = AgendaForm(user=request.user)

    return render(request, "agenda/cadastrar_agenda.html", {"form": form})


@login_required
def listar_agendas(request):
    user = request.user
    filtro = request.GET.get("filtro", "futuras")
    hoje = timezone.localdate()

    # Busca agendas relacionadas ao usuário
    agendas = Agenda.objects.filter(Q(professor=user) | Q(aluno=user))

    # Aplicando filtros com base na query string
    if filtro == "futuras":
        agendas = agendas.filter(data__gt=hoje, cancelado=False)
    elif filtro == "passadas":
        agendas = agendas.filter(data__lt=hoje, cancelado=False)
    elif filtro == "canceladas":
        agendas = agendas.filter(cancelado=True)
    elif filtro == "finalizadas":
        agendas = agendas.filter(data__lt=hoje, cancelado=False)

    agendas = agendas.order_by("data", "hora")

    return render(
        request,
        "agenda/listar_agendas.html",
        {
            "agendas": agendas,
            "filtro_aplicado": filtro,
            "hoje": hoje,
        }
    )


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
    aulas = Agenda.objects.filter(professor=professor, data__gte=data_limite)

    # somar os valores por mês
    aulas_por_mes = (
        aulas.annotate(mes=ExtractMonth("data"), ano=ExtractYear("data"))
        .values("mes", "ano")
        .annotate(total=Sum("valor"))
        .order_by("ano", "mes")
    )

    # Extrair os dados para o gráfico
    valores = [aula["total"] for aula in aulas_por_mes]

    # Bokeh não aceita decimal, então é necessário converter para float
    v = [float(v) for v in valores]

    # Código específico para mostrar os últimos 3 meses, no formato mês/ano.
    ultimos_meses = [
        (datetime.today() - relativedelta(months=2)).replace(day=1),
        (datetime.today() - relativedelta(months=1)).replace(day=1),
        datetime.today().replace(day=1),
    ]

    dados_reais = {
        (aula["mes"], aula["ano"]): float(aula["total"]) for aula in aulas_por_mes
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
    p = figure(  # title="Relatório Financeiro (últimos 3 meses)",
        # title_location="above",
        x_axis_label="Mês",
        y_axis_label="Total (R$)",
        # x_range=[str(mes) for mes in meses_nomes],
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

    # print(script[:300])
    # print(div[:300])

    # Consulta aos alunos do professor.
    # user = request.user
    alunos_ativos = UserProfile.objects.filter(Q(is_professor=False)|Q(is_active=True))

    return render(
        request,
        "agenda/analytics.html",
        {"script": script, "div": div, "alunos_ativos": alunos_ativos},
    )


@login_required
def analytics_details(request):

    # Filtrar as aulas da professora logada
    professor = request.user
    periodo = int(
        request.GET.get("periodo", 6)
    )  # valor padrão 6 meses se não enviar nada
    data_limite = datetime.today() - relativedelta(months=periodo)
    aulas = Agenda.objects.filter(professor=professor, data__gte=data_limite)

    # somar os valores por mês
    aulas_por_mes = (
        aulas.annotate(mes=ExtractMonth("data"), ano=ExtractYear("data"))
        .values("mes", "ano")
        .annotate(total=Sum("valor"))
        .order_by("ano", "mes")
    )

    # Calcular os rendimentos de acordo com o período
    valor_total = aulas.aggregate(total=Sum("valor"))["total"] or 0
    valor_medio = valor_total / periodo if periodo else 0

    # Extrair os dados para o gráfico
    valores = [aula["total"] for aula in aulas_por_mes]

    # Bokeh não aceita decimal, então é necessário converter para float
    v = [float(v) for v in valores]

    # Código específico para mostrar os meses no periodo selecionado
    ultimos_meses = [
        (datetime.today() - relativedelta(months=i)).replace(day=1)
        for i in reversed(range(periodo))
    ]

    dados_reais = {
        (aula["mes"], aula["ano"]): float(aula["total"]) for aula in aulas_por_mes
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
    p = figure(
        y_range=meses_formatados,
        x_axis_label="Total (R$)",
        y_axis_label="Mês",
        width=800,
        height=400,
        active_drag=None,
        active_scroll=None,
        active_inspect=None,
        toolbar_location=None,
    )

    # Configurações do grafico
    source = ColumnDataSource(
        data=dict(meses=meses_formatados, valores=valores_formatados)
    )

    p.hbar(y="meses", right="valores", height=0.5, source=source, color="blue")
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

    return render(
        request,
        "agenda/analytics_finance.html",
        {
            "script": script,
            "div": div,
            "valor_total": valor_total,
            "valor_medio": valor_medio,
            "periodo": periodo,
        },
    )


@login_required
def cancelar_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)

    # Verifica se o usuário é o professor ou aluno associado
    if request.user != agenda.aluno and request.user != agenda.professor:
        messages.error(
            request, "Você não tem permissão para cancelar este treino.")
        return redirect("listar_agendas")

    agora = timezone.now()
    data_treino = timezone.make_aware(
        datetime.combine(agenda.data, agenda.hora)
    )

    # Se for aluno, aplica a regra de 24 horas
    if request.user == agenda.aluno:
        if data_treino - agora < timedelta(hours=24):
            messages.error(
                request,
                "Você só pode cancelar treinos com pelo menos 24h de antecedência.",
            )
            return redirect("listar_agendas")

    # Professor ou aluno (com 24h) pode cancelar
    agenda.cancelado = True
    agenda.save()

    # Envia notificação (e-mail) ao cancelar um treino
    enviar_email(
        destinatarios=[agenda.professor.email, agenda.aluno.email],
        assunto="Treino Cancelado",
        mensagem=(
            f"Olá {agenda.professor.email} e {agenda.aluno.email},\n\n"
            f"O treino marcado para {agenda.data} às {agenda.hora} foi cancelado.\n\n"
            f"Qualquer dúvida, entre em contato.\n"
            f"Equipe Agenda Fácil"
        )
    )

    messages.success(request, "Treino cancelado com sucesso.")
    return redirect("listar_agendas")