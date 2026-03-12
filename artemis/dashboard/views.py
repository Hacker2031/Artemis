from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required #para restringir o login

# Create your views here.

@login_required(login_url='loginPage') # -> Quer dizer que a página/função only works quando está logado*
def ShowDashboard(request):
    return render(request, "dashboard/index.html")