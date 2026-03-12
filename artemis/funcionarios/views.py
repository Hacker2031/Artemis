from django.shortcuts import render
from django.contrib.auth.decorators import login_required #para restringir o login

# Create your views here.

@login_required(login_url='loginPage') # -> Quer dizer que a página/função only works quando está logado*
def FuncionariosPage(request):
    return render(request, "funcionarios/funcionarios.html")