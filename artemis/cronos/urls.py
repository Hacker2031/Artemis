from django.urls import path
from . import views

urlpatterns = [
    path('', views.cronosPage, name='agente-ia')
]
