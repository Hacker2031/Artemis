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

# ─── Configuração ─────────────────────────────────────────────────────────────
DB_CONFIG = {
    'user':     os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Artemis2025!'),
    'host':     os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'artemis_db'),
}

TABELAS_PERMITIDAS = {'funcionarios', 'cargos', 'departamentos', 'users'}

MAX_ROWS      = 50
MODEL         = "gemini-2.0-flash"
MAX_HISTORICO = 10

# ─── Engine SQLAlchemy (singleton) ────────────────────────────────────────────
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


# ─── Schema Inspector (com cache) ─────────────────────────────────────────────
_schema_cache: str | None = None

def obter_schema() -> str:
    global _schema_cache
    if _schema_cache:
        return _schema_cache
    try:
        inspector = inspect(get_engine())
        linhas = ["SCHEMA DO BANCO DE DADOS (artemis_db)\n"]
        for tabela in inspector.get_table_names():
            if tabela not in TABELAS_PERMITIDAS:
                continue
            colunas = inspector.get_columns(tabela)
            fks     = inspector.get_foreign_keys(tabela)
            linhas.append(f"TABELA: {tabela}")
            for col in colunas:
                nulo = "NULL" if col.get('nullable', True) else "NOT NULL"
                linhas.append(f"  - {col['name']} ({col['type']}) {nulo}")
            for fk in fks:
                cols     = ', '.join(fk['constrained_columns'])
                ref_tab  = fk['referred_table']
                ref_cols = ', '.join(fk['referred_columns'])
                linhas.append(f"  FK: {cols} → {ref_tab}({ref_cols})")
            linhas.append("")
        _schema_cache = "\n".join(linhas)
        return _schema_cache
    except Exception as e:
        return f"[Erro ao ler schema: {e}]"


# ─── Validação e execução de SQL ──────────────────────────────────────────────
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


# ─── Respostas fixas ──────────────────────────────────────────────────────────
RESPOSTAS_FIXAS = {
    'quem criou o artemis':  "O sistema Artemis foi desenvolvido por Alcides Nolasco como um ERP para gestão empresarial.",
    'criador do artemis':    "O sistema Artemis foi desenvolvido por Alcides Nolasco.",
    'quem criou o cronos':   "O Cronos foi desenvolvido por Alcides Nolasco como o agente de IA integrado ao Artemis.",
    'criador do cronos':     "O Cronos foi desenvolvido por Alcides Nolasco.",
    'o que é o artemis':     "Artemis é um sistema ERP para gestão de dados empresariais: RH, stock, vendas e operações.",
    'o que é o cronos':      "Cronos é o agente de inteligência artificial do Artemis. Consulta dados em tempo real, gera relatórios e gráficos sobre a empresa.",
    'o que o cronos faz':    "Cronos consulta o banco de dados directamente, interpreta os resultados e apresenta-os com tabelas, análises e gráficos interactivos.",
    'função do cronos':      "Cronos consulta o banco de dados, interpreta resultados e apresenta-os de forma clara com gráficos quando relevante.",
}

def resposta_fixa(pergunta: str) -> str | None:
    p = pergunta.lower()
    for chave, resposta in RESPOSTAS_FIXAS.items():
        if chave in p:
            return resposta
    return None


# ─── System Prompt ────────────────────────────────────────────────────────────
def construir_system_prompt() -> str:
    schema = obter_schema()
    return f"""És o CRONOS, assistente de inteligência artificial integrado ao ERP Artemis.
Tens acesso directo ao banco de dados MySQL da empresa.

{schema}

══════════════════════════════════════
COMO FUNCIONA
══════════════════════════════════════
Quando precisares de dados da empresa, gera UMA query SQL dentro desta tag exacta:
<sql>SELECT ... FROM ...</sql>

Os resultados serão enviados de volta para ti assim:
<resultado>...</resultado>

Depois dos resultados, formula a resposta final em português claro e profissional.

══════════════════════════════════════
REGRAS DE SQL
══════════════════════════════════════
- Apenas SELECT (nunca INSERT/UPDATE/DELETE/DROP)
- Usa JOINs adequados:
  funcionarios f
  JOIN cargos c ON f.cargo = c.id_cargo
  JOIN departamentos d ON f.departamento_id = d.id_dpt
- Para nomes usa: WHERE f_nome LIKE '%nome%'
- Não uses LIMIT — é aplicado automaticamente pelo sistema

══════════════════════════════════════
GRÁFICOS INTERACTIVOS
══════════════════════════════════════
Sempre que os dados se prestam a visualização (distribuições, rankings, comparações, proporções),
inclui OBRIGATORIAMENTE um bloco de dados para gráfico em formato JSON, dentro destas tags:

<chart>
{{
  "type": "bar",
  "title": "Título descritivo do gráfico",
  "labels": ["Label 1", "Label 2", "Label 3"],
  "datasets": [
    {{
      "label": "Nome da série",
      "data": [10, 25, 8]
    }}
  ]
}}
</chart>

TIPOS DE GRÁFICO DISPONÍVEIS:
- "bar"      → Rankings, comparações entre categorias (ex: salário por departamento)
- "pie"      → Proporções/distribuições (ex: % de funcionários por sexo)
- "doughnut" → Como pie, mas com aspecto mais moderno
- "line"     → Evolução temporal ou tendências

QUANDO USAR CADA TIPO:
- Distribuição por departamento/sexo/estado civil → "doughnut" ou "pie"
- Top N (salários, contagens) → "bar"
- Faixas salariais → "bar" com múltiplas séries (mínimo, base, máximo)
- Crescimento/evolução → "line"

REGRAS DO BLOCO <chart>:
- O JSON deve ser válido (sem aspas simples, sem comentários, sem vírgulas finais)
- Os arrays "labels" e "data" devem ter o mesmo tamanho
- Para múltiplas séries, usa vários objectos em "datasets"
- NÃO incluas "backgroundColor" — o frontend aplica cores automaticamente
- Coloca o bloco <chart> DEPOIS do texto/tabela Markdown correspondente

══════════════════════════════════════
FORMATAÇÃO DAS RESPOSTAS
══════════════════════════════════════
- Usa SEMPRE Markdown estruturado nas respostas
- Títulos com # ## ###
- **negrito** para valores importantes
- Tabelas Markdown para dados tabulares (nunca listas quando há mais de 3 itens comparáveis)
- Listas com - para pontos de análise
- Separa secções com --- quando o relatório for longo

══════════════════════════════════════
ESTRUTURA OBRIGATÓRIA PARA RELATÓRIOS
══════════════════════════════════════
Quando gerares um relatório ou análise com dados, segue sempre:

## [Título do Relatório]

**Resumo executivo:** Uma frase com o insight principal.

### [Secção 1]
[dados/tabela/análise]

<chart>...</chart>

### [Secção 2]
[dados/tabela/análise]

---
### Análise e Recomendações
- [ponto 1]
- [ponto 2]

---
> **Quer explorar mais?** [Sugere 2-3 perguntas de seguimento concretas]

══════════════════════════════════════
REGRAS GERAIS
══════════════════════════════════════
- Coloca sempre o SQL dentro de <sql>...</sql>
- Nunca mostres o SQL ao utilizador na resposta final
- Nunca inventes dados — se não encontrares resultados, diz isso claramente
- Responde sempre em português de Angola
- Para perguntas simples (saudações, etc.) responde directamente sem estrutura de relatório
- Nunca incluas os blocos <chart> sem dados reais dos resultados SQL
"""


# ─── Loop agentic com Gemini ──────────────────────────────────────────────────
def processar_com_sql(client: genai.Client, historico: list[dict], pergunta: str) -> str:
    system_prompt = construir_system_prompt()
    historico.append({"role": "user", "content": pergunta})

    MAX_ITER = 4  # +1 iteração para suportar gráficos complexos

    for _ in range(MAX_ITER):
        contents = []
        for msg in historico:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=msg["content"])]
                )
            )

        resposta = client.models.generate_content(
            model=MODEL,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2,
                max_output_tokens=3072,  # mais espaço para gráficos + análise
            ),
            contents=contents
        )

        texto = resposta.text

        # Verifica se o Gemini gerou SQL
        match = re.search(r'<sql>(.*?)</sql>', texto, re.DOTALL | re.IGNORECASE)
        if match:
            sql = match.group(1).strip()
            historico.append({"role": "assistant", "content": texto})

            df, erro = executar_sql(sql)
            resultado = f"ERRO: {erro}" if erro else formatar_resultado(df)

            # Devolve resultado + instrução para incluir gráfico se adequado
            historico.append({
                "role": "user",
                "content": (
                    f"<resultado>\n{resultado}\n</resultado>\n\n"
                    "Formula agora a resposta final para o utilizador:\n"
                    "1. Apresenta os dados em Markdown claro (tabela se adequado)\n"
                    "2. Se os dados tiverem 2+ categorias/valores comparáveis, inclui OBRIGATORIAMENTE um bloco <chart>JSON</chart>\n"
                    "3. Não mostres o SQL na resposta\n"
                    "4. Termina com análise e sugestões de aprofundamento"
                )
            })
            continue
        else:
            historico.append({"role": "assistant", "content": texto})
            return texto

    return "Não foi possível processar o pedido. Tenta reformular a pergunta."


# ─── Gestão de conversas ──────────────────────────────────────────────────────
def obter_conversa_ativa(usuario):
    conversa, _ = ConversaCronos.objects.get_or_create(
        usuario=usuario,
        ativa=True,
        defaults={'titulo': f'Conversa {usuario.username}'}
    )
    return conversa


def salvar_mensagens(conversa, pergunta: str, resposta: str, tipo_resposta: str = 'text'):
    MensagemCronos.objects.create(
        conversa=conversa, tipo='user',
        conteudo=pergunta, tipo_resposta='text'
    )
    MensagemCronos.objects.create(
        conversa=conversa, tipo='assistant',
        conteudo=resposta, tipo_resposta=tipo_resposta
    )
    conversa.num_mensagens = MensagemCronos.objects.filter(conversa=conversa).count()
    conversa.save(update_fields=['num_mensagens'])


def fechar_conversa(conversa):
    from django.utils import timezone
    conversa.ativa = False
    conversa.data_fim = timezone.now()
    conversa.save(update_fields=['ativa', 'data_fim'])


# ─── Views Django ─────────────────────────────────────────────────────────────
@login_required(login_url='loginPage')
def cronosPage(request):
    request.session.pop('cronos_historico', None)
    return render(request, "cronos/agente-ia.html")


@login_required(login_url='loginPage')
def perguntar(request):
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    try:
        data     = json.loads(request.body)
        pergunta = data.get('pergunta', '').strip()

        if not pergunta:
            return JsonResponse({'erro': 'Pergunta vazia'}, status=400)

        conversa = obter_conversa_ativa(request.user)

        # 1. Respostas fixas (sem IA)
        fixa = resposta_fixa(pergunta)
        if fixa:
            salvar_mensagens(conversa, pergunta, fixa, 'fixa')
            return JsonResponse({'resposta': fixa, 'tipo': 'fixa'})

        # 2. Verificar API key
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            return JsonResponse({'erro': 'GOOGLE_API_KEY não configurada'}, status=500)

        client = genai.Client(api_key=api_key)

        # 3. Histórico da sessão
        historico_sessao   = request.session.get('cronos_historico', [])
        historico_completo = list(historico_sessao)

        # 4. Processar com Text-to-SQL (+ gráficos)
        resposta_texto = processar_com_sql(client, historico_completo, pergunta)

        # 5. Actualizar histórico de sessão (só pergunta + resposta final, sem tags <chart>)
        resposta_limpa = re.sub(r'<chart>[\s\S]*?</chart>', '', resposta_texto).strip()
        historico_sessao.append({"role": "user",      "content": pergunta})
        historico_sessao.append({"role": "assistant", "content": resposta_limpa})
        request.session['cronos_historico'] = historico_sessao[-MAX_HISTORICO:]

        # 6. Salvar no banco (com as tags <chart> para reutilização futura)
        salvar_mensagens(conversa, pergunta, resposta_texto, 'sql')

        return JsonResponse({
            'resposta': resposta_texto,
            'pergunta': pergunta,
            'tipo':     'sql'
        })

    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


@login_required(login_url='loginPage')
def limpar_historico(request):
    """
    Fecha a conversa ACTUAL e limpa a sessão.
    As conversas anteriores ficam PRESERVADAS no histórico.
    """
    if request.method == 'POST':
        conversa = ConversaCronos.objects.filter(
            usuario=request.user, ativa=True
        ).first()
        if conversa:
            fechar_conversa(conversa)
        request.session.pop('cronos_historico', None)
        return JsonResponse({'status': 'ok', 'mensagem': 'Conversa fechada. Histórico preservado.'})
    return JsonResponse({'erro': 'Método não permitido'}, status=405)


@login_required(login_url='loginPage')
def listar_conversas(request):
    try:
        conversas = ConversaCronos.objects.filter(
            usuario=request.user
        ).values(
            'id', 'titulo', 'data_inicio', 'num_mensagens', 'ativa'
        ).order_by('-data_inicio')
        return JsonResponse({'conversas': list(conversas), 'total': conversas.count()})
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


@login_required(login_url='loginPage')
def obter_conversa(request, conversa_id):
    try:
        conversa = ConversaCronos.objects.get(id=conversa_id, usuario=request.user)
        mensagens = MensagemCronos.objects.filter(
            conversa=conversa
        ).values(
            'id', 'tipo', 'conteudo', 'tipo_resposta', 'data_criacao'
        ).order_by('data_criacao')
        return JsonResponse({
            'conversa': {
                'id':            conversa.id,
                'titulo':        conversa.titulo,
                'data_inicio':   conversa.data_inicio.isoformat(),
                'num_mensagens': conversa.num_mensagens,
                'ativa':         conversa.ativa,
            },
            'mensagens': list(mensagens)
        })
    except ConversaCronos.DoesNotExist:
        return JsonResponse({'erro': 'Conversa não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


@login_required(login_url='loginPage')
def exportar_docx(request):
    """Recebe Markdown e devolve ficheiro .docx via pypandoc."""
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    try:
        data     = json.loads(request.body)
        conteudo = data.get('conteudo', '').strip()
        titulo   = data.get('titulo', 'Relatório CRONOS')

        if not conteudo:
            return JsonResponse({'erro': 'Conteúdo vazio'}, status=400)

        try:
            import pypandoc
        except ImportError:
            return JsonResponse(
                {'erro': 'Dependência em falta. Execute: pip install pypandoc'},
                status=500
            )

        from datetime import datetime
        data_hora = datetime.now().strftime('%d/%m/%Y às %H:%M')

        # Remove blocos <chart> do documento Word (não fazem sentido em .docx)
        conteudo_limpo = re.sub(r'<chart>[\s\S]*?</chart>', '', conteudo).strip()

        markdown_final = (
            f"# {titulo}\n\n"
            f"*Relatório gerado pelo **CRONOS** — Artemis ERP*  \n"
            f"*Data: {data_hora}*\n\n"
            "---\n\n"
            f"{conteudo_limpo}"
        )

        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            tmp_path = tmp.name

        pypandoc.convert_text(
            markdown_final, 'docx', format='markdown',
            outputfile=tmp_path, extra_args=['--standalone']
        )

        with open(tmp_path, 'rb') as f:
            docx_bytes = f.read()
        os.unlink(tmp_path)

        nome_seguro = re.sub(r'[^\w\s-]', '', titulo)[:50].strip().replace(' ', '_') or 'relatorio_cronos'

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