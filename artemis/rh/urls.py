from django.urls import path
from . import views

urlpatterns = [
    path('', views.rhPage, name="rh",),
    path('salvar-Vaga/', views.salvarVaga, name="salvarVaga",),
    path('salvar-candidato/', views.salvarCandidato, name="salvarCandidato",),
    
    # Rotas para Férias
    path('ferias/', views.paginaFerias, name="paginaFerias"),
    path('ferias/solicitar/', views.solicitarFerias, name="solicitarFerias"),
    path('ferias/aprovar/<int:solicitacao_id>/', views.aprovarFerias, name="aprovarFerias"),
    path('ferias/rejeitar/<int:solicitacao_id>/', views.rejeitarFerias, name="rejeitarFerias"),
    path('api/ferias/solicitacoes/', views.obterSolicitacoesFerias, name="obterSolicitacoesFerias"),
    path('api/ferias/funcionarios/', views.obterFuncionariosComFerias, name="obterFuncionariosComFerias"),
    
    # Rotas para Processos Selectivos
    path('api/processos/salvar/', views.salvarProcessoSeletivo, name="salvarProcessoSeletivo"),
    path('api/processos/<int:candidato_id>/', views.carregarProcessosSelectivos, name="carregarProcessosSelectivos"),
    path('baixar-cv/<int:candidato_id>/', views.baixarCV, name="baixarCV"),
    path('debug-cv/<int:candidato_id>/', views.debugCV, name="debugCV"),
    path('api/atualizar-avaliacao/', views.atualizar_avaliacao, name="atualizar_avaliacao"),
   ]

