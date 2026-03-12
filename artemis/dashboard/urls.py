from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShowDashboard, name="Dashboard")
]
