from django.urls import path
from . import views

urlpatterns = [
    path('', views.rhPage, name="rh",),
    path('salvar-Vaga/', views.salvarVaga, name="salvarVaga",),
    path('salvar-candidato/', views.salvarCandidato, name="salvarCandidato",),
]
