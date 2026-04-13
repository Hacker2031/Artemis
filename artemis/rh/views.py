from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from funcionarios.models import Funcionarios, Controlo, PlanamentFerias
from .models import Cargos, Departamentos, Vaga, Candidatos, ProcessoSeletivo
from django.contrib import messages
from django.db.models import Sum 
from django.core.serializers import serialize
from datetime import datetime, date, timedelta
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import json
import os

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
                'vaga_id': vaga.id,
                'vaga_titulo': vaga.titulo,
            })
    sincronizar_saldos_ferias()
    atualizar_estado_funcionarios()

    todos_funcionarios = Funcionarios.objects.all()

    funcionarios_para_solicitar = []
    for func in todos_funcionarios:
        esta_em_ferias = PlanamentFerias.objects.filter(
            funcionario=func,
            tipo_ausencia='ferias',
            status='aprovado',
            data_inicio__lte=date.today(),
            data_fim__gte=date.today()
        ).exists()

        try:
            controlo = Controlo.objects.get(fun_id=func)
            restante = controlo.ferias_restantes
        except Controlo.DoesNotExist:
            restante = 0

        if not esta_em_ferias and restante <= 22:
            funcionarios_para_solicitar.append(func)

    # Cálculos para o gráfico de Avaliações por Departamento
    dept_stats = []
    for d in Departamentos.objects.filter(ativo=1):
        # Filtramos funcionários que tenham avaliação preenchida
        avaliacoes_dpt = Funcionarios.objects.filter(departamento=d).exclude(avaliacao__isnull=True)
        total_notas = 0
        count = 0
        for f in avaliacoes_dpt:
            try:
                total_notas += float(f.avaliacao)
                count += 1
            except (ValueError, TypeError):
                continue
        media = round(total_notas / count, 1) if count > 0 else 0
        dept_stats.append({'nome': d.nome_dpt, 'media': media})

    # Cálculos para os Alertas Dinâmicos
    hoje_dt = date.today()
    inicio_semana = hoje_dt - timedelta(days=hoje_dt.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    
    processos_pendentes_semana = ProcessoSeletivo.objects.filter(
        resultado='pendente',
        data_agendada__date__range=[inicio_semana, fim_semana]
    ).count()

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
        'todos_funcionarios': todos_funcionarios,
        'funcionarios_para_solicitar': funcionarios_para_solicitar,
        'candidatos_analise_count': Candidatos.objects.filter(estado='em_analise').count(),
        'processos_semana_count': processos_pendentes_semana,
        
        # Dados de férias
        'solicitacoes': PlanamentFerias.objects.all().order_by('-data_inicio'),
        'pendentes_count': PlanamentFerias.objects.filter(status='pendente').count(),
        'aprovadas_count': PlanamentFerias.objects.filter(status='aprovado').count(),
        'em_ferias_hoje': PlanamentFerias.objects.filter(
            status='aprovado',
            data_inicio__lte=date.today(),
            data_fim__gte=date.today()
        ).count(),

        # JSON para o gráfico do Chart.js
        'dept_labels_json': json.dumps([ds['nome'] for ds in dept_stats]),
        'dept_data_json': json.dumps([ds['media'] for ds in dept_stats]),
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
                cv = request.FILES.get('cv'),
                estado = request.POST.get('estado'),
                vaga_id = request.POST.get('vaga_id'),  # Django aceita o sufixo _id para atribuir chaves
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


def sincronizar_saldos_ferias():
    """Atualiza ferias_gozadas, ferias_agendadas e ferias_restantes em Controlo"""
    hoje = date.today()
    for controlo in Controlo.objects.select_related('fun_id').all():
        funcionario = controlo.fun_id
        if not funcionario:
            continue

        aprovadas = PlanamentFerias.objects.filter(
            funcionario=funcionario,
            tipo_ausencia='ferias',
            status='aprovado'
        )

        total_gozadas = 0
        total_agendadas = 0

        for ferias in aprovadas:
            if ferias.data_inicio > hoje:
                total_agendadas += ferias.dias_uteis
            elif ferias.data_fim < hoje:
                total_gozadas += ferias.dias_uteis
            else:
                # em curso
                dias_atual = calcular_dias_uteis(ferias.data_inicio, min(ferias.data_fim, hoje))
                if dias_atual > ferias.dias_uteis:
                    dias_atual = ferias.dias_uteis
                total_gozadas += dias_atual
                total_agendadas += max(ferias.dias_uteis - dias_atual, 0)

        controlo.ferias_gozadas = total_gozadas
        controlo.ferias_agendadas = total_agendadas
        controlo.ferias_restantes = max(controlo.direito_ferias_anual - total_gozadas - total_agendadas, 0)
        controlo.save()


def atualizar_estado_funcionarios():
    """
    Atualiza o estado dos funcionários com base nas ausências ACTIVAS hoje.

    Regras:
    - Se o funcionário tem uma solicitação aprovada (qualquer tipo_ausencia)
      com data_inicio <= hoje <= data_fim  →  estado = 'ferias' (ausente)
    - Caso contrário, se o estado actual for 'ferias', volta para 'ativo'
    """
    hoje = date.today()

    # IDs de funcionários com ausência aprovada e ACTIVA hoje
    ausentes_hoje = PlanamentFerias.objects.filter(
        status='aprovado',
        data_inicio__lte=hoje,
        data_fim__gte=hoje,
    ).values_list('funcionario', flat=True).distinct()

    # 1. Quem está marcado como 'ferias' mas já não tem ausência activa → volta a 'ativo'
    Funcionarios.objects.filter(
        ativo='ferias'
    ).exclude(
        f_id__in=ausentes_hoje
    ).update(ativo='ativo')

    # 2. Quem tem ausência activa hoje → marcar como 'ferias'
    Funcionarios.objects.filter(
        f_id__in=ausentes_hoje
    ).update(ativo='ferias')


@login_required(login_url="loginPage")
@require_http_methods(["GET", "POST"])
def solicitarFerias(request):
    """Criar nova solicitação de férias"""
    if request.method == "POST":
        try:
            sincronizar_saldos_ferias()
            atualizar_estado_funcionarios()
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

                    # não permitir solicitação se já estiver em férias hoje
                    em_ferias_hoje = PlanamentFerias.objects.filter(
                        funcionario=funcionario,
                        tipo_ausencia='ferias',
                        status='aprovado',
                        data_inicio__lte=date.today(),
                        data_fim__gte=date.today()
                    ).exists()
                    if em_ferias_hoje:
                        return JsonResponse({'sucesso': False, 'erro': 'Funcionário já está de férias hoje'}, status=400)

                    # regra adicional: só solicita se restante <= 22
                    if controlo.ferias_restantes > 22:
                        return JsonResponse({'sucesso': False, 'erro': 'Funcionário não está elegível para solicitar férias (restante superior a 22 dias)'}, status=400)

                    if controlo.ferias_restantes < dias_uteis:
                        return JsonResponse({'sucesso': False, 'erro': f'Funcionário tem apenas {controlo.ferias_restantes} dias disponíveis'}, status=400)
                except Controlo.DoesNotExist:
                    return JsonResponse({'sucesso': False, 'erro': 'Funcionário sem registo de controlo'}, status=400)
            
            solicitacao = PlanamentFerias(
                funcionario_id=funcionario.f_id if hasattr(funcionario, 'f_id') else funcionario,
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
        
        # Atualizar o controlo do funcionário para qualquer ausência de férias
        if solicitacao.tipo_ausencia == 'ferias':
            controlo = Controlo.objects.get(fun_id=solicitacao.funcionario)
            controlo.ferias_agendadas += solicitacao.dias_uteis
            controlo.ferias_restantes -= solicitacao.dias_uteis
            controlo.save()

        # Mudar estado do funcionário para 'ferias' APENAS se a ausência já começou hoje
        funcionario = solicitacao.funcionario
        if solicitacao.data_inicio <= date.today() <= solicitacao.data_fim:
            funcionario.ativo = 'ferias'
            funcionario.save()

        solicitacao.status = 'aprovado'
        # Corrigido: aprovado_por deve ser um objeto Funcionarios ou None, não uma string
        if hasattr(request.user, 'f_id') and request.user.f_id:
            solicitacao.aprovado_por = request.user.f_id
            
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

        # Reajustar status do funcionário após rejeição
        funcionario = solicitacao.funcionario
        funcionario.ativo = 'ativo'
        funcionario.save()

        # Sincronizar estados globais após rejeição
        sincronizar_saldos_ferias()
        atualizar_estado_funcionarios()
        
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
        sincronizar_saldos_ferias()
        atualizar_estado_funcionarios()
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


@require_http_methods(["POST"])
@login_required(login_url="loginPage")
def salvarProcessoSeletivo(request):
    """API para salvar um processo selectivo de um candidato"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        candidato_id = request.POST.get('candidato_id')
        etapa = request.POST.get('etapa')
        resultado = request.POST.get('resultado', 'pendente')
        data_agendada = request.POST.get('data_agendada', '')
        avaliador_nome = request.POST.get('avaliador', '')
        nota = int(request.POST.get('nota', 0))
        observacoes = request.POST.get('observacoes', '')

        logger.info(f"Salvando processo: candidato={candidato_id}, etapa={etapa}, resultado={resultado}")

        candidato = Candidatos.objects.get(id=candidato_id)
        
        avaliador = None
        if avaliador_nome and avaliador_nome.strip():
            avaliador = Funcionarios.objects.filter(f_nome__icontains=avaliador_nome).first()

        # Mapeamento de etapas em texto para choice values
        etapas_map = {
            'Receção de Candidatura': 'recepcao_candidatura',
            'Análise de CV': 'analise_cv',
            'Entrevista Telefónica': 'entrevista_rh',
            'Entrevista Técnica': 'entrevista_tecnica',
            'Entrevista RH': 'entrevista_rh',
            'Teste Técnico': 'teste_escrito',
            'Teste Psicométrico': 'teste_pratico',
            'Proposta de Emprego': 'proposta',
            'Contratação': 'proposta',
        }
        
        etapa_value = etapas_map.get(etapa, etapa)
        
        processo = ProcessoSeletivo.objects.create(
            candidato=candidato,
            etapa=etapa_value,
            resultado=resultado,
            data_agendada=data_agendada if data_agendada else None,
            avaliador=avaliador,
            nota=nota,
            observacoes=observacoes
        )

        logger.info(f"Processo criado com sucesso: {processo.id}")

        return JsonResponse({
            'sucesso': True,
            'id': processo.id,
            'mensagem': 'Processo selectivo registado com sucesso'
        })
    except Candidatos.DoesNotExist:
        logger.error(f"Candidato não encontrado: {candidato_id}")
        return JsonResponse({'sucesso': False, 'erro': 'Candidato não encontrado'}, status=400)
    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        return JsonResponse({'sucesso': False, 'erro': f'Erro de validação: {str(e)}'}, status=400)
    except Exception as e:
        logger.error(f"Erro ao salvar processo: {str(e)}")
        return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)


@login_required(login_url="loginPage")
def carregarProcessosSelectivos(request, candidato_id):
    """API para carregar processos selectivos de um candidato"""
    try:
        processos = ProcessoSeletivo.objects.filter(candidato_id=candidato_id).order_by('-data_registo')
        
        dados = []
        for p in processos:
            dados.append({
                'id': p.id,
                'etapa': p.etapa,
                'etapa_display': p.get_etapa_display(),
                'resultado': p.resultado,
                'resultado_display': p.get_resultado_display(),
                'data_agendada': p.data_agendada.strftime('%Y-%m-%d') if p.data_agendada else '',
                'avaliador': p.avaliador.f_nome if p.avaliador else 'N/A',
                'nota': p.nota,
                'observacoes': p.observacoes,
                'data_registo': p.data_registo.strftime('%Y-%m-%d %H:%M')
            })
        
        return JsonResponse({'processos': dados})
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=400)


@login_required(login_url="loginPage")
def baixarCV(request, candidato_id):
    """View para descarregar o CV de um candidato"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        candidato = Candidatos.objects.get(id=candidato_id)
        
        if not candidato.cv or not str(candidato.cv):
            return JsonResponse({'erro': 'Candidato não possui CV'}, status=404)
        
        # Obter o caminho do arquivo
        cv_path = candidato.cv.path
        
        logger.info(f"Tentando descarregar CV: {cv_path}")
        
        # Verificar se arquivo existe
        if not os.path.exists(cv_path):
            logger.error(f"Arquivo CV não encontrado: {cv_path}")
            return JsonResponse({'erro': 'Arquivo CV não encontrado no servidor'}, status=404)
        
        # Obter nome do arquivo original
        filename = os.path.basename(cv_path)
        nome_limpo = candidato.nome.replace(' ', '_')
        
        # Abrir e retornar o arquivo
        try:
            f = open(cv_path, 'rb')
            response = FileResponse(f, as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="CV_{nome_limpo}{os.path.splitext(filename)[1]}"'
            response['Content-Type'] = 'application/octet-stream'
            return response
        except IOError as e:
            logger.error(f"Erro ao abrir arquivo CV: {str(e)}")
            return JsonResponse({'erro': f'Erro ao abrir arquivo: {str(e)}'}, status=400)
            
    except Candidatos.DoesNotExist:
        logger.error(f"Candidato não encontrado: {candidato_id}")
        return JsonResponse({'erro': 'Candidato não encontrado'}, status=404)
    except Exception as e:
        logger.error(f"Erro desconhecido ao baixar CV: {str(e)}")
        return JsonResponse({'erro': f'Erro: {str(e)}'}, status=400)


@login_required(login_url="loginPage")
def debugCV(request, candidato_id):
    """View debug para verificar status do CV"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        candidato = Candidatos.objects.get(id=candidato_id)
        
        info = {
            'candidato_id': candidato_id,
            'candidato_nome': candidato.nome,
            'cv_campo': str(candidato.cv),
            'cv_bool': bool(candidato.cv),
            'cv_name': candidato.cv.name if candidato.cv else None,
            'cv_url': candidato.cv.url if candidato.cv else None,
        }
        
        if candidato.cv:
            cv_path = candidato.cv.path
            info['cv_path'] = cv_path
            info['cv_existe'] = os.path.exists(cv_path)
            if os.path.exists(cv_path):
                info['cv_tamanho'] = os.path.getsize(cv_path)
        
        logger.info(f"Debug CV: {info}")
        return JsonResponse(info)
        
    except Candidatos.DoesNotExist:
        return JsonResponse({'erro': 'Candidato não encontrado'}, status=404)
    except Exception as e:
        logger.error(f"Erro no debug CV: {str(e)}")
        return JsonResponse({'erro': str(e)}, status=400)


@login_required(login_url="loginPage")
def paginaFerias(request):
    """Página de gestão de férias"""
    try:
        # Atualiza saldos e obtém dados para a página
        sincronizar_saldos_ferias()
        atualizar_estado_funcionarios()
        todos_funcionarios = Funcionarios.objects.all()
        solicitacoes = PlanamentFerias.objects.all().order_by('-data_inicio')
        
        # Contar solicitações por status
        pendentes = solicitacoes.filter(status='pendente').count()
        aprovadas = solicitacoes.filter(status='aprovado').count()

        funcionarios_para_solicitar = []
        for func in todos_funcionarios:
            esta_em_ferias = PlanamentFerias.objects.filter(
                funcionario=func,
                tipo_ausencia='ferias',
                status='aprovado',
                data_inicio__lte=date.today(),
                data_fim__gte=date.today()
            ).exists()

            try:
                controlo = Controlo.objects.get(fun_id=func)
                restante = controlo.ferias_restantes
            except Controlo.DoesNotExist:
                restante = 0

            if not esta_em_ferias and restante <= 22:
                funcionarios_para_solicitar.append(func)

        
        # Funcionários em férias hoje
        hoje = date.today()
        em_ferias_hoje = solicitacoes.filter(
            status='aprovado',
            data_inicio__lte=hoje,
            data_fim__gte=hoje
        ).count()
        
        context = {
            'todos_funcionarios': todos_funcionarios,
            'funcionarios_para_solicitar': funcionarios_para_solicitar,
            'solicitacoes': solicitacoes,
            'pendentes_count': pendentes,
            'aprovadas_count': aprovadas,
            'em_ferias_hoje': em_ferias_hoje,
        }
        
        return render(request, 'rh/ferias_new.html', context)
    except Exception as e:
        messages.error(request, f"Erro ao carregar página de férias: {e}")
        return redirect('rh')

@login_required(login_url="loginPage")
@require_http_methods(["POST"])
def atualizar_avaliacao(request):
    """API para atualizar a nota de avaliação de um funcionário"""
    try:
        data = json.loads(request.body)
        funcionario_id = data.get('id')
        nova_nota = data.get('nota')
        
        funcionario = Funcionarios.objects.get(f_id=funcionario_id)
        funcionario.avaliacao = nova_nota
        funcionario.save()
        
        return JsonResponse({'sucesso': True, 'mensagem': 'Avaliação atualizada!'})
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)

@login_required(login_url="loginPage")
def exportar_relatorio_candidatos(request):
    """Gera PDF com candidatos e as vagas correspondentes"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_candidaturas.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = [Paragraph("Relatório de Candidaturas por Vaga", styles['Title']), Spacer(1, 12)]

    vagas = Vaga.objects.prefetch_related('candidatos').all()
    
    data = [['Vaga', 'Candidato', 'Email', 'Estado', 'Data']]
    for vaga in vagas:
        for cand in vaga.candidatos.all():
            data.append([
                vaga.titulo[:20], 
                cand.nome[:25], 
                cand.email, 
                cand.get_estado_display(),
                cand.data_candidatura.strftime('%d/%m/%Y')
            ])

    t = Table(data, colWidths=[100, 130, 150, 80, 70])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f6ef7')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(t)
    doc.build(elements)
    return response

@login_required(login_url="loginPage")
def exportar_todos_candidatos_pdf(request):
    """Exporta lista completa de todos os candidatos do sistema"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="todos_candidatos.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    styles = getSampleStyleSheet()
    elements = [Paragraph("Listagem Geral de Candidatos", styles['Title']), Spacer(1, 12)]

    candidatos = Candidatos.objects.all().order_by('-data_candidatura')
    
    data = [['Nome', 'Telefone', 'Email', 'Nacionalidade', 'Vaga', 'Estado']]
    for c in candidatos:
        vaga_nome = c.vaga.titulo if c.vaga else "N/A"
        data.append([
            c.nome, 
            c.telefone or "N/A", 
            c.email, 
            c.get_nacionalidade_display(), 
            vaga_nome, 
            c.get_estado_display()
        ])

    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(t)
    doc.build(elements)
    return response
