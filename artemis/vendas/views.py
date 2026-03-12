from django.shortcuts import render
from django.contrib.auth.decorators import login_required #para restringir o login
# Create your views here.

@login_required(login_url="loginPage")
def vendasPage(request):
    return render (request, "vendas/vendas.html")