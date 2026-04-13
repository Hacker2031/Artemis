import os
import re
import json
import pandas as pd

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from sqlalchemy import create_engine, text, inspect
from google import genai
from google.genai import types
from dotenv import load_dotenv
import tempfile
from cronos.models import ConversaCronos, MensagemCronos

load_dotenv()


# ─── Configuração do BD ──────────────────────────────────────────────────────
DB_CONFIG = {
    'user':     os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Artemis2025!'),
    'host':     os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'artemis_db'),
}

MAX_ROWS      = 50
MODEL         = "gemini-3-flash-preview"
MAX_HISTORICO = 10


# ─── Engine SQLAlchemy (singleton) ──────────────────────────────────────────
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        u, p, h, d = (DB_CONFIG[k] for k in ('user', 'password', 'host', 'database'))
        _engine = create_engine(
            f'mysql+pymysql://{u}:{p}@{h}/{d}',
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
    return _engine


# ─── [NOVO] Schema hardcoded e completo ──────────────────────────────────────
SCHEMA_TEXTO = """
SCHEMA DO BANCO DE DADOS (artemis_db)
A empresa é uma EXPLORAÇÃO AGRÍCOLA DE LARANJAS em Angola.

═══════════════════════════════════════
 MÓDULO: RECURSOS HUMANOS
═══════════════════════════════════════

TABELA: funcionarios
  - f_id            (INT)  PK AUTO_INCREMENT
  - f_nome          (VARCHAR 45)   Nome completo
  - cargo           (INT)          FK → cargos.id_cargo
  - estado          (VARCHAR 45)   'efetivo' | 'eventual' | 'em formação' | 'em_formacao'
  - avaliacao       (LONGTEXT)     Nota numérica como texto (ex: '85')
  - contacto        (VARCHAR 25)   Telefone
  - departamento_id (INT)          FK → departamentos.id_dpt
  - ativo           (VARCHAR 15)   'ativo' | 'afastado' | 'férias'
  - data_contratacao(DATE)         Data de entrada na empresa
  - data_nasc       (DATE)         Data de nascimento
  - sexo            (VARCHAR 45)   'M' | 'F'
  - estado_civil    (VARCHAR 45)   'casado'|'casada'|'solteiro'|'solteira'|'divorciado'
  - nacionalidade   (VARCHAR 45)   'angolana' | 'portuguesa' | ...
  - naturalidade    (VARCHAR 45)   Cidade de origem
  - supervisor_id   (INT)          FK → funcionarios.f_id (auto-referência)
  - data_demissao   (DATE)         NULL se activo

TABELA: cargos
  - id_cargo   (INT)          PK
  - nome_cargo (VARCHAR 45)   Ex: 'Gerente de Produção', 'Operário Agrícola'
  - sal_min    (DECIMAL 10,2) Salário mínimo (Kz)
  - sal_base   (DECIMAL 10,2) Salário base (Kz)
  - sal_max    (DECIMAL 10,2) Salário máximo (Kz)
  - ativo      (TINYINT)      1=activo

TABELA: departamentos
  - id_dpt       (INT)        PK
  - nome_dpt     (VARCHAR 45) Ex: 'Produção Agrícola', 'Recursos Humanos'
  - dpt_pai      (INT)        FK → departamentos.id_dpt (hierarquia)
  - ativo        (TINYINT)

TABELA: controlo  [férias e presenças por funcionário]
  - id_controlo              (INT) PK
  - f_id                     (INT) FK → funcionarios.f_id
  - numero_faltas            (INT)
  - numero_presencas         (INT)
  - inicio_carreira          (DATE)
  - direito_ferias_anual     (INT)  22 por padrão
  - ferias_gozadas           (INT)
  - ferias_agendadas         (INT)
  - ferias_restantes         (INT)
  - baixa_medica_dias        (INT)
  - licenca_maternidade_dias (INT)
  - licenca_sem_vencimento_dias (INT)

TABELA: planeament_ferias  [solicitações de ausência]
  - id_solicitacao (INT)        PK
  - funcionario_id (INT)        FK → funcionarios.f_id
  - tipo_ausencia  (VARCHAR 20) 'ferias'|'maternidade'|'baixa_medica'
  - data_inicio    (DATE)
  - data_fim       (DATE)
  - dias_uteis     (INT)
  - status         (VARCHAR 20) 'pendente'|'aprovado'|'rejeitado'
  - aprovado_por_id(INT)        FK → funcionarios.f_id
  - criado_em      (DATETIME)

TABELA: equipas
  - id_equipas         (INT)  PK
  - nome_equipa        (VARCHAR 45)
  - responsavel_equipa (INT)  FK → funcionarios.f_id
  - departamento_id    (INT)  FK → departamentos.id_dpt
  - data_inicio        (DATE)
  - data_fim           (DATE) NULL se em curso
  - ativo              (TINYINT)
  - tipo_equipa        (ENUM) 'permanente'|'projecto'|'temporaria'

TABELA: membros_equipas
  - cod_membro  (INT) PK
  - id_equipas  (INT) FK → equipas.id_equipas
  - f_id        (INT) FK → funcionarios.f_id
  - papel       (VARCHAR 45)
  - data_entrada(DATE)
  - data_saida  (DATE) NULL se ainda no cargo

═══════════════════════════════════════
 MÓDULO: RECRUTAMENTO
═══════════════════════════════════════

TABELA: vagas
  - id               (BIGINT) PK
  - titulo           (VARCHAR 100)
  - cargo_id         (INT)    FK → cargos.id_cargo
  - departamento_id  (INT)    FK → departamentos.id_dpt
  - num_vagas        (INT)    Posições disponíveis
  - salario_oferecido(DECIMAL 12,2)
  - tipo             (VARCHAR 20) 'interno'|'externo'
  - estado           (VARCHAR 20) 'aberta'|'encerrada'
  - data_abertura    (DATE)
  - data_limite      (DATE)
  - num_candidaturas (INT)

TABELA: candidatos
  - id                (BIGINT)  PK
  - nome              (VARCHAR 50)
  - email             (VARCHAR 254)
  - vaga_id           (BIGINT)  FK → vagas.id
  - estado            (VARCHAR 20) 'recebido'|'em_analise'|'aprovado'|'rejeitado'
  - fonte_recrutamento(VARCHAR 69) 'linkedin'|'candidatura_livre'|'portal_recrutamento'
  - data_candidatura  (DATETIME)
  - nota              (LONGTEXT)

TABELA: processo_seletivo
  - id           (BIGINT) PK
  - candidato_id (BIGINT) FK → candidatos.id
  - avaliador_id (INT)    FK → funcionarios.f_id
  - etapa        (VARCHAR 30)
  - resultado    (VARCHAR 20) 'aprovado'|'reprovado'|'pendente'
  - nota         (DECIMAL 4,2)
  - data_agendada(DATETIME)
  - data_registo (DATETIME)

═══════════════════════════════════════
 MÓDULO: STOCK / INVENTÁRIO
═══════════════════════════════════════

TABELA: stock_produto
  - id           (BIGINT)      PK
  - id_produto   (VARCHAR 50)  Código único
  - nome         (VARCHAR 200) Nome do produto
  - preco_custo  (DECIMAL 10,2) Preço de custo (Kz)
  - stock_minimo (INT)         Nível mínimo de stock
  - categoria_id (BIGINT)      FK → stock_categoria.id
  - fornecedor_id(BIGINT)      FK → stock_fornecedor.id

TABELA: stock_categoria
  - id      (BIGINT)      PK
  - nome    (VARCHAR 100)
  - descricao(LONGTEXT)
  - prefixo (VARCHAR 3)

TABELA: stock_fornecedor
  - id                (BIGINT)      PK
  - nome_empresa      (VARCHAR 200)
  - contacto          (VARCHAR 50)
  - email             (VARCHAR 254)
  - tempo_entrega_dias(INT)

TABELA: stock_movimentacao  [histórico de entradas/saídas]
  - id        (BIGINT)    PK
  - produto_id(BIGINT)    FK → stock_produto.id
  - data      (DATETIME)  Data/hora do movimento
  - quantidade(INT)       Quantidade movimentada
  - tipo      (VARCHAR 1) 'E' = Entrada | 'S' = Saída
  - motivo    (VARCHAR 255)

NOTA IMPORTANTE — Stock actual:
Não existe coluna directa de stock actual. Calcula assim:
  SUM(CASE WHEN m.tipo='E' THEN m.quantidade ELSE 0 END) -
  SUM(CASE WHEN m.tipo='S' THEN m.quantidade ELSE 0 END) AS stock_actual

═══════════════════════════════════════
 UTILIZADORES DO SISTEMA
═══════════════════════════════════════

TABELA: users
  - id      (BIGINT)      PK
  - f_id    (INT)         FK → funcionarios.f_id (NULL se não ligado)
  - username(VARCHAR 150) Email usado como username
  - nivel   (VARCHAR 20)  'operario'|'gestor'|'admin'
  - tipo    (VARCHAR 20)  'rh'|'admin'|'stock'
"""

def obter_schema() -> str:
    return SCHEMA_TEXTO


# ─── Validação e execução de SQL ─────────────────────────────────────────────
def validar_sql(query: str) -> tuple[bool, str]:
    q = query.strip().upper()
    proibidos = ['DROP', 'DELETE', 'UPDATE', 'INSERT',
                 'ALTER', 'CREATE', 'TRUNCATE', 'EXEC', 'EXECUTE']
    for cmd in proibidos:
        if re.search(rf'\b{cmd}\b', q):
            return False, f"Comando não permitido: {cmd}"
    if not q.startswith('SELECT'):
        return False, "Apenas queries SELECT são permitidas."
    return True, "OK"


def executar_sql(query: str) -> tuple[pd.DataFrame | None, str]:
    valido, motivo = validar_sql(query)
    if not valido:
        return None, motivo
    if 'limit' not in query.lower():
        query = query.rstrip(';') + f' LIMIT {MAX_ROWS}'
    try:
        with get_engine().connect() as conn:
            df = pd.read_sql(text(query), conn)
        return df, ""
    except Exception as e:
        return None, str(e)


def formatar_resultado(df: pd.DataFrame | None) -> str:
    if df is None or df.empty:
        return "Nenhum resultado encontrado."
    total = len(df)
    cabecalho = f"[{total} linha(s) encontrada(s)]\n"
    if total <= 20:
        return cabecalho + df.to_string(index=False, max_colwidth=60)
    return (cabecalho
            + df.head(20).to_string(index=False, max_colwidth=60)
            + f"\n... (mostrando 20 de {total})")


# ─── Respostas fixas ─────────────────────────────────────────────────────────
RESPOSTAS_FIXAS = {
    'quem criou o artemis':  "O sistema Artemis foi desenvolvido por Alcides Nolasco como um ERP para gestão empresarial.",
    'criador do artemis':    "O sistema Artemis foi desenvolvido por Alcides Nolasco.",
    'quem criou o cronos':   "O Cronos foi desenvolvido por Alcides Nolasco como o agente de IA integrado ao Artemis.",
    'criador do cronos':     "O Cronos foi desenvolvido por Alcides Nolasco.",
    'o que é o artemis':     "Artemis é um sistema ERP para gestão de dados empresariais: RH, recrutamento, stock e operações.",
    'o que é o cronos':      "Cronos é o agente de inteligência artificial do Artemis. Consulta dados em tempo real, gera relatórios e responde perguntas sobre a empresa.",
    'o que o cronos faz':    "Cronos analisa dados do ERP directamente no banco de dados e apresenta os resultados de forma clara.",
    'função do cronos':      "Cronos consulta o banco de dados directamente, interpreta os resultados e apresenta-os de forma clara.",
}

def resposta_fixa(pergunta: str) -> str | None:
    p = pergunta.lower()
    for chave, resposta in RESPOSTAS_FIXAS.items():
        if chave in p:
            return resposta
    return None


# ─── [NOVO] Detecção de período temporal ────────────────────────────────────
def detectar_periodo(pergunta: str) -> str:
    p = pergunta.lower()
    if any(w in p for w in ['anual', 'este ano', 'ano actual', 'ano corrente', 'do ano']):
        return 'anual'
    if any(w in p for w in ['mensal', 'este mês', 'mês actual', 'mês corrente', 'do mês']):
        return 'mensal'
    if any(w in p for w in ['semanal', 'esta semana', 'semana actual', 'da semana']):
        return 'semanal'
    if any(w in p for w in ['diário', 'diario', 'hoje', 'do dia', 'dia actual']):
        return 'diario'
    return ''


def construir_contexto_periodo(periodo: str) -> str:
    if periodo == 'anual':
        return (
            "⚙️ PERÍODO ACTIVO: ANUAL\n"
            "Aplica YEAR(coluna_data) = YEAR(CURDATE()) para o ano corrente.\n"
            "Para tendência mensal: GROUP BY MONTH(coluna_data) ORDER BY MONTH(coluna_data).\n"
        )
    if periodo == 'mensal':
        return (
            "⚙️ PERÍODO ACTIVO: MENSAL\n"
            "Aplica MONTH(coluna_data)=MONTH(CURDATE()) AND YEAR(coluna_data)=YEAR(CURDATE()).\n"
        )
    if periodo == 'semanal':
        return (
            "⚙️ PERÍODO ACTIVO: SEMANAL\n"
            "Aplica WEEK(coluna_data)=WEEK(CURDATE()) AND YEAR(coluna_data)=YEAR(CURDATE()).\n"
            "Para tendência diária: GROUP BY DAYOFWEEK(coluna_data) ORDER BY DAYOFWEEK(coluna_data).\n"
        )
    if periodo == 'diario':
        return (
            "⚙️ PERÍODO ACTIVO: DIÁRIO\n"
            "Aplica DATE(coluna_data) = CURDATE().\n"
        )
    return ""


# ─── System Prompt ───────────────────────────────────────────────────────────
def construir_system_prompt(periodo: str = '') -> str:
    return f"""És o CRONOS, assistente de inteligência artificial integrado ao ERP Artemis.
Tens acesso directo ao banco de dados MySQL da empresa.

{obter_schema()}

{construir_contexto_periodo(periodo)}

COMO FUNCIONA:
Quando precisares de dados da empresa, gera UMA query SQL dentro desta tag exacta:
<sql>SELECT ... FROM ...</sql>

Os resultados serão enviados de volta para ti assim:
<resultado>...</resultado>

Depois dos resultados, formula a resposta final em português claro e profissional.

REGRAS DE SQL:
- Apenas SELECT (nunca INSERT/UPDATE/DELETE/DROP/ALTER)
- Não uses LIMIT — é aplicado automaticamente pelo sistema
- JOINs de RH:
    funcionarios f
    LEFT JOIN cargos c ON f.cargo = c.id_cargo
    LEFT JOIN departamentos d ON f.departamento_id = d.id_dpt
    LEFT JOIN controlo ct ON ct.f_id = f.f_id
- JOINs de Stock:
    stock_produto p
    LEFT JOIN stock_categoria cat ON p.categoria_id = cat.id
    LEFT JOIN stock_fornecedor forn ON p.fornecedor_id = forn.id
    LEFT JOIN stock_movimentacao m ON m.produto_id = p.id
- Stock actual (não existe coluna directa):
    SUM(CASE WHEN m.tipo='E' THEN m.quantidade ELSE 0 END) -
    SUM(CASE WHEN m.tipo='S' THEN m.quantidade ELSE 0 END) AS stock_actual
- Pesquisa por nome: WHERE f.f_nome LIKE '%nome%'
- Funcionários activos: WHERE f.ativo = 'ativo'
- Se ⚙️ PERÍODO ACTIVO estiver definido acima, aplica SEMPRE os filtros de data

FORMATAÇÃO DAS RESPOSTAS:
- Usa SEMPRE Markdown estruturado nas respostas.
- Títulos com # ## ###
- Negrito com **texto** para valores importantes
- Tabelas Markdown para dados tabulares (nunca listas quando há mais de 3 itens comparáveis)
- Listas com - para pontos de análise
- Separa secções com --- quando o relatório for longo

ESTRUTURA OBRIGATÓRIA PARA RELATÓRIOS:
## [Título do Relatório]

**Resumo executivo:** Uma frase com o insight principal.

### [Secção 1 relevante]
[dados/tabela/análise]

### [Secção 2 relevante]
[dados/tabela/análise]

---
### Análise e Recomendações
- [ponto de análise 1]
- [ponto de análise 2]

---
> **Quer explorar mais?** [Sugere 2-3 perguntas de seguimento concretas]

GRÁFICOS:
Quando os dados forem adequados para visualização, gera TAMBÉM uma tag <chart> após a tabela Markdown.
Formato obrigatório:
<chart type="TIPO" title="Título do Gráfico">
{{"labels": ["A", "B", "C"], "datasets": [{{"label": "Nome da Série", "data": [10, 20, 30]}}]}}
</chart>

Tipos disponíveis:
- "bar"           → comparações entre categorias
- "pie"           → distribuição proporcional (≤ 8 fatias)
- "doughnut"      → igual ao pie, preferido para totais
- "line"          → evolução temporal ou tendências
- "horizontalBar" → muitas categorias ou nomes longos (> 8 itens)

Regras dos gráficos:
- Gera gráfico APENAS quando os dados numéricos o justificam
- Máximo 1 gráfico por resposta
- Labels ≤ 25 caracteres
- Data: apenas números (nunca strings)
- Não repitas os dados do gráfico — a tabela já os mostra

REGRAS DE RESPOSTA:
- SQL SEMPRE dentro de <sql>...</sql> — nunca fora dessa tag
- Nunca inventes dados. Se não encontrares resultados, diz isso claramente.
- Responde sempre em português de Angola.
- Nunca mostres o SQL ao utilizador na resposta final.
- Saudações e perguntas simples → resposta directa, sem estrutura de relatório.
- Relatórios → cumpre SEMPRE a estrutura acima.
"""


# ─── Extractor de chart ──────────────────────────────────────────────────────
def extrair_chart(texto: str) -> tuple[str, dict | None]:
    """Extrai a tag <chart> do texto e devolve (texto_limpo, chart_data | None)."""
    match = re.search(
        r'<chart\s+type=["\'](\w+)["\'](?:\s+title=["\']([^"\']*)["\'])?\s*>\s*(\{.*?\})\s*</chart>',
        texto, re.DOTALL | re.IGNORECASE
    )
    if not match:
        return texto, None
    chart_type  = match.group(1).lower()
    chart_title = match.group(2) or ''
    try:
        chart_json = json.loads(match.group(3))
    except json.JSONDecodeError:
        return texto, None
    texto_limpo = texto[:match.start()].rstrip() + texto[match.end():]
    chart_data  = {'type': chart_type, 'title': chart_title, **chart_json}
    return texto_limpo, chart_data


# ─── Loop agentic ────────────────────────────────────────────────────────────
def processar_com_sql(
    client: genai.Client,
    historico: list[dict],
    pergunta: str,
    periodo: str = ''
) -> tuple[str, dict | None]:
    """
    Loop agentic: pergunta → [SQL → execução → resultado] → resposta final.
    Devolve (texto_resposta, chart_data | None).
    """
    system_prompt = construir_system_prompt(periodo)
    historico.append({"role": "user", "content": pergunta})

    for _ in range(3):
        contents = [
            types.Content(
                role="user" if m["role"] == "user" else "model",
                parts=[types.Part(text=m["content"])]
            )
            for m in historico
        ]

        resposta = client.models.generate_content(
            model=MODEL,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2,
                max_output_tokens=3000,
            ),
            contents=contents
        )

        texto = resposta.text
        match = re.search(r'<sql>(.*?)</sql>', texto, re.DOTALL | re.IGNORECASE)

        if match:
            sql = match.group(1).strip()
            historico.append({"role": "assistant", "content": texto})
            df, erro = executar_sql(sql)
            resultado = f"ERRO: {erro}" if erro else formatar_resultado(df)
            historico.append({
                "role": "user",
                "content": (
                    f"<resultado>\n{resultado}\n</resultado>\n\n"
                    "Formula agora a resposta final para o utilizador. "
                    "Não mostres o SQL nem os dados brutos — apresenta a informação de forma clara."
                )
            })
        else:
            texto_limpo, chart_data = extrair_chart(texto)
            historico.append({"role": "assistant", "content": texto_limpo})
            return texto_limpo, chart_data

    return "Não foi possível processar o pedido. Tenta reformular a pergunta.", None


# ─── Gestão de conversas ─────────────────────────────────────────────────────
def obter_conversa_ativa(usuario):
    conversa, _ = ConversaCronos.objects.get_or_create(
        usuario=usuario, ativa=True,
        defaults={'titulo': f'Conversa {usuario.username}'}
    )
    return conversa


def salvar_mensagens(conversa, pergunta: str, resposta: str, tipo_resposta: str = 'text'):
    msg_user = MensagemCronos.objects.create(
        conversa=conversa, tipo='user',
        conteudo=pergunta, tipo_resposta='text'
    )
    msg_assistant = MensagemCronos.objects.create(
        conversa=conversa, tipo='assistant',
        conteudo=resposta, tipo_resposta=tipo_resposta
    )
    conversa.num_mensagens = MensagemCronos.objects.filter(conversa=conversa).count()
    conversa.save(update_fields=['num_mensagens'])
    return msg_user, msg_assistant


def fechar_conversa(conversa):
    from django.utils import timezone
    conversa.ativa = False
    conversa.data_fim = timezone.now()
    conversa.save(update_fields=['ativa', 'data_fim'])


# ─── Views ───────────────────────────────────────────────────────────────────
@login_required(login_url='loginPage')
def cronosPage(request):
    request.session.pop('cronos_historico', None)
    return render(request, "cronos/agente-ia.html")


@login_required(login_url='loginPage')
def perguntar(request):
    """Endpoint AJAX — recebe pergunta, devolve resposta do Cronos."""
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)
    try:
        data     = json.loads(request.body)
        pergunta = data.get('pergunta', '').strip()
        if not pergunta:
            return JsonResponse({'erro': 'Pergunta vazia'}, status=400)

        conversa = obter_conversa_ativa(request.user)

        # 1. Resposta fixa
        fixa = resposta_fixa(pergunta)
        if fixa:
            salvar_mensagens(conversa, pergunta, fixa, 'fixa')
            return JsonResponse({'resposta': fixa, 'tipo': 'fixa'})

        # 2. API key
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            return JsonResponse({'erro': 'GOOGLE_API_KEY não configurada'}, status=500)

        client  = genai.Client(api_key=api_key)
        periodo = detectar_periodo(pergunta)

        # 3. Histórico da sessão
        historico_sessao   = request.session.get('cronos_historico', [])
        historico_completo = list(historico_sessao)

        # 4. Processar
        resposta_texto, chart_data = processar_com_sql(
            client, historico_completo, pergunta, periodo
        )

        # 5. Actualizar histórico
        historico_sessao.append({"role": "user",      "content": pergunta})
        historico_sessao.append({"role": "assistant", "content": resposta_texto})
        request.session['cronos_historico'] = historico_sessao[-MAX_HISTORICO:]

        # 6. Guardar no BD
        salvar_mensagens(conversa, pergunta, resposta_texto, 'sql')

        resposta_json = {
            'resposta': resposta_texto,
            'pergunta': pergunta,
            'tipo':     'sql',
            'periodo':  periodo,
        }
        if chart_data:
            resposta_json['chart'] = chart_data

        return JsonResponse(resposta_json)

    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


@login_required(login_url='loginPage')
def limpar_historico(request):
    """Endpoint para o botão 'Nova conversa' na UI."""
    if request.method == 'POST':
        conversa = ConversaCronos.objects.filter(
            usuario=request.user, ativa=True
        ).first()
        if conversa:
            fechar_conversa(conversa)
        request.session.pop('cronos_historico', None)
        return JsonResponse({'status': 'ok', 'mensagem': 'Histórico limpo.'})
    return JsonResponse({'erro': 'Método não permitido'}, status=405)


@login_required(login_url='loginPage')
def listar_conversas(request):
    """Endpoint AJAX — lista todas as conversas do utilizador."""
    try:
        conversas = ConversaCronos.objects.filter(
            usuario=request.user
        ).values('id', 'titulo', 'data_inicio', 'num_mensagens', 'ativa'
                 ).order_by('-data_inicio')
        lst = list(conversas)
        return JsonResponse({'conversas': lst, 'total': len(lst)})
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


@login_required(login_url='loginPage')
def obter_conversa(request, conversa_id):
    """Endpoint AJAX — obtém mensagens de uma conversa específica."""
    try:
        conversa  = ConversaCronos.objects.get(id=conversa_id, usuario=request.user)
        mensagens = MensagemCronos.objects.filter(conversa=conversa).values(
            'id', 'tipo', 'conteudo', 'tipo_resposta', 'data_criacao'
        ).order_by('data_criacao')
        return JsonResponse({
            'conversa': {
                'id': conversa.id, 'titulo': conversa.titulo,
                'data_inicio': conversa.data_inicio.isoformat(),
                'num_mensagens': conversa.num_mensagens, 'ativa': conversa.ativa,
            },
            'mensagens': list(mensagens)
        })
    except ConversaCronos.DoesNotExist:
        return JsonResponse({'erro': 'Conversa não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


# ─── [NOVO] Exportar .docx com python-docx + matplotlib ─────────────────────
@login_required(login_url='loginPage')
def exportar_docx(request):
    """Endpoint AJAX — recebe Markdown + chart_data e devolve .docx formatado."""
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    try:
        from docx import Document
        from docx.shared import Pt, RGBColor, Inches
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.oxml.ns import qn
        from docx.oxml import OxmlElement
        from datetime import datetime

        data     = json.loads(request.body)
        conteudo = data.get('conteudo', '').strip()
        titulo   = data.get('titulo', 'Relatório CRONOS')

        if not conteudo:
            return JsonResponse({'erro': 'Conteúdo vazio'}, status=400)

        # Remove secção "Quer explorar mais?" — não vai para o documento
        conteudo = re.split(
            r'(?:>\s*\*?\*?Quer explorar mais|---\s*\n.*?Quer explorar mais)',
            conteudo, flags=re.DOTALL | re.IGNORECASE
        )[0].rstrip()

        # ── Gera imagem do gráfico (se existir) ──────────────────────
        chart_data  = data.get('chart')
        chart_image = None
        if chart_data:
            try:
                import matplotlib
                matplotlib.use('Agg')
                import matplotlib.pyplot as plt
                import io

                labels   = chart_data.get('labels', [])
                datasets = chart_data.get('datasets', [])
                title    = chart_data.get('title', '')
                ctype    = chart_data.get('type', 'bar')
                values   = datasets[0].get('data', []) if datasets else []
                serie    = datasets[0].get('label', '') if datasets else ''

                CORES = ['#4C72B0','#DD8452','#55A868','#C44E52','#8172B2',
                         '#937860','#DA8BC3','#8C8C8C','#CCB974','#64B5CD']

                fig, ax = plt.subplots(figsize=(8, 4.5))
                fig.patch.set_facecolor('#FAFAFA')
                ax.set_facecolor('#FAFAFA')

                if ctype in ('pie', 'doughnut'):
                    wp = {'linewidth': 1.5, 'edgecolor': 'white'}
                    if ctype == 'doughnut':
                        wp['width'] = 0.5
                    ax.pie(values, labels=labels, colors=CORES[:len(labels)],
                           autopct='%1.1f%%', startangle=90, wedgeprops=wp,
                           textprops={'fontsize': 9})
                elif ctype == 'line':
                    ax.plot(labels, values, marker='o', color=CORES[0],
                            linewidth=2, markersize=6)
                    ax.fill_between(range(len(labels)), values, alpha=0.1, color=CORES[0])
                    ax.set_xticks(range(len(labels)))
                    ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=8)
                    ax.set_ylabel(serie, fontsize=9)
                    ax.grid(axis='y', linestyle='--', alpha=0.5)
                    ax.spines[['top', 'right']].set_visible(False)
                elif ctype == 'horizontalbar':
                    bars = ax.barh(labels, values,
                                   color=CORES[:len(labels)], edgecolor='white')
                    ax.bar_label(bars, fmt='%g', padding=4, fontsize=8)
                    ax.set_xlabel(serie, fontsize=9)
                    ax.spines[['top', 'right']].set_visible(False)
                    ax.grid(axis='x', linestyle='--', alpha=0.5)
                else:  # bar (default)
                    bars = ax.bar(range(len(labels)), values,
                                  color=CORES[:len(labels)], edgecolor='white', width=0.6)
                    ax.bar_label(bars, fmt='%g', padding=3, fontsize=8)
                    ax.set_xticks(range(len(labels)))
                    ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=8)
                    ax.set_ylabel(serie, fontsize=9)
                    ax.spines[['top', 'right']].set_visible(False)
                    ax.grid(axis='y', linestyle='--', alpha=0.5)

                if title:
                    ax.set_title(title, fontsize=11, fontweight='bold', pad=12)

                plt.tight_layout()
                buf = io.BytesIO()
                plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                plt.close(fig)
                buf.seek(0)
                chart_image = buf
            except Exception:
                chart_image = None  # falha silenciosa — documento sai sem gráfico

        # ── Monta o documento ────────────────────────────────────────
        doc = Document()

        # Rodapé
        section = doc.sections[0]
        footer  = section.footer
        fp1 = footer.paragraphs[0]
        fp1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp1.clear()
        r = fp1.add_run(
            f"Relatório gerado pelo CRONOS — Artemis ERP  |  "
            f"Data: {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
        )
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

        fp2 = footer.add_paragraph()
        fp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rb = fp2.add_run('CRONOS')
        rb.bold = True
        rb.font.size = Pt(9)
        rb.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        rs = fp2.add_run(' — Artemis ERP    Pág. ')
        rs.font.size = Pt(9)
        rs.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        # Campo PAGE
        for tag, fld in [('begin', None), ('instrText', ' PAGE '), ('end', None)]:
            el = OxmlElement('w:r')
            if tag == 'instrText':
                instr = OxmlElement('w:instrText')
                instr.set(qn('xml:space'), 'preserve')
                instr.text = fld
                el.append(instr)
            else:
                fc = OxmlElement('w:fldChar')
                fc.set(qn('w:fldCharType'), tag)
                el.append(fc)
            fp2._p.append(el)

        # Logo (opcional — só se existir o ficheiro)
        LOGO_PATH = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'static', 'cronos', 'logo_cronos.png'
        )
        if os.path.exists(LOGO_PATH):
            lp = doc.add_paragraph()
            lp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            lp.add_run().add_picture(LOGO_PATH, width=Inches(1.8))
            doc.add_paragraph()

        # Título
        h = doc.add_heading(titulo, level=1)
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph()

        # ── Helpers ──────────────────────────────────────────────────
        def add_inline(para, text):
            """Renderiza **negrito** e *itálico* inline."""
            for seg in re.split(r'(\*\*[^*]+\*\*)', text):
                if seg.startswith('**') and seg.endswith('**'):
                    para.add_run(seg[2:-2]).bold = True
                else:
                    for part in re.split(r'(\*[^*]+\*)', seg):
                        if part.startswith('*') and part.endswith('*'):
                            para.add_run(part[1:-1]).italic = True
                        else:
                            para.add_run(part)

        state = {'in_table': False, 'rows': []}

        def flush_table():
            rows = [r for r in state['rows']
                    if not re.match(r'^\|[\s\-|:]+\|$', r.strip())]
            if not rows:
                state.update({'in_table': False, 'rows': []})
                return
            headers = [c.strip() for c in rows[0].strip('|').split('|')]
            tbl = doc.add_table(rows=1, cols=len(headers))
            tbl.style = 'Table Grid'
            for i, ht in enumerate(headers):
                cp = tbl.rows[0].cells[i].paragraphs[0]
                cp.clear()
                add_inline(cp, ht)
                for run in cp.runs:
                    run.bold = True
            for row_line in rows[1:]:
                cells = [c.strip() for c in row_line.strip('|').split('|')]
                rc = tbl.add_row().cells
                for i, ct in enumerate(cells[:len(headers)]):
                    cp = rc[i].paragraphs[0]
                    cp.clear()
                    add_inline(cp, ct)
            doc.add_paragraph()
            state.update({'in_table': False, 'rows': []})

        # ── Parser Markdown → python-docx ────────────────────────────
        for line in conteudo.splitlines():
            s = line.strip()

            if s.startswith('|'):
                state['in_table'] = True
                state['rows'].append(s)
                continue
            elif state['in_table']:
                flush_table()

            if re.match(r'^-{3,}$', s):
                doc.add_paragraph('─' * 60)
            elif s.startswith('### '):
                doc.add_heading(s[4:], level=3)
            elif s.startswith('## '):
                doc.add_heading(s[3:], level=2)
            elif s.startswith('# '):
                doc.add_heading(s[2:], level=1)
            elif s.startswith('> '):
                p = doc.add_paragraph(style='Quote')
                add_inline(p, s[2:])
            elif s.startswith('- '):
                p = doc.add_paragraph(style='List Bullet')
                add_inline(p, s[2:])
            elif s == '':
                doc.add_paragraph()
            else:
                p = doc.add_paragraph()
                add_inline(p, s)

        if state['in_table']:
            flush_table()

        # Gráfico no final
        if chart_image:
            doc.add_paragraph()
            cp = doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.add_run().add_picture(chart_image, width=Inches(5.5))
            chart_image.close()

        # ── Serializar e devolver ────────────────────────────────────
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            tmp_path = tmp.name
        doc.save(tmp_path)
        with open(tmp_path, 'rb') as f:
            docx_bytes = f.read()
        os.unlink(tmp_path)

        nome_seguro = (
            re.sub(r'[^\w\s-]', '', titulo)[:50].strip().replace(' ', '_')
            or 'relatorio_cronos'
        )
        response = HttpResponse(
            docx_bytes,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = f'attachment; filename="{nome_seguro}.docx"'
        return response

    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': f'Erro ao gerar documento: {str(e)}'}, status=500)