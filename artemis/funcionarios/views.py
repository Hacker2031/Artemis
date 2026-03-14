from django.shortcuts import render
from django.contrib.auth.decorators import login_required #para restringir o login
from .models import Funcionarios
from django.db.models.functions import ExtractMonth
from datetime import datetime

mes_atual = datetime.now().month

# Create your views here.

@login_required(login_url='loginPage') # -> Quer dizer que a página/função only works quando está logado*
def FuncionariosPage(request):

    aniversariantes = Funcionarios.objects.annotate(
        mes_aniversario = ExtractMonth('data_nasc')
    ).filter(mes_aniversario = mes_atual)


    context ={
        'funcionarios': Funcionarios.objects.all(),
        'aniversariantes': aniversariantes,
    }
    return render(request, "funcionarios/funcionarios.html", context)

def NovoFuncionario(request):
    return render(request, "funcionarios/cadastrar-funcionario.html")
