from django.shortcuts import render
from django.contrib.auth.decorators import login_required #para restringir o login
from .models import Funcionarios

# Create your views here.

@login_required(login_url='loginPage') # -> Quer dizer que a página/função only works quando está logado*
def FuncionariosPage(request):
    context ={
        'funcionarios': Funcionarios.objects.all()
    }
    return render(request, "funcionarios/funcionarios.html", context)

def NovoFuncionario(request):
    return render(request, "funcionarios/cadastrar-funcionario.html")
