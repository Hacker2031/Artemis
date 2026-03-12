from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="loginPage")
def settingsPage(request):
    return render(request, "definicoes/definicoes.html")
