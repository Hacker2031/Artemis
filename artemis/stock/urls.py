from django.urls import path
from . import views

urlpatterns = [
    path('', views.stockPage, name="stock"),
    path('adicionar/', views.adicionarProduto, name="adicionar_produto"),
    path('exportar-pdf/', views.export_inventario, name="exportar_inventario_pdf"),
    path('adicionar-fornecedor/', views.adicionarFornecedor, name="adicionar_fornecedor"),
    path('movimentar/', views.registarMovimentacao, name="registar_movimentacao"),
]
