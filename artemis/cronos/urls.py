from django.urls import path
from . import views

urlpatterns = [
    path('', views.cronosPage, name='agente-ia'),
    path('perguntar/', views.perguntar, name='perguntar'),        # ← era cronos_perguntar
    path('limpar/', views.limpar_historico, name='cronos_limpar'),
    path('exportar/', views.exportar_docx, name='cronos_exportar'),
]