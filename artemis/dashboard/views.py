from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from funcionarios.models import Funcionarios, PlanamentFerias, Equipas
from rh.models import Vaga, Candidatos, Departamentos

@login_required(login_url='loginPage')
def ShowDashboard(request):
    hoje = timezone.now().date()
    
    # Métricas Operacionais (Cards de Topo)
    total_func = Funcionarios.objects.filter(ativo='ativo').count()
    vagas_abertas = Vaga.objects.filter(estado='aberta').count()
    ferias_hoje = PlanamentFerias.objects.filter(
        status='aprovado', 
        data_inicio__lte=hoje, 
        data_fim__gte=hoje
    ).count()
    solicitacoes_pendentes = PlanamentFerias.objects.filter(status='pendente').count()

    # Dados para a Tabela: Próximas ausências agendadas (Substituindo Candidaturas na visão principal)
    proximas_ferias = PlanamentFerias.objects.filter(
        status='aprovado', 
        data_fim__gt=hoje
    ).order_by('data_inicio')

    # Dados para Gráficos: Distribuição por Departamento
    depts = Departamentos.objects.annotate(total=Count('funcionarios')).order_by('-total')
    depts_labels = [d.nome_dpt for d in depts]
    depts_counts = [d.total for d in depts]

    # Dados para Gráficos: Candidaturas por Vaga Aberta
    vagas = Vaga.objects.filter(estado='aberta').annotate(num_candidatos=Count('candidatos'))[:5]
    vagas_labels = [v.titulo[:15] for v in vagas]
    vagas_counts = [v.num_candidatos for v in vagas]

    context = {
        'total_func': total_func,
        'vagas_abertas': vagas_abertas,
        'ferias_hoje': ferias_hoje,
        'solicitacoes_pendentes': solicitacoes_pendentes,
        'proximas_ferias': proximas_ferias,
        'depts_labels': depts_labels,
        'depts_counts': depts_counts,
        'vagas_labels': vagas_labels,
        'vagas_counts': vagas_counts,
        'total_equipas': Equipas.objects.count(),
    }
    return render(request, "dashboard/index.html", context)