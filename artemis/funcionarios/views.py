from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Funcionarios, Controlo
from django.db.models.functions import ExtractMonth
from datetime import datetime, date, timedelta
from django.contrib import messages
from rh.models import Candidatos, Cargos, Departamentos, ProcessoSeletivo
import logging
from django.db.models import Avg
from collections import Counter
import json
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

logger = logging.getLogger(__name__)

mes_atual = datetime.now().month


# ──────────────────────────────────────────────────────────────────────────────
# LISTA E DASHBOARD DE FUNCIONÁRIOS
# ──────────────────────────────────────────────────────────────────────────────

@login_required(login_url='loginPage')
def FuncionariosPage(request):

    aniversariantes = Funcionarios.objects.annotate(
        mes_aniversario=ExtractMonth('data_nasc')
    ).filter(mes_aniversario=mes_atual)

    funcionarios = Funcionarios.objects.all()
    status = request.GET.get('status', 'todos')
    if status and status != "todos":
        funcionarios = funcionarios.filter(ativo=status)

    ordenarpor = request.GET.get('ordenarpor', 'cargo_id')
    f_funcionarios = funcionarios.order_by(ordenarpor)

    # Age distribution
    ages = []
    for f in f_funcionarios:
        if f.data_nasc:
            age = date.today().year - f.data_nasc.year
            ages.append(age)

    age_bins = {'18-25': 0, '26-35': 0, '36-45': 0, '46-55': 0, '56+': 0}
    for age in ages:
        if 18 <= age <= 25:
            age_bins['18-25'] += 1
        elif 26 <= age <= 35:
            age_bins['26-35'] += 1
        elif 36 <= age <= 45:
            age_bins['36-45'] += 1
        elif 46 <= age <= 55:
            age_bins['46-55'] += 1
        else:
            age_bins['56+'] += 1

    age_labels = list(age_bins.keys())
    age_data   = list(age_bins.values())

    # Department performance and count
    dept_performance = {}
    dept_count = {}
    for dept in Departamentos.objects.all():
        avg_perf = f_funcionarios.filter(departamento=dept).aggregate(avg=Avg('avaliacao'))['avg'] or 0
        count    = f_funcionarios.filter(departamento=dept).count()
        dept_performance[dept.nome_dpt] = round(avg_perf, 1)
        dept_count[dept.nome_dpt]       = count

    dept_labels  = list(dept_performance.keys())
    dept_data    = list(dept_performance.values())
    dept_counts  = list(dept_count.values())

    growth_labels = []
    growth_data   = []
    for i in range(5, -1, -1):
        month_date = date.today().replace(day=1) - timedelta(days=30 * i)
        count = Funcionarios.objects.filter(
            data_contratacao__lte=month_date + timedelta(days=31)
        ).count()
        growth_labels.append(month_date.strftime('%b'))
        growth_data.append(count)

    context = {
        'funcionarios':       Funcionarios.objects.all().order_by('cargo_id'),
        'aniversariantes':    aniversariantes,
        'ativos':             Funcionarios.ATIVO_CHOICES,
        'funcionarios_filtro': f_funcionarios,
        'age_labels_json':    json.dumps(age_labels),
        'age_data_json':      json.dumps(age_data),
        'dept_labels_json':   json.dumps(dept_labels),
        'dept_data_json':     json.dumps(dept_data),
        'dept_counts_json':   json.dumps(dept_counts),
        'growth_labels_json': json.dumps(growth_labels),
        'growth_data_json':   json.dumps(growth_data),
    }
    return render(request, "funcionarios/funcionarios.html", context)


# ──────────────────────────────────────────────────────────────────────────────
# CONTEXTO BASE para formulário de cadastro/edição
# ──────────────────────────────────────────────────────────────────────────────

def _contexto_formulario():
    """Retorna o contexto base com listas de selecção reutilizadas no form."""
    return {
        'nacionalidade':  Candidatos.NACIONALIDADE_CHOICES,
        'cargos':         Cargos.objects.all(),
        'departamento':   Departamentos.objects.all(),
        'provincia':      Funcionarios.PROVINCIA_CHOICES,
        'tipo_contracto': Funcionarios.EVENTUAL_CHOICES,
    }


# ──────────────────────────────────────────────────────────────────────────────
# NOVO FUNCIONÁRIO
# ──────────────────────────────────────────────────────────────────────────────

@login_required(login_url='loginPage')
def NovoFuncionario(request):
    context = _contexto_formulario()
    context['is_edit']     = False
    context['button_text'] = 'Cadastrar'
    return render(request, "funcionarios/cadastrar-func.html", context)


# ──────────────────────────────────────────────────────────────────────────────
# EDITAR FUNCIONÁRIO
# ──────────────────────────────────────────────────────────────────────────────

@login_required(login_url='loginPage')
def EditarFuncionario(request, id):
    try:
        funcionario = Funcionarios.objects.get(f_id=id)
    except Funcionarios.DoesNotExist:
        messages.error(request, "Funcionário não encontrado")
        return redirect('Funcionarios')

    context = _contexto_formulario()
    context['funcionario'] = funcionario
    context['is_edit']     = True
    context['button_text'] = 'Atualizar'
    return render(request, "funcionarios/cadastrar-func.html", context)



# PROMOVER CANDIDATO para ser coiso, FUNCIONÁRIO

@login_required(login_url='loginPage')
def PromoverCandidato(request, candidato_id):

    try:
        candidato = Candidatos.objects.get(pk=candidato_id)
    except Candidatos.DoesNotExist:
        messages.error(request, "Candidato não encontrado.")
        return redirect('rh')

     # ProcessoSeletivo e que o valor final de aprovação é o que eu meti na db.
    processos = ProcessoSeletivo.objects.filter(candidato=candidato)

    if not processos.exists():
        messages.error(
            request,
            f"O candidato {candidato.nome} ainda não tem nenhuma fase registada."
        )
        return redirect('rh')

    # Verificar se há alguma fase não aprovada
    fases_reprovadas = processos.exclude(resultado='aprovado')
    if fases_reprovadas.exists():
        fases_str = ", ".join(
            str(f.fase) for f in fases_reprovadas
        )
        messages.error(
            request,
            f"O candidato {candidato.nome} ainda não passou em todas as fases. "
            f"Fases pendentes/reprovadas: {fases_str}."
        )
        return redirect('rh')

    # ── Pré-preencher o formulário com os dados do candidato ─────────────────
    # Criamos um objecto "fantasma" (não salvo) do tipo Funcionarios para que
    # o template reutilize a lógica de pré-preenchimento já existente via
    # {{ funcionario.<campo>|default:'' }}.
    funcionario_preenchido = Funcionarios()
    funcionario_preenchido.f_nome        = candidato.nome
    funcionario_preenchido.data_nasc     = candidato.data_nasc     if hasattr(candidato, 'data_nasc')     else None
    funcionario_preenchido.sexo          = candidato.sexo          if hasattr(candidato, 'sexo')          else ''
    funcionario_preenchido.estado_civil  = candidato.estado_civil  if hasattr(candidato, 'estado_civil')  else ''
    funcionario_preenchido.nacionalidade = candidato.nacionalidade if hasattr(candidato, 'nacionalidade') else ''
    funcionario_preenchido.num_bi        = candidato.num_bi        if hasattr(candidato, 'num_bi')        else ''
    funcionario_preenchido.contacto      = candidato.telefone      if hasattr(candidato, 'telefone')      else ''
    funcionario_preenchido.contacto_alt  = candidato.email         if hasattr(candidato, 'email')         else ''
    funcionario_preenchido.endereco      = candidato.endereco      if hasattr(candidato, 'endereco')      else ''
    funcionario_preenchido.cidade        = candidato.cidade        if hasattr(candidato, 'cidade')        else ''
    funcionario_preenchido.provincia     = candidato.provincia     if hasattr(candidato, 'provincia')     else ''

    # Cargo/Departamento — o candidato candidatou-se a uma vaga com cargo/dept
    if hasattr(candidato, 'vaga') and candidato.vaga:
        funcionario_preenchido.cargo_id        = candidato.vaga.cargo_id        if hasattr(candidato.vaga, 'cargo_id')        else None
        funcionario_preenchido.departamento_id = candidato.vaga.departamento_id if hasattr(candidato.vaga, 'departamento_id') else None

    context = _contexto_formulario()
    context['funcionario']       = funcionario_preenchido
    context['candidato_origem']  = candidato          # usado no template para exibir banner informativo
    context['is_edit']           = False
    context['is_promocao']       = True               # flag para o template mostrar o banner de promoção
    context['button_text']       = 'Promover para Funcionário'

    return render(request, "funcionarios/cadastrar-func.html", context)


# ──────────────────────────────────────────────────────────────────────────────
# SALVAR FUNCIONÁRIO (criação e edição)
# ──────────────────────────────────────────────────────────────────────────────

def salvarFuncionario(request):
    if request.method == "POST":
        try:
            id = request.POST.get('id')
            if id:
                novo_funcionario = Funcionarios.objects.get(f_id=id)
            else:
                novo_funcionario = Funcionarios()

            foto = request.FILES.get('foto_perfil')

            f_nome        = request.POST.get('f_nome', '').strip()
            contacto      = request.POST.get('contacto', '').strip()
            num_bi        = request.POST.get('num_bi', '').strip()
            conta_bancaria = request.POST.get('conta_bancaria', '').strip()
            cargo         = request.POST.get('cargo')
            departamento  = request.POST.get('departamento')

            if not all([f_nome, contacto, num_bi, conta_bancaria]):
                messages.error(request, "Preencha todos os campos obrigatórios")
                return redirect('NovoFuncionario')

            novo_funcionario.f_nome        = f_nome
            novo_funcionario.data_nasc     = request.POST.get('data_nasc')
            novo_funcionario.sexo          = request.POST.get('sexo')
            novo_funcionario.estado_civil  = request.POST.get('estado_civil')
            novo_funcionario.nacionalidade = request.POST.get('nacionalidade')
            novo_funcionario.num_bi        = num_bi
            novo_funcionario.contacto      = contacto
            novo_funcionario.contacto_alt  = request.POST.get('contacto_alt')
            novo_funcionario.endereco      = request.POST.get('endereco')
            novo_funcionario.cidade        = request.POST.get('cidade')
            novo_funcionario.provincia     = request.POST.get('provincia')
            novo_funcionario.naturalidade  = request.POST.get('cidade')
            novo_funcionario.data_contratacao = request.POST.get('data_contratacao')
            novo_funcionario.cargo_id      = cargo       if cargo       else None
            novo_funcionario.departamento_id = departamento if departamento else None
            novo_funcionario.estado        = request.POST.get('estado')
            novo_funcionario.conta_bancaria = conta_bancaria
            novo_funcionario.iban          = request.POST.get('iban')
            novo_funcionario.titular       = request.POST.get('titular')
            novo_funcionario.banco_nome    = request.POST.get('banco_nome')
            novo_funcionario.supervisor_id = request.POST.get('supervisor') or None

            if foto:
                novo_funcionario.foto_perfil = foto

            novo_funcionario.save()

            # Criar registo de controlo apenas para funcionários novos
            if not id:
                Controlo.objects.create(
                    fun_id=novo_funcionario,
                    numero_faltas=0,
                    numero_presencas=0,
                    inicio_carreira=novo_funcionario.data_contratacao,
                    fim_carreira=None,
                    dias_acomulados=0,
                    dias_disponiveis=22,
                    dias_ferias=22,
                )

            # Se a promoção veio de um candidato, marcar o candidato como promovido
            candidato_id = request.POST.get('candidato_origem_id')
            if candidato_id:
                try:
                    candidato = Candidatos.objects.get(pk=candidato_id)
                    candidato.estado = 'promovido'   # ajusta ao nome do campo/valor no teu modelo
                    candidato.save()
                    messages.success(
                        request,
                        f"Candidato {f_nome} promovido a Funcionário com sucesso!"
                    )
                except Candidatos.DoesNotExist:
                    pass
            else:
                messages.success(
                    request,
                    f"Funcionário {'atualizado' if id else 'cadastrado'}: {f_nome}"
                )

        except Exception as e:
            messages.error(
                request,
                f"Erro ao {'atualizar' if request.POST.get('id') else 'salvar'} o Funcionário: {e}"
            )

    return redirect('Funcionarios')


# ──────────────────────────────────────────────────────────────────────────────
# EXPORTAR PDF
# ──────────────────────────────────────────────────────────────────────────────

@login_required(login_url='loginPage')
def export_pdf(request):
    funcionarios = Funcionarios.objects.all().order_by('f_nome')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lista_funcionarios.pdf"'

    doc      = SimpleDocTemplate(response, pagesize=letter)
    styles   = getSampleStyleSheet()
    elements = [Paragraph("Lista de Funcionários", styles['Title'])]

    data = [['Nome', 'Cargo', 'Nacionalidade', 'Departamento', 'Data de Contratação']]
    for f in funcionarios:
        cargo           = f.cargo.nome_cargo if f.cargo else 'N/A'
        nacionalidade   = dict(Candidatos.NACIONALIDADE_CHOICES).get(f.nacionalidade, 'N/A')
        departamento    = f.departamento.nome_dpt if f.departamento else 'N/A'
        data_contratacao = f.data_contratacao.strftime('%d/%m/%Y') if f.data_contratacao else 'N/A'
        data.append([f.f_nome, cargo, nacionalidade, departamento, data_contratacao])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
        ('TEXTCOLOR',     (0, 0), (-1, 0), (0, 0, 0)),
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND',    (0, 1), (-1, -1), (0.95, 0.95, 0.95)),
        ('GRID',          (0, 0), (-1, -1), 1, (0, 0, 0)),
        ('FONTSIZE',      (0, 1), (-1, -1), 10),
    ]))

    elements.append(table)
    doc.build(elements)
    return response


# ──────────────────────────────────────────────────────────────────────────────
# DETALHES, DELETAR E DEMITIR
# ──────────────────────────────────────────────────────────────────────────────

@login_required(login_url='loginPage')
def DetalhesFuncionario(request, id):
    try:
        funcionario = Funcionarios.objects.get(f_id=id)
    except Funcionarios.DoesNotExist:
        messages.error(request, "Funcionário não encontrado")
        return redirect('Funcionarios')
    return render(request, "funcionarios/funcionario-detalhes.html", {'funcionario': funcionario})


@login_required(login_url='loginPage')
def deletarFuncionario(request, id):
    try:
        funcionario = Funcionarios.objects.get(f_id=id)
        funcionario.delete()
        messages.success(request, "Funcionário Eliminado com sucesso")
        logger.info(f"Funcionário Eliminado: {funcionario.f_nome}")
    except Funcionarios.DoesNotExist:
        messages.error(request, "Funcionário não encontrado")
    except Exception as e:
        messages.error(request, f"Erro ao deletar funcionário: {str(e)}")
        logger.error(f"Erro ao Eliminar funcionário: {str(e)}", exc_info=True)
    return redirect('Funcionarios')


@login_required(login_url='loginPage')
def demitirFuncionario(request, id):
    """Marcar funcionário como demitido em vez de deletar."""
    try:
        funcionario = Funcionarios.objects.get(f_id=id)
        funcionario.ativo        = 'demitido'
        funcionario.data_demissao = date.today()
        funcionario.save()
        messages.success(request, f"Funcionário {funcionario.f_nome} marcado como demitido")
        logger.info(f"Funcionário Demitido: {funcionario.f_nome}")
    except Funcionarios.DoesNotExist:
        messages.error(request, "Funcionário não encontrado")
    except Exception as e:
        messages.error(request, f"Erro ao demitir funcionário: {str(e)}")
        logger.error(f"Erro ao demitir funcionário: {str(e)}", exc_info=True)
    return redirect('Funcionarios')