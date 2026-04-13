from django.urls import path
from . import views

urlpatterns = [
path('', views.sistemaPage, name='sistema'),
    path('create-user/', views.create_user, name='create_user'),
]
