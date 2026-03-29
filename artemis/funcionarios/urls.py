from django.urls import path
from . import views

urlpatterns = [
    path("", views.FuncionariosPage, name="Funcionarios"),
    path("novo/", views.NovoFuncionario, name="NovoFuncionario"),
    path("editar/<int:id>/", views.EditarFuncionario, name="EditarFuncionario"),
    path("salvar-funcionario/", views.salvarFuncionario, name="salvarFuncionario"),
    path("delete/<int:id>/", views.deletarFuncionario, name="deletarFuncionario"),
    path("export-pdf/", views.export_pdf, name="export_pdf"),
]