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
from cronos.models import ConversaCronos, MensagemCronos
 


load_dotenv()

# ─── Inicializar IA ────────────────────────────────────────────────────────
def inicializar_ia() -> bool:
    """Inicializa a IA (Gemini). Valida API key disponível."""
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("[CRONOS] ⚠️ GOOGLE_API_KEY não configurada no .env")
            return False
        # Testa se a key é válida criando um cliente
        client = genai.Client(api_key=api_key)
        return True
    except Exception as e:
        print(f"[CRONOS] ❌ Erro ao inicializar: {e}")
        return False

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

GRÁFICOS:
Quando os dados forem adequados para visualização, gera TAMBÉM uma tag <chart> logo após a tabela Markdown correspondente.
Formato obrigatório:
<chart type="TIPO" title="Título do Gráfico">
{{"labels": ["A", "B", "C"], "datasets": [{{"label": "Nome da Série", "data": [10, 20, 30]}}]}}
</chart>

Regras para escolha do tipo:
- "bar"       → comparações entre categorias (ex: funcionários por departamento)
- "pie"       → distribuição proporcional com poucos itens (≤ 8)
- "doughnut"  → igual ao pie mas com totais no centro
- "line"      → evolução temporal ou tendências
- "horizontalBar" → muitas categorias longas (> 8 itens)

Regras adicionais:
- Gera gráfico APENAS quando os dados numéricos o justificam (nunca para texto puro)
- Máximo 1 gráfico por resposta
- Os labels devem ser curtos (≤ 25 caracteres)
- Os values devem ser números inteiros ou decimais (nunca strings)
- Nunca repitas os dados do gráfico — a tabela Markdown já os mostra

REGRAS DE RESPOSTA:
- Cumpra sempre a ESTRUTURA OBRIGATÓRIA
- IMPORTANTE: Coloca sempre o SQL dentro de <sql>...</sql> — nunca fora dessa tag.
- Nunca inventes dados. Se não encontrares resultados, diz isso claramente.
- Responde sempre em português de Angola.
- Nunca mostres o SQL ao utilizador na resposta final.
- Para perguntas simples (saudações, etc.) responde directamente sem estrutura de relatório.
- Para qualquer pedido de relatório ou análise, SEMPRE termina com sugestões de aprofundamento.
"""

# ─── Processamento agentic com Gemini ─────────────────────────────────────────
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
    # Remove a tag do texto visível
    texto_limpo = texto[:match.start()].rstrip() + texto[match.end():]
    chart_data  = {'type': chart_type, 'title': chart_title, **chart_json}
    return texto_limpo, chart_data


def processar_com_sql(client: genai.Client, historico: list[dict], pergunta: str) -> tuple[str, dict | None]:
    """
    Loop agentic: pergunta → [SQL → execução → resultado] → resposta final.
    Devolve (texto_resposta, chart_data | None).
    """
    system_prompt = construir_system_prompt()
    historico.append({"role": "user", "content": pergunta})

    MAX_ITER = 3

    for _ in range(MAX_ITER):
        contents = []
        for msg in historico:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(
                types.Content(role=role, parts=[types.Part(text=msg["content"])])
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
            continue

        else:
            texto_limpo, chart_data = extrair_chart(texto)
            historico.append({"role": "assistant", "content": texto_limpo})
            return texto_limpo, chart_data

    return "Não foi possível processar o pedido. Tenta reformular a pergunta.", None


# ─── Armazenar histórico em base de dados ─────────────────────────────────────
def obter_conversa_ativa(usuario):
    """Obtém ou cria a conversa activa para o utilizador"""
    conversa, created = ConversaCronos.objects.get_or_create(
        usuario=usuario,
        ativa=True,
        defaults={'titulo': f'Conversa {usuario.username}'}
    )
    return conversa


def salvar_mensagens(conversa, pergunta: str, resposta: str, tipo_resposta: str = 'text'):
    """Salva a pergunta e resposta (mensagens) no banco de dados"""
    # Salva a pergunta
    msg_user = MensagemCronos.objects.create(
        conversa=conversa,
        tipo='user',
        conteudo=pergunta,
        tipo_resposta='text'
    )

    # Salva a resposta
    msg_assistant = MensagemCronos.objects.create(
        conversa=conversa,
        tipo='assistant',
        conteudo=resposta,
        tipo_resposta=tipo_resposta
    )

    # Atualiza contador de mensagens na conversa
    conversa.num_mensagens = MensagemCronos.objects.filter(conversa=conversa).count()
    conversa.save(update_fields=['num_mensagens'])

    return msg_user, msg_assistant


def fechar_conversa(conversa):
    """Marca a conversa como inactiva"""
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
    """Endpoint AJAX — recebe pergunta, devolve resposta do Cronos 2.0"""
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    try:
        data     = json.loads(request.body)
        pergunta = data.get('pergunta', '').strip()

        if not pergunta:
            return JsonResponse({'erro': 'Pergunta vazia'}, status=400)

        # ── Obter conversa activa ────────────────────────────────────────────
        conversa = obter_conversa_ativa(request.user)

        # ── 1. Resposta fixa ──────────────────────────────────────────────
        fixa = resposta_fixa(pergunta)
        if fixa:
            # Salva a interação com resposta fixa
            salvar_mensagens(conversa, pergunta, fixa, 'fixa')
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
        resposta_texto, chart_data = processar_com_sql(client, historico_completo, pergunta)

        # ── 5. Actualizar histórico (só pergunta + resposta final) ─────────
        historico_sessao.append({"role": "user",      "content": pergunta})
        historico_sessao.append({"role": "assistant", "content": resposta_texto})
        request.session['cronos_historico'] = historico_sessao[-MAX_HISTORICO:]

        # ── 6. Salvar no banco de dados ───────────────────────────────────
        salvar_mensagens(conversa, pergunta, resposta_texto, 'sql')

        resposta_json = {
            'resposta': resposta_texto,
            'pergunta': pergunta,
            'tipo':     'sql'
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
    """Endpoint para o botão 'Nova conversa' na UI"""
    if request.method == 'POST':
        # Fecha a conversa actual
        conversa = ConversaCronos.objects.filter(
            usuario=request.user,
            ativa=True
        ).first()
        if conversa:
            fechar_conversa(conversa)

        # Limpa a sessão
        request.session.pop('cronos_historico', None)
        return JsonResponse({'status': 'ok', 'mensagem': 'Histórico limpo.'})
    return JsonResponse({'erro': 'Método não permitido'}, status=405)


@login_required(login_url='loginPage')
def listar_conversas(request):
    """Endpoint AJAX — lista todas as conversas do utilizador"""
    try:
        conversas = ConversaCronos.objects.filter(
            usuario=request.user
        ).values(
            'id', 'titulo', 'data_inicio', 'num_mensagens', 'ativa'
        ).order_by('-data_inicio')

        conversas_list = list(conversas)

        return JsonResponse({
            'conversas': conversas_list,
            'total': len(conversas_list)
        })
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


@login_required(login_url='loginPage')
def obter_conversa(request, conversa_id):
    """Endpoint AJAX — obtém mensagens de uma conversa específica"""
    try:
        conversa = ConversaCronos.objects.get(
            id=conversa_id,
            usuario=request.user
        )

        mensagens = MensagemCronos.objects.filter(
            conversa=conversa
        ).values(
            'id', 'tipo', 'conteudo', 'tipo_resposta', 'data_criacao'
        ).order_by('data_criacao')

        return JsonResponse({
            'conversa': {
                'id': conversa.id,
                'titulo': conversa.titulo,
                'data_inicio': conversa.data_inicio.isoformat(),
                'num_mensagens': conversa.num_mensagens,
                'ativa': conversa.ativa,
            },
            'mensagens': list(mensagens)
        })
    except ConversaCronos.DoesNotExist:
        return JsonResponse({'erro': 'Conversa não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)

@login_required(login_url='loginPage')
def exportar_docx(request):
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

        # ── Remove secção "Quer explorar mais?" ─────────────────────
        conteudo = re.split(
            r'(?:>\s*\*?\*?Quer explorar mais|---\s*\n.*?Quer explorar mais)',
            conteudo,
            flags=re.DOTALL | re.IGNORECASE
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

                CORES = [
                    '#4C72B0','#DD8452','#55A868','#C44E52','#8172B2',
                    '#937860','#DA8BC3','#8C8C8C','#CCB974','#64B5CD'
                ]

                fig, ax = plt.subplots(figsize=(8, 4.5))
                fig.patch.set_facecolor('#FAFAFA')
                ax.set_facecolor('#FAFAFA')

                if ctype in ('pie', 'doughnut'):
                    wedge_props = {'linewidth': 1.5, 'edgecolor': 'white'}
                    if ctype == 'doughnut':
                        wedge_props['width'] = 0.5
                    ax.pie(values, labels=labels, colors=CORES[:len(labels)],
                           autopct='%1.1f%%', startangle=90,
                           wedgeprops=wedge_props,
                           textprops={'fontsize': 9})
                elif ctype == 'line':
                    ax.plot(labels, values, marker='o', color=CORES[0],
                            linewidth=2, markersize=6)
                    ax.fill_between(range(len(labels)), values,
                                    alpha=0.1, color=CORES[0])
                    ax.set_xticks(range(len(labels)))
                    ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=8)
                    ax.set_ylabel(serie, fontsize=9)
                    ax.grid(axis='y', linestyle='--', alpha=0.5)
                    ax.spines[['top','right']].set_visible(False)
                elif ctype == 'horizontalbar':
                    bars = ax.barh(labels, values,
                                   color=CORES[:len(labels)], edgecolor='white')
                    ax.bar_label(bars, fmt='%g', padding=4, fontsize=8)
                    ax.set_xlabel(serie, fontsize=9)
                    ax.spines[['top','right']].set_visible(False)
                    ax.grid(axis='x', linestyle='--', alpha=0.5)
                else:  # bar (default)
                    bars = ax.bar(range(len(labels)), values,
                                  color=CORES[:len(labels)], edgecolor='white', width=0.6)
                    ax.bar_label(bars, fmt='%g', padding=3, fontsize=8)
                    ax.set_xticks(range(len(labels)))
                    ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=8)
                    ax.set_ylabel(serie, fontsize=9)
                    ax.spines[['top','right']].set_visible(False)
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
                chart_image = None

        doc = Document()

        # ── Rodapé ──────────────────────────────────────────────────
        section = doc.sections[0]
        footer  = section.footer

        fp1 = footer.paragraphs[0]
        fp1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp1.clear()
        run_data = fp1.add_run(
            f"Relatório gerado pelo CRONOS — Artemis ERP  |  "
            f"Data: {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
        )
        run_data.font.size = Pt(9)
        run_data.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

        fp2 = footer.add_paragraph()
        fp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_brand = fp2.add_run('CRONOS')
        run_brand.bold = True
        run_brand.font.size = Pt(9)
        run_brand.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        run_sub2 = fp2.add_run(' — Artemis ERP    Pág. ')
        run_sub2.font.size = Pt(9)
        run_sub2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

        r_begin = OxmlElement('w:r')
        rpr = OxmlElement('w:rPr')
        sz = OxmlElement('w:sz')
        sz.set(qn('w:val'), '18')
        rpr.append(sz)
        r_begin.append(rpr)
        fc_begin = OxmlElement('w:fldChar')
        fc_begin.set(qn('w:fldCharType'), 'begin')
        r_begin.append(fc_begin)
        fp2._p.append(r_begin)

        r_instr = OxmlElement('w:r')
        instr = OxmlElement('w:instrText')
        instr.set(qn('xml:space'), 'preserve')
        instr.text = ' PAGE '
        r_instr.append(instr)
        fp2._p.append(r_instr)

        r_end = OxmlElement('w:r')
        fc_end = OxmlElement('w:fldChar')
        fc_end.set(qn('w:fldCharType'), 'end')
        r_end.append(fc_end)
        fp2._p.append(r_end)

        # ── Logo no início ───────────────────────────────────────────
        LOGO_PATH = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'static', 'cronos', 'logo_cronos.png'
        )
        if os.path.exists(LOGO_PATH):
            logo_p = doc.add_paragraph()
            logo_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            logo_p.add_run().add_picture(LOGO_PATH, width=Inches(1.8))
            doc.add_paragraph()

        # ── Título ──────────────────────────────────────────────────
        h = doc.add_heading(titulo, level=1)
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph()

        # ── Funções auxiliares ───────────────────────────────────────
        def add_inline(para, text):
            segments = re.split(r'(\*\*[^*]+\*\*)', text)
            for seg in segments:
                if seg.startswith('**') and seg.endswith('**'):
                    r = para.add_run(seg[2:-2])
                    r.bold = True
                else:
                    parts = re.split(r'(\*[^*]+\*)', seg)
                    for part in parts:
                        if part.startswith('*') and part.endswith('*'):
                            r = para.add_run(part[1:-1])
                            r.italic = True
                        else:
                            para.add_run(part)

        state = {'in_table': False, 'rows': []}

        def flush_table():
            rows = [r for r in state['rows']
                    if not re.match(r'^\|[\s\-|:]+\|$', r.strip())]
            if not rows:
                state['in_table'] = False
                state['rows'].clear()
                return
            headers = [c.strip() for c in rows[0].strip('|').split('|')]
            tbl = doc.add_table(rows=1, cols=len(headers))
            tbl.style = 'Table Grid'
            for i, h_txt in enumerate(headers):
                cell_p = tbl.rows[0].cells[i].paragraphs[0]
                cell_p.clear()
                add_inline(cell_p, h_txt)
                for run in cell_p.runs:
                    run.bold = True
            for row_line in rows[1:]:
                cells = [c.strip() for c in row_line.strip('|').split('|')]
                row_cells = tbl.add_row().cells
                for i, cell_txt in enumerate(cells[:len(headers)]):
                    cell_p = row_cells[i].paragraphs[0]
                    cell_p.clear()
                    add_inline(cell_p, cell_txt)
            doc.add_paragraph()
            state['in_table'] = False
            state['rows'].clear()

        # ── Parser Markdown ──────────────────────────────────────────
        for line in conteudo.splitlines():
            stripped = line.strip()

            if stripped.startswith('|'):
                state['in_table'] = True
                state['rows'].append(stripped)
                continue
            elif state['in_table']:
                flush_table()

            if re.match(r'^-{3,}$', stripped):
                doc.add_paragraph('─' * 60)
            elif stripped.startswith('### '):
                doc.add_heading(stripped[4:], level=3)
            elif stripped.startswith('## '):
                doc.add_heading(stripped[3:], level=2)
            elif stripped.startswith('# '):
                doc.add_heading(stripped[2:], level=1)
            elif stripped.startswith('> '):
                p = doc.add_paragraph(style='Quote')
                add_inline(p, stripped[2:])
            elif stripped.startswith('- '):
                p = doc.add_paragraph(style='List Bullet')
                add_inline(p, stripped[2:])
            elif stripped == '':
                doc.add_paragraph()
            else:
                p = doc.add_paragraph()
                add_inline(p, stripped)

        if state['in_table']:
            flush_table()

        # ── Gráfico no final ─────────────────────────────────────────
        if chart_image:
            doc.add_paragraph()
            chart_p = doc.add_paragraph()
            chart_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            chart_p.add_run().add_picture(chart_image, width=Inches(5.5))
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