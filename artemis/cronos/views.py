import os
import re
import json
import pandas as pd

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from sqlalchemy import create_engine, text, inspect
from google import genai
from google.genai import types
from dotenv import load_dotenv
from django.http import HttpResponse
import tempfile, os, re
 


load_dotenv()

# ─── Configuração do BD ───────────────────────────────────────────────────────
DB_CONFIG = {
    'user':     os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Artemis2025!'),
    'host':     os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'artemis_db'),
}

TABELAS_PERMITIDAS = {'funcionarios', 'cargos', 'departamentos', 'users'}

MAX_ROWS      = 50
MODEL         = "gemini-3-flash-preview"   # gemini-2.0-flash tier gratuito: 1500 req/dia
MAX_HISTORICO = 10                   # mensagens mantidas na sessão

# ─── Engine SQLAlchemy (singleton) ───────────────────────────────────────────
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


# ─── Respostas fixas (sem IA) ─────────────────────────────────────────────────
RESPOSTAS_FIXAS = {
    'quem criou o artemis':  "O sistema Artemis foi desenvolvido por Alcides Nolasco como um ERP para gestão empresarial.",
    'criador do artemis':    "O sistema Artemis foi desenvolvido por Alcides Nolasco.",
    'quem criou o cronos':   "O Cronos foi desenvolvido por Alcides Nolasco como o agente de IA integrado ao Artemis.",
    'criador do cronos':     "O Cronos foi desenvolvido por Alcides Nolasco.",
    'o que é o artemis':     "Artemis é um sistema ERP para gestão de dados empresariais: RH, stock, vendas e operações.",
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


# ─── System Prompt ────────────────────────────────────────────────────────────
def construir_system_prompt() -> str:
    schema = obter_schema()
    return f"""És o CRONOS, assistente de inteligência artificial integrado ao ERP Artemis.
Tens acesso directo ao banco de dados MySQL da empresa.

{schema}

COMO FUNCIONA:
Quando precisares de dados da empresa, gera UMA query SQL dentro desta tag exacta:
<sql>SELECT ... FROM ...</sql>

Os resultados serão enviados de volta para ti assim:
<resultado>...</resultado>

Depois dos resultados, formula a resposta final em português claro e profissional.

REGRAS DE SQL:
- Apenas SELECT (nunca INSERT/UPDATE/DELETE/DROP)
- Usa JOINs adequados (ex: funcionarios f JOIN cargos c ON f.cargo = c.id_cargo JOIN departamentos d ON f.departamento_id = d.id_dpt)
- Para nomes usa: WHERE f_nome LIKE '%nome%'
- Não uses LIMIT — é aplicado automaticamente pelo sistema

FORMATAÇÃO DAS RESPOSTAS:
- Usa SEMPRE Markdown estruturado nas respostas.
- Títulos com # ## ###
- Negrito com **texto** para valores importantes
- Tabelas Markdown para dados tabulares (nunca listas quando há mais de 3 itens comparáveis)
- Listas com - para pontos de análise
- Separa secções com --- quando o relatório for longo

ESTRUTURA OBRIGATÓRIA PARA RELATÓRIOS:
Quando gerares um relatório ou análise com dados, segue sempre esta estrutura:

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
> **Quer explorar mais?** [Sugere 2-3 perguntas de seguimento concretas e relevantes com base nos dados apresentados, como "Posso detalhar os funcionários do departamento X?" ou "Quer ver a evolução salarial por cargo?"]

REGRAS DE RESPOSTA:
- IMPORTANTE: Coloca sempre o SQL dentro de <sql>...</sql> — nunca fora dessa tag.
- Nunca inventes dados. Se não encontrares resultados, diz isso claramente.
- Responde sempre em português de Angola.
- Nunca mostres o SQL ao utilizador na resposta final.
- Para perguntas simples (saudações, etc.) responde directamente sem estrutura de relatório.
- Para qualquer pedido de relatório ou análise, SEMPRE termina com sugestões de aprofundamento.
"""

# ─── Processamento agentic com Gemini ─────────────────────────────────────────
def processar_com_sql(client: genai.Client, historico: list[dict], pergunta: str) -> str:
    """
    Loop agentic: pergunta → [SQL → execução → resultado] → resposta final.
    O histórico é convertido para o formato Content do Gemini a cada iteração.
    """
    system_prompt = construir_system_prompt()

    # Adiciona a pergunta actual ao histórico local
    historico.append({"role": "user", "content": pergunta})

    MAX_ITER = 3

    for _ in range(MAX_ITER):

        # Converte histórico para formato Gemini (lista de Content)
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
                max_output_tokens=2048,
            ),
            contents=contents
        )

        texto = resposta.text

        # Verifica se o Gemini gerou SQL
        match = re.search(r'<sql>(.*?)</sql>', texto, re.DOTALL | re.IGNORECASE)
        if match:
            sql = match.group(1).strip()

            # Adiciona resposta do modelo ao histórico
            historico.append({"role": "assistant", "content": texto})

            # Executa o SQL
            df, erro = executar_sql(sql)
            resultado = f"ERRO: {erro}" if erro else formatar_resultado(df)

            # Devolve o resultado ao modelo
            historico.append({
                "role": "user",
                "content": (
                    f"<resultado>\n{resultado}\n</resultado>\n\n"
                    "Formula agora a resposta final para o utilizador. "
                    "Não mostres o SQL nem os dados brutos — apresenta a informação de forma clara."
                )
            })
            continue  # próxima iteração → Gemini formula resposta final

        else:
            # Resposta final sem SQL
            historico.append({"role": "assistant", "content": texto})
            return texto

    return "Não foi possível processar o pedido. Tenta reformular a pergunta."


# ─── Views Django ─────────────────────────────────────────────────────────────
@login_required(login_url='loginPage')
def cronosPage(request):
    request.session.pop('cronos_historico', None)
    return render(request, "cronos/agente-ia.html")


@login_required(login_url='loginPage')
def perguntar(request):
    """Endpoint AJAX — recebe pergunta, devolve resposta do Cronos 2.0"""
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    try:
        data     = json.loads(request.body)
        pergunta = data.get('pergunta', '').strip()

        if not pergunta:
            return JsonResponse({'erro': 'Pergunta vazia'}, status=400)

        # ── 1. Resposta fixa ──────────────────────────────────────────────
        fixa = resposta_fixa(pergunta)
        if fixa:
            return JsonResponse({'resposta': fixa, 'tipo': 'fixa'})

        # ── 2. Verificar API key ──────────────────────────────────────────
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            return JsonResponse({'erro': 'GOOGLE_API_KEY não configurada'}, status=500)

        client = genai.Client(api_key=api_key)

        # ── 3. Histórico da sessão ────────────────────────────────────────
        historico_sessao   = request.session.get('cronos_historico', [])
        historico_completo = list(historico_sessao)

        # ── 4. Processar com Text-to-SQL ──────────────────────────────────
        resposta_texto = processar_com_sql(client, historico_completo, pergunta)

        # ── 5. Actualizar histórico (só pergunta + resposta final) ─────────
        historico_sessao.append({"role": "user",      "content": pergunta})
        historico_sessao.append({"role": "assistant", "content": resposta_texto})
        request.session['cronos_historico'] = historico_sessao[-MAX_HISTORICO:]

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
    """Endpoint para o botão 'Nova conversa' na UI"""
    if request.method == 'POST':
        request.session.pop('cronos_historico', None)
        return JsonResponse({'status': 'ok', 'mensagem': 'Histórico limpo.'})
    return JsonResponse({'erro': 'Método não permitido'}, status=405)

@login_required(login_url='loginPage')
def exportar_docx(request):
    """
    Endpoint AJAX — recebe conteúdo Markdown e devolve ficheiro .docx.
    Body JSON esperado:
        { "conteudo": "...", "titulo": "Nome do Relatório" }
    """
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
 
        # Cabeçalho do documento
        from datetime import datetime
        data_hora = datetime.now().strftime('%d/%m/%Y às %H:%M')
        markdown_final = (
            f"# {titulo}\n\n"
            f"*Relatório gerado pelo **CRONOS** — Artemis ERP*  \n"
            f"*Data: {data_hora}*\n\n"
            "---\n\n"
            f"{conteudo}"
        )
 
        # Gera o .docx via pandoc
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            tmp_path = tmp.name
 
        pypandoc.convert_text(
            markdown_final,
            'docx',
            format='markdown',
            outputfile=tmp_path,
            extra_args=['--standalone']
        )
 
        with open(tmp_path, 'rb') as f:
            docx_bytes = f.read()
 
        os.unlink(tmp_path)
 
        # Nome do ficheiro seguro
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
 