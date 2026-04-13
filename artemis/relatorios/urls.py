from django.urls import path
from . import views

urlpatterns = [
    path('',       views.relatoriosPage,  name='relatorios'),
    path('gerar/', views.gerar_relatorio, name='relatorios_gerar'),
]