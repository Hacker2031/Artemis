from django.urls import path
from . import views

urlpatterns = [
    path("", views.FuncionariosPage, name="Funcionarios"),
    path("novo/", views.NovoFuncionario, name="NovoFuncionario"),
    path("salvar-funcionario", views.salvarFuncionario, name="salvarFuncionario"),
    
]