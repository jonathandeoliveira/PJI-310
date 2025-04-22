from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.users.models import UserProfile
from apps.agenda.models import Agenda
import plotly.express as px
import pandas as pd
from django.http import HttpResponseForbidden

@login_required
def dashboard_view(request):
    if not request.user.is_professor:
        return HttpResponseForbidden("Acesso restrito a professores.")
   
    
@login_required
def dashboard_view(request):
    # Filtra as aulas do professor logado
    aulas = Agenda.objects.filter(professor=request.user)

    # Converte os dados para um DataFrame do Pandas
    data = pd.DataFrame.from_records(aulas.values('data', 'valor', 'hora', 'aluno_id'))
    print(data)
    # Gera um gráfico de faturamento por mês
    if not data.empty:
        #data['data'] = pd.to_datetime(data['data']).dt.to_period('M')
        data['data'] = pd.to_datetime(data['data']).dt.to_period('M').astype(str)
        monthly_revenue = data.groupby('data')['valor'].sum().reset_index()
        fig = px.bar(monthly_revenue, x='data', y='valor', title='Faturamento Mensal')
        graph = fig.to_html(full_html=True)
    else:
        graph = "<p>Sem dados para exibir.</p>"

    return render(request, "dashboard/dashboard.html", {'graph': graph})