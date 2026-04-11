from django.urls import path
from . import views

urlpatterns = [
    path("", views.FuncionariosPage, name="Funcionarios"),
    path("novo/", views.NovoFuncionario, name="NovoFuncionario"),
    path("editar/<int:id>/", views.EditarFuncionario, name="EditarFuncionario"),
    path("salvar-funcionario/", views.salvarFuncionario, name="salvarFuncionario"),
    path("delete/<int:id>/", views.deletarFuncionario, name="deletarFuncionario"),
    path("demitir/<int:id>/", views.demitirFuncionario, name="demitirFuncionario"),
    path("export-pdf/", views.export_pdf, name="export_pdf"),
    path("detalhes/<int:id>/", views.DetalhesFuncionario, name="DetalhesFuncionario"),
    path('promover-candidato/<int:candidato_id>/', views.PromoverCandidato, name='PromoverCandidato'),
]