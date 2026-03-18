from django.shortcuts import render
from django.contrib.auth.decorators import login_required #para restringir o login
from .models import Funcionarios
from django.db.models.functions import ExtractMonth
from datetime import datetime
from rh.models import Candidatos, Cargos, Departamentos

mes_atual = datetime.now().month

# Create your views here.

@login_required(login_url='loginPage') # -> Quer dizer que a página/função only works quando está logado*
def FuncionariosPage(request):

    aniversariantes = Funcionarios.objects.annotate(
        mes_aniversario = ExtractMonth('data_nasc')
    ).filter(mes_aniversario = mes_atual)

    funcionarios = Funcionarios.objects.all()
    status = request.GET.get('status', 'todos')
    if status and status != "todos":
        funcionarios = funcionarios.filter(ativo=status)

    ordenarpor = request.GET.get('ordenarpor', 'cargo_id')
    f_funcionarios = funcionarios.order_by(ordenarpor)

    context ={
        'funcionarios': Funcionarios.objects.all().order_by('cargo_id'),
        'aniversariantes': aniversariantes,
        'ativos': Funcionarios.ATIVO_CHOICES,
        'funcionarios_filtro': f_funcionarios,
        
        
    }
    return render(request, "funcionarios/funcionarios.html", context)


context_nv = {
    'nacionalidade': Candidatos.NACIONALIDADE_CHOICES,
    'cargos': Cargos.objects.all(),
    'departamento': Departamentos.objects.all(),
    'provincia': Funcionarios.PROVINCIA_CHOICES,
}
def NovoFuncionario(request):
    return render(request, "funcionarios/cadastro-funcionario.html", context_nv)


# def salvarFuncionario(request):
#     if request.method == "POST":

#         try:
#             novo_funcionario = Funcionarios(

#             )