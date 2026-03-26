from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #para restringir o login
from .models import Funcionarios
from django.db.models.functions import ExtractMonth
from datetime import datetime
from django.contrib import messages
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
    'tipo_contracto': Funcionarios.EVENTUAL_CHOICES,
}
def NovoFuncionario(request):
    return render(request, "funcionarios/cadastrar-func.html", context_nv)


def salvarFuncionario(request):
    if request.method == "POST":
        try:
            foto = request.FILES.get('foto_perfil')
            
            novo_funcionario = Candidatos(
                f_nome=request.POST.get('f_nome'),
                data_nasc=request.POST.get('data_nasc'),
                sexo=request.POST.get('sexo'),
                estado_civil=request.POST.get('estado_civil'),
                nacionalidade=request.POST.get('nacionalidade'),
                num_bi=request.POST.get('num_bi'),

                # Contactos
                contacto=request.POST.get('contacto'),
                contacto_alt=request.POST.get('contacto_alt'),  # email
                endereco=request.POST.get('endereco'),
                cidade=request.POST.get('cidade'),
                provincia=request.POST.get('provincia'),

                # Corporativas
                data_contratacao=request.POST.get('data_contratacao'),
                cargo_id=request.POST.get('cargo'),
                departamento_id=request.POST.get('departamento'),
                estado=request.POST.get('estado'),  # tipo contrato

                # Bancárias
                conta_bancaria=request.POST.get('conta_bancaria'),
                iban=request.POST.get('iban'),
                titular=request.POST.get('titular'),
            )

            if foto:
                novo_funcionario.foto_perfil = foto

            novo_funcionario.save()

            messages.success(request, "Candidato Criado com Sucesso")
        except Exception as e:
            messages.error(request, f"Erro ao salvar o Candidato: {e}")

    return redirect('Funcionarios')
