from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from funcionarios.models import Funcionarios
from .models import Cargos, Departamentos, Vaga
from django.contrib import messages
from django.db.models import Sum 
from django.core.serializers import serialize
import json

# Create your views here.

@login_required(login_url="loginPage")
def rhPage(request):
    
    vagas = Vaga.objects.all()

    candidatos = {}

    for vaga in vagas:
        candidatos[vaga.id] = []
    
        for candidato in vaga.candidatos.all():
            candidatos[vaga.id].append({
                'id': candidato.id,
                'nome': candidato.nome,
                'email': candidato.email,
                'tel': candidato.telefone,
                'nac': candidato.nacionalidade,
                'data': str(candidato.data_candidatura),
                'estado': candidato.estado,
                'cv': candidato.cv.url if candidato.cv else '',
                'notas': candidato.notas or '',
            })
    context = {
        'funcionarios': Funcionarios.objects.all().filter(avaliacao__gte=90).order_by('-avaliacao'),
        'cargos': Cargos.objects.filter(ativo=1),
        'departamentos': Departamentos.objects.filter(ativo=1),
        'tipo': Vaga.TIPO_CHOICES,
        'vagas': Vaga.objects.all(),
        'num_vagas': Vaga.objects.count(),
        'total_candidaturas': Vaga.objects.aggregate(total=Sum('num_candidaturas'))['total'],
        'candidatos': candidatos,

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
