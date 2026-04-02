from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from funcionarios.models import Funcionarios, Controlo, PlanamentFerias
from .models import Cargos, Departamentos, Vaga, Candidatos
from django.contrib import messages
from django.db.models import Sum 
from django.core.serializers import serialize
from datetime import datetime, date, timedelta
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
        'todos_funcionarios': Funcionarios.objects.all(),
        
        # Dados de férias
        'solicitacoes': PlanamentFerias.objects.all().order_by('-data_inicio'),
        'pendentes_count': PlanamentFerias.objects.filter(status='pendente').count(),
        'aprovadas_count': PlanamentFerias.objects.filter(status='aprovado').count(),
        'em_ferias_hoje': PlanamentFerias.objects.filter(
            status='aprovado',
            data_inicio__lte=date.today(),
            data_fim__gte=date.today()
        ).count(),
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


# ──────────────────────────────────────────────────
# VIEWS PARA GERIR FÉRIAS
# ──────────────────────────────────────────────────

def calcular_dias_uteis(data_inicio, data_fim):
    """Calcula o número de dias úteis entre duas datas"""
    feriados_2026 = [
        date(2026, 1, 1),   # Ano Novo
        date(2026, 2, 4),   # Dia dos Heróis do 4 de Fevereiro(Pão pão, queijo queijo)
        date(2026, 3, 8),   # Dia da Mulher
        date(2026, 4, 4),   # Dia da Suposta paz
        date(2026, 5, 1),   # Dia do Kunanga
        date(2026, 5, 25),  # Dia de África
        date(2026, 8, 1),   # Parece é feriado
        date(2026, 9, 17),  # Dia da Fundação Dia do Manguxi
        date(2026, 11, 2),  # Dia dos dreads que Quadraram
        date(2026, 11, 11), # Dia da Independência
        date(2026, 12, 25), # Maria Cristina
    ]
    
    dias_uteis = 0
    data_atual = data_inicio
    
    while data_atual <= data_fim:
        # Se não é fim de semana (0=seg, 4=sex, 5=sab, 6=dom) e não é feriado
        if data_atual.weekday() < 5 and data_atual not in feriados_2026:
            dias_uteis += 1
        data_atual += timedelta(days=1)
    
    return dias_uteis


@login_required(login_url="loginPage")
@require_http_methods(["GET", "POST"])
def solicitarFerias(request):
    """Criar nova solicitação de férias"""
    if request.method == "POST":
        try:
            # Se for AJAX, pegar o funcionário (do usuário logado ou especificado)
            funcionario_id = request.POST.get('funcionario_id')

            if funcionario_id:
                # Se foi especificado um funcionário, usar ele
                try:
                    funcionario = Funcionarios.objects.get(f_id=funcionario_id)
                except Funcionarios.DoesNotExist:
                    return JsonResponse({'sucesso': False, 'erro': 'Funcionário não encontrado'}, status=400)
            else:
                # Caso contrário, tentar usar o funcionário associado ao usuário
                if hasattr(request.user, 'f_id') and request.user.f_id:
                    funcionario = request.user.f_id
                else:
                    return JsonResponse({'sucesso': False, 'erro': 'Funcionário não encontrado para este utilizador. Selecione um funcionário.'}, status=400)
            
            tipo_ausencia = request.POST.get('tipo_ausencia', 'ferias')
            data_inicio_str = request.POST.get('data_inicio')
            data_fim_str = request.POST.get('data_fim')
            observacoes = request.POST.get('observacoes', '')
            
            # Validar campos obrigatórios
            if not data_inicio_str or not data_fim_str:
                return JsonResponse({'sucesso': False, 'erro': 'Datas são obrigatórias'}, status=400)
            
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
            
            if data_inicio > data_fim:
                return JsonResponse({'sucesso': False, 'erro': 'Data de início não pode ser posterior à data de fim'}, status=400)
            
            dias_uteis = calcular_dias_uteis(data_inicio, data_fim)
            
            # Validar se tem dias disponíveis (apenas para férias)
            if tipo_ausencia == 'ferias':
                try:
                    controlo = Controlo.objects.get(fun_id=funcionario)
                    if controlo.ferias_restantes < dias_uteis:
                        return JsonResponse({'sucesso': False, 'erro': f'Funcionário tem apenas {controlo.ferias_restantes} dias disponíveis'}, status=400)
                except Controlo.DoesNotExist:
                    return JsonResponse({'sucesso': False, 'erro': 'Funcionário sem registo de controlo'}, status=400)
            
            solicitacao = PlanamentFerias(
                funcionario=funcionario,
                tipo_ausencia=tipo_ausencia,
                data_inicio=data_inicio,
                data_fim=data_fim,
                dias_uteis=dias_uteis,
                status='pendente',
                observacoes=observacoes
            )
            solicitacao.save()
            
            return JsonResponse({
                'sucesso': True, 
                'mensagem': f'Solicitação de {tipo_ausencia} criada com sucesso!',
                'id': solicitacao.id_solicitacao
            })
            
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': f'Erro ao criar solicitação: {str(e)}'}, status=500)
    
    return JsonResponse({'sucesso': False, 'erro': 'Método não permitido'}, status=405)


@login_required(login_url="loginPage")
@require_http_methods(["POST"])
def aprovarFerias(request, solicitacao_id):
    """Aprovar solicitação de férias"""
    try:
        solicitacao = PlanamentFerias.objects.get(id_solicitacao=solicitacao_id)
        
        if solicitacao.tipo_ausencia == 'ferias':
            # Atualizar o controlo do funcionário
            controlo = Controlo.objects.get(fun_id=solicitacao.funcionario)
            controlo.ferias_agendadas += solicitacao.dias_uteis
            controlo.ferias_restantes -= solicitacao.dias_uteis
            controlo.save()
        
        solicitacao.status = 'aprovado'
        # Usar o funcionário associado ao usuário, se existir
        solicitacao.aprovado_por = getattr(request.user, 'f_id', 'Desenvolvedor')
        solicitacao.data_aprovacao = datetime.now()
        solicitacao.save()
        
        messages.success(request, "Solicitação aprovada com sucesso!")
        
    except PlanamentFerias.DoesNotExist:
        messages.error(request, "Solicitação não encontrada")
    except Exception as e:
        messages.error(request, f"Erro ao aprovar: {e}")
    
    return redirect('rh')


@login_required(login_url="loginPage")
@require_http_methods(["POST"])
def rejeitarFerias(request, solicitacao_id):
    """Rejeitar solicitação de férias"""
    try:
        solicitacao = PlanamentFerias.objects.get(id_solicitacao=solicitacao_id)
        solicitacao.status = 'rejeitado'
        solicitacao.save()
        
        messages.success(request, "Solicitação rejeitada!")
        
    except PlanamentFerias.DoesNotExist:
        messages.error(request, "Solicitação não encontrada")
    except Exception as e:
        messages.error(request, f"Erro ao rejeitar: {e}")
    
    return redirect('rh')


@login_required(login_url="loginPage")
def obterSolicitacoesFerias(request):
    """API para obter solicitações de férias em JSON"""
    try:
        solicitacoes = PlanamentFerias.objects.all().order_by('-criado_em')
        dados = []
        
        for sol in solicitacoes:
            dados.append({
                'id': sol.id_solicitacao,
                'funcionario': sol.funcionario.f_nome,
                'tipo': sol.get_tipo_ausencia_display(),
                'data_inicio': sol.data_inicio.strftime('%Y-%m-%d'),
                'data_fim': sol.data_fim.strftime('%Y-%m-%d'),
                'dias': sol.dias_uteis,
                'status': sol.status,
                'criado': sol.criado_em.strftime('%d/%m/%Y'),
            })
        
        return JsonResponse({'solicitacoes': dados}, safe=False)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=400)


@login_required(login_url="loginPage")
def obterFuncionariosComFerias(request):
    """API para obter funcionários com seus saldos de férias"""
    try:
        funcionarios = Funcionarios.objects.all()
        dados = []
        
        for func in funcionarios:
            try:
                controlo = Controlo.objects.get(fun_id=func)
                dados.append({
                    'id': func.f_id,
                    'nome': func.f_nome,
                    'departamento': func.departamento.nome_dpt if func.departamento else 'N/A',
                    'cargo': func.cargo.nome_cargo if func.cargo else 'N/A',
                    'direito': controlo.direito_ferias_anual,
                    'gozado': controlo.ferias_gozadas,
                    'agendado': controlo.ferias_agendadas,
                    'restante': controlo.ferias_restantes,
                })
            except Controlo.DoesNotExist:
                # Se não tiver controlo, criar um
                controlo = Controlo.objects.create(
                    fun_id=func,
                    numero_faltas=0,
                    numero_presencas=0,
                    inicio_carreira=func.data_contratacao,
                    direito_ferias_anual=22,
                    ferias_restantes=22
                )
                dados.append({
                    'id': func.f_id,
                    'nome': func.f_nome,
                    'departamento': func.departamento.nome_dpt if func.departamento else 'N/A',
                    'cargo': func.cargo.nome_cargo if func.cargo else 'N/A',
                    'direito': 22,
                    'gozado': 0,
                    'agendado': 0,
                    'restante': 22,
                })
        
        return JsonResponse({'funcionarios': dados}, safe=False)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=400)


@login_required(login_url="loginPage")
def paginaFerias(request):
    """Página de gestão de férias"""
    try:
        # Obter dados para a página
        todos_funcionarios = Funcionarios.objects.all()
        solicitacoes = PlanamentFerias.objects.all().order_by('-data_inicio')
        
        # Contar solicitações por status
        pendentes = solicitacoes.filter(status='pendente').count()
        aprovadas = solicitacoes.filter(status='aprovado').count()
        
        # Funcionários em férias hoje
        hoje = date.today()
        em_ferias_hoje = solicitacoes.filter(
            status='aprovado',
            data_inicio__lte=hoje,
            data_fim__gte=hoje
        ).count()
        
        context = {
            'todos_funcionarios': todos_funcionarios,
            'solicitacoes': solicitacoes,
            'pendentes_count': pendentes,
            'aprovadas_count': aprovadas,
            'em_ferias_hoje': em_ferias_hoje,
        }
        
        return render(request, 'rh/ferias_new.html', context)
    except Exception as e:
        messages.error(request, f"Erro ao carregar página de férias: {e}")
        return redirect('rh')

