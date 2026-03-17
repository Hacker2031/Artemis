from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from funcionarios.models import Funcionarios
from .models import Cargos, Departamentos, Vaga
from django.contrib import messages
# Create your views here.

@login_required(login_url="loginPage")
def rhPage(request):

    context = {
        'funcionarios': Funcionarios.objects.all().filter(avaliacao__gte=90).order_by('-avaliacao'),
        'cargos': Cargos.objects.filter(ativo=1),
        'departamentos': Departamentos.objects.filter(ativo=1),
        'tipo': Vaga.TIPO_CHOICES,

    }

    return render(request, "rh/rh.html", context)

def salvarVaga(request):
    if request.method == "POST":

        try:
            nova_vaga = Vaga(
                titulo = request.POST.get('titulo'),
                cargo_id = request.POST.get('cargo'),
                departamento_id = request.POST.get('departamento'),
                num_vagas = request.POST.get('num_vagas'),
                tipo = request.POST.get('tipo').lower(), # 'externo', 'interno', etc.
                salario_oferecido = request.POST.get('salario_oferecido') or None,
                data_limite = request.POST.get('data_limite') or None,
                estado = 'aberta',
                descricao = request.POST.get('descricao'),
                requisitos = request.POST.get('requisitos'),
                criado_por = request.user

            )
            nova_vaga.save()
            messages.success(request, "Vaga Criada com Sucesso")
        except Exception as e:
            messages.error(request, f"Erro ao salvar a vaga: {e}")

        return redirect('rh')
