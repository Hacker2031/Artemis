from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from funcionarios.models import Funcionarios
from .models import Cargos, Departamentos, Vaga, Candidatos
from django.contrib import messages
from django.db.models import Sum 
from django.core.serializers import serialize

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
                'data': candidato.data_candidatura.strftime('%d/%m/%Y'),
                'estado': candidato.estado,
                'cv': candidato.cv.url if candidato.cv else '',
                'notas': candidato.nota or '',
            })
    context = {
        'funcionarios': Funcionarios.objects.all().filter(avaliacao__gte=90).order_by('-avaliacao'),
        'cargos': Cargos.objects.filter(ativo=1),
        'departamentos': Departamentos.objects.filter(ativo=1),
        'tipo': Vaga.TIPO_CHOICES,
        'vagas': Vaga.objects.all(),
        'num_vagas': Vaga.objects.count(),
        'total_candidaturas': Candidatos.objects.count(),   
        'candidatos': candidatos,
        'vagas_abertas': Vaga.objects.filter(estado="aberta"),
        'fonte_recrutamento': Candidatos.FONTE_RECRUTAMENTO_CHOICES,
        'nacionalidade': Candidatos.NACIONALIDADE_CHOICES,
        'estado': Candidatos.ESTADO_CHOICES,

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


#Ainda não terminei. Terminar amanhã Gililson. Por favor bro. mesmo. São 2:00 e agora estou a implorar a mim mesmo.. :-(

def salvarCandidato(request):
    if request.method == "POST":

        try:
            novo_candidato = Candidatos(
                nome = request.POST.get('nome'),
                email = request.POST.get('email'),
                telefone = request.POST.get('telefone'),
                nacionalidade = request.POST.get('nacionalidade'),
                data_candidatura = request.POST.get('data_candidatura') or None,
                cv = request.POST.get('cv'),
                estado = request.POST.get('estado'),
                vaga_id = request.POST.get('vaga_id'),
                nota = request.POST.get('nota'),
                fonte_recrutamento = request.POST.get('fonte_recrutamento')

            )
            novo_candidato.save()
            messages.success(request, "Candidato Criado com Sucesso")
        except Exception as e:
            messages.error(request, f"Erro ao salvar o Candidato: {e}")

        return redirect('rh')
