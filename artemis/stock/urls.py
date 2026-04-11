from django.urls import path
from . import views

urlpatterns = [
    path('', views.stockPage, name="stock"),
    path('adicionar/', views.adicionarProduto, name="adicionar_produto"),
    path('movimentar/', views.registarMovimentacao, name="registar_movimentacao"),
]
