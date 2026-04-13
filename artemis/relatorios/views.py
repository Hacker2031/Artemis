import json
import re
from datetime import datetime

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Reutiliza a lógica de BD do Cronos
from cronos.views import executar_sql


# ─── Catálogo de Relatórios ──────────────────────────────────────────────────
# Cada entrada define: titulo, modulo, icone, descricao, sql e chart config.
# chart: None → relatório sem gráfico (só tabela)

CATALOGO = {

    # ══════════════════════════════════════════════════════════════════════════
    #  MÓDULO: RECURSOS HUMANOS
    # ══════════════════════════════════════════════════════════════════════════

    'rh_capital_humano': {
        'titulo':    'Capital Humano por Departamento',
        'modulo':    'rh',
        'icone':     'groups',
        'descricao': 'Total de funcionários, distribuição por género e média salarial por departamento.',
        'sql': """
            SELECT
                d.nome_dpt                                    AS Departamento,
                COUNT(f.f_id)                                 AS Total,
                SUM(CASE WHEN f.sexo = 'M' THEN 1 ELSE 0 END) AS Homens,
                SUM(CASE WHEN f.sexo = 'F' THEN 1 ELSE 0 END) AS Mulheres,
                ROUND(AVG(c.sal_base), 0)                     AS Media_Salarial_Kz
            FROM funcionarios f
            LEFT JOIN cargos c        ON f.cargo = c.id_cargo
            LEFT JOIN departamentos d ON f.departamento_id = d.id_dpt
            WHERE f.ativo = 'ativo'
            GROUP BY d.id_dpt, d.nome_dpt
            ORDER BY Total DESC
        """,
        'chart': {
            'type':      'bar',
            'label_col': 'Departamento',
            'value_col': 'Total',
            'title':     'Funcionários por Departamento',
        },
    },

    'rh_folha_salarial': {
        'titulo':    'Faixas Salariais por Cargo',
        'modulo':    'rh',
        'icone':     'payments',
        'descricao': 'Salário mínimo, base e máximo de cada cargo activo, com número de funcionários.',
        'sql': """
            SELECT
                c.nome_cargo              AS Cargo,
                COUNT(f.f_id)             AS Funcionários,
                c.sal_min                 AS Sal_Min_Kz,
                c.sal_base                AS Sal_Base_Kz,
                c.sal_max                 AS Sal_Max_Kz
            FROM cargos c
            LEFT JOIN funcionarios f ON f.cargo = c.id_cargo AND f.ativo = 'ativo'
            WHERE c.ativo = 1
            GROUP BY c.id_cargo, c.nome_cargo, c.sal_min, c.sal_base, c.sal_max
            ORDER BY c.sal_base DESC
        """,
        'chart': {
            'type':      'horizontalBar',
            'label_col': 'Cargo',
            'value_col': 'Sal_Base_Kz',
            'title':     'Salário Base por Cargo (Kz)',
        },
    },

    'rh_distribuicao': {
        'titulo':    'Distribuição por Sexo e Estado Civil',
        'modulo':    'rh',
        'icone':     'diversity_3',
        'descricao': 'Contagem de funcionários activos por sexo e estado civil.',
        'sql': """
            SELECT
                sexo         AS Sexo,
                estado_civil AS Estado_Civil,
                COUNT(*)     AS Total
            FROM funcionarios
            WHERE ativo = 'ativo'
            GROUP BY sexo, estado_civil
            ORDER BY Sexo, Total DESC
        """,
        'chart': {
            'type':      'doughnut',
            'label_col': 'Estado_Civil',
            'value_col': 'Total',
            'title':     'Distribuição por Estado Civil',
        },
    },

    'rh_ferias': {
        'titulo':    'Saldo de Férias por Funcionário',
        'modulo':    'rh',
        'icone':     'beach_access',
        'descricao': 'Férias gozadas, agendadas e restantes de cada funcionário activo.',
        'sql': """
            SELECT
                f.f_nome              AS Funcionário,
                d.nome_dpt            AS Departamento,
                ct.ferias_gozadas     AS Gozadas,
                ct.ferias_agendadas   AS Agendadas,
                ct.ferias_restantes   AS Restantes
            FROM controlo ct
            JOIN funcionarios f       ON ct.f_id = f.f_id
            LEFT JOIN departamentos d ON f.departamento_id = d.id_dpt
            WHERE f.ativo = 'ativo'
            ORDER BY ct.ferias_restantes DESC
        """,
        'chart': {
            'type':      'bar',
            'label_col': 'Funcionário',
            'value_col': 'Restantes',
            'title':     'Dias de Férias Restantes por Funcionário',
        },
    },

    'rh_faltas': {
        'titulo':    'Presenças e Faltas',
        'modulo':    'rh',
        'icone':     'event_busy',
        'descricao': 'Presenças, faltas e percentagem de absentismo por funcionário.',
        'sql': """
            SELECT
                f.f_nome              AS Funcionário,
                d.nome_dpt            AS Departamento,
                ct.numero_presencas   AS Presenças,
                ct.numero_faltas      AS Faltas,
                ROUND(
                    ct.numero_faltas * 100.0 /
                    NULLIF(ct.numero_presencas + ct.numero_faltas, 0), 1
                )                     AS Pct_Absentismo
            FROM controlo ct
            JOIN funcionarios f       ON ct.f_id = f.f_id
            LEFT JOIN departamentos d ON f.departamento_id = d.id_dpt
            WHERE f.ativo = 'ativo'
            ORDER BY Faltas DESC
        """,
        'chart': {
            'type':      'bar',
            'label_col': 'Funcionário',
            'value_col': 'Faltas',
            'title':     'Faltas por Funcionário',
        },
    },

    'rh_antiguidade': {
        'titulo':    'Antiguidade dos Funcionários',
        'modulo':    'rh',
        'icone':     'history_edu',
        'descricao': 'Anos de serviço de cada funcionário activo desde a data de contratação.',
        'sql': """
            SELECT
                f.f_nome                                                AS Funcionário,
                c.nome_cargo                                            AS Cargo,
                d.nome_dpt                                              AS Departamento,
                TIMESTAMPDIFF(YEAR, f.data_contratacao, CURDATE())      AS Anos_Serviço,
                DATE_FORMAT(f.data_contratacao, '%d/%m/%Y')             AS Data_Entrada
            FROM funcionarios f
            LEFT JOIN cargos c        ON f.cargo = c.id_cargo
            LEFT JOIN departamentos d ON f.departamento_id = d.id_dpt
            WHERE f.ativo = 'ativo' AND f.data_contratacao IS NOT NULL
            ORDER BY Anos_Serviço DESC
        """,
        'chart': {
            'type':      'bar',
            'label_col': 'Funcionário',
            'value_col': 'Anos_Serviço',
            'title':     'Anos de Serviço por Funcionário',
        },
    },

    'rh_avaliacoes': {
        'titulo':    'Avaliações de Desempenho',
        'modulo':    'rh',
        'icone':     'stars',
        'descricao': 'Nota de avaliação de cada funcionário activo, da maior para a menor.',
        'sql': """
            SELECT
                f.f_nome                             AS Funcionário,
                c.nome_cargo                         AS Cargo,
                d.nome_dpt                           AS Departamento,
                CAST(f.avaliacao AS DECIMAL(5,1))    AS Nota
            FROM funcionarios f
            LEFT JOIN cargos c        ON f.cargo = c.id_cargo
            LEFT JOIN departamentos d ON f.departamento_id = d.id_dpt
            WHERE f.ativo = 'ativo'
              AND f.avaliacao IS NOT NULL
              AND f.avaliacao != ''
            ORDER BY Nota DESC
        """,
        'chart': {
            'type':      'bar',
            'label_col': 'Funcionário',
            'value_col': 'Nota',
            'title':     'Avaliações de Desempenho',
        },
    },

    'rh_equipas': {
        'titulo':    'Equipas Activas',
        'modulo':    'rh',
        'icone':     'group_work',
        'descricao': 'Equipas em curso com o responsável, departamento e número de membros.',
        'sql': """
            SELECT
                e.nome_equipa                       AS Equipa,
                e.tipo_equipa                       AS Tipo,
                d.nome_dpt                          AS Departamento,
                f.f_nome                            AS Responsável,
                COUNT(me.f_id)                      AS Membros,
                DATE_FORMAT(e.data_inicio,'%d/%m/%Y') AS Inicio
            FROM equipas e
            LEFT JOIN departamentos d     ON e.departamento_id = d.id_dpt
            LEFT JOIN funcionarios f      ON e.responsavel_equipa = f.f_id
            LEFT JOIN membros_equipas me  ON me.id_equipas = e.id_equipas
                                        AND me.data_saida IS NULL
            WHERE e.ativo = 1
            GROUP BY e.id_equipas, e.nome_equipa, e.tipo_equipa, d.nome_dpt, f.f_nome, e.data_inicio
            ORDER BY Membros DESC
        """,
        'chart': {
            'type':      'bar',
            'label_col': 'Equipa',
            'value_col': 'Membros',
            'title':     'Membros por Equipa',
        },
    },

    # ══════════════════════════════════════════════════════════════════════════
    #  MÓDULO: STOCK
    # ══════════════════════════════════════════════════════════════════════════

    'stock_actual': {
        'titulo':    'Stock Actual por Produto',
        'modulo':    'stock',
        'icone':     'inventory',
        'descricao': 'Nível de stock calculado (entradas − saídas) para cada produto.',
        'sql': """
            SELECT
                p.nome      AS Produto,
                cat.nome    AS Categoria,
                COALESCE(SUM(CASE WHEN m.tipo = 'E' THEN m.quantidade ELSE 0 END), 0) -
                COALESCE(SUM(CASE WHEN m.tipo = 'S' THEN m.quantidade ELSE 0 END), 0) AS Stock_Actual,
                p.stock_minimo AS Mínimo
            FROM stock_produto p
            LEFT JOIN stock_categoria cat  ON p.categoria_id = cat.id
            LEFT JOIN stock_movimentacao m ON m.produto_id = p.id
            GROUP BY p.id, p.nome, cat.nome, p.stock_minimo
            ORDER BY Stock_Actual DESC
        """,
        'chart': {
            'type':      'bar',
            'label_col': 'Produto',
            'value_col': 'Stock_Actual',
            'title':     'Stock Actual por Produto',
        },
    },

    'stock_minimos': {
        'titulo':    'Produtos Abaixo do Stock Mínimo',
        'modulo':    'stock',
        'icone':     'warning',
        'descricao': 'Alertas de ruptura — produtos cujo stock está abaixo do nível mínimo.',
        'sql': """
            SELECT
                p.nome            AS Produto,
                cat.nome          AS Categoria,
                forn.nome_empresa AS Fornecedor,
                COALESCE(SUM(CASE WHEN m.tipo = 'E' THEN m.quantidade ELSE 0 END), 0) -
                COALESCE(SUM(CASE WHEN m.tipo = 'S' THEN m.quantidade ELSE 0 END), 0) AS Stock_Actual,
                p.stock_minimo    AS Mínimo,
                p.stock_minimo - (
                    COALESCE(SUM(CASE WHEN m.tipo = 'E' THEN m.quantidade ELSE 0 END), 0) -
                    COALESCE(SUM(CASE WHEN m.tipo = 'S' THEN m.quantidade ELSE 0 END), 0)
                )                 AS Défice
            FROM stock_produto p
            LEFT JOIN stock_categoria cat   ON p.categoria_id = cat.id
            LEFT JOIN stock_fornecedor forn ON p.fornecedor_id = forn.id
            LEFT JOIN stock_movimentacao m  ON m.produto_id = p.id
            GROUP BY p.id, p.nome, cat.nome, forn.nome_empresa, p.stock_minimo
            HAVING Stock_Actual < p.stock_minimo
            ORDER BY Défice DESC
        """,
        'chart': {
            'type':      'horizontalBar',
            'label_col': 'Produto',
            'value_col': 'Défice',
            'title':     'Défice de Stock por Produto',
        },
    },

    'stock_movimentacoes': {
        'titulo':    'Movimentações Recentes de Stock',
        'modulo':    'stock',
        'icone':     'swap_vert',
        'descricao': 'Últimas movimentações de stock registadas (entradas e saídas).',
        'sql': """
            SELECT
                DATE_FORMAT(m.data, '%d/%m/%Y %H:%i')              AS Data,
                p.nome                                              AS Produto,
                CASE m.tipo WHEN 'E' THEN 'Entrada' ELSE 'Saída'
                END                                                 AS Tipo,
                m.quantidade                                        AS Quantidade,
                m.motivo                                            AS Motivo
            FROM stock_movimentacao m
            JOIN stock_produto p ON m.produto_id = p.id
            ORDER BY m.data DESC
            LIMIT 100
        """,
        'chart': None,
    },

    'stock_categorias': {
        'titulo':    'Stock por Categoria',
        'modulo':    'stock',
        'icone':     'category',
        'descricao': 'Total de stock e número de produtos agrupado por categoria.',
        'sql': """
            SELECT
                cat.nome             AS Categoria,
                COUNT(DISTINCT p.id) AS Produtos,
                COALESCE(SUM(CASE WHEN m.tipo = 'E' THEN m.quantidade ELSE 0 END), 0) -
                COALESCE(SUM(CASE WHEN m.tipo = 'S' THEN m.quantidade ELSE 0 END), 0) AS Stock_Total
            FROM stock_categoria cat
            LEFT JOIN stock_produto p      ON p.categoria_id = cat.id
            LEFT JOIN stock_movimentacao m ON m.produto_id = p.id
            GROUP BY cat.id, cat.nome
            ORDER BY Stock_Total DESC
        """,
        'chart': {
            'type':      'doughnut',
            'label_col': 'Categoria',
            'value_col': 'Stock_Total',
            'title':     'Distribuição do Stock por Categoria',
        },
    },

    # ══════════════════════════════════════════════════════════════════════════
    #  MÓDULO: RECRUTAMENTO
    # ══════════════════════════════════════════════════════════════════════════

    'rec_vagas': {
        'titulo':    'Vagas Abertas',
        'modulo':    'recrutamento',
        'icone':     'work_outline',
        'descricao': 'Vagas actualmente abertas com número de candidaturas e prazo limite.',
        'sql': """
            SELECT
                v.titulo                                AS Vaga,
                c.nome_cargo                            AS Cargo,
                d.nome_dpt                              AS Departamento,
                v.num_vagas                             AS Posições,
                v.num_candidaturas                      AS Candidaturas,
                v.tipo                                  AS Tipo,
                DATE_FORMAT(v.data_limite, '%d/%m/%Y')  AS Prazo
            FROM vagas v
            LEFT JOIN cargos c        ON v.cargo_id = c.id_cargo
            LEFT JOIN departamentos d ON v.departamento_id = d.id_dpt
            WHERE v.estado = 'aberta'
            ORDER BY v.data_limite ASC
        """,
        'chart': {
            'type':      'bar',
            'label_col': 'Vaga',
            'value_col': 'Candidaturas',
            'title':     'Candidaturas por Vaga',
        },
    },

    'rec_candidatos': {
        'titulo':    'Pipeline de Candidatos',
        'modulo':    'recrutamento',
        'icone':     'people_outline',
        'descricao': 'Distribuição dos candidatos por estado e fonte de recrutamento.',
        'sql': """
            SELECT
                estado              AS Estado,
                fonte_recrutamento  AS Fonte,
                COUNT(*)            AS Total
            FROM candidatos
            GROUP BY estado, fonte_recrutamento
            ORDER BY Total DESC
        """,
        'chart': {
            'type':      'doughnut',
            'label_col': 'Estado',
            'value_col': 'Total',
            'title':     'Candidatos por Estado',
        },
    },

    'rec_processo': {
        'titulo':    'Resultados do Processo Selectivo',
        'modulo':    'recrutamento',
        'icone':     'fact_check',
        'descricao': 'Resumo dos resultados e médias de notas por etapa do processo selectivo.',
        'sql': """
            SELECT
                ps.etapa                    AS Etapa,
                ps.resultado                AS Resultado,
                COUNT(*)                    AS Total,
                ROUND(AVG(ps.nota), 1)      AS Média_Nota
            FROM processo_seletivo ps
            GROUP BY ps.etapa, ps.resultado
            ORDER BY ps.etapa, Total DESC
        """,
        'chart': {
            'type':      'bar',
            'label_col': 'Resultado',
            'value_col': 'Total',
            'title':     'Resultados do Processo Selectivo',
        },
    },
}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def df_para_markdown(df: pd.DataFrame) -> str:
    """Converte um DataFrame para uma tabela Markdown."""
    if df is None or df.empty:
        return "_Nenhum resultado encontrado._"

    cols = list(df.columns)
    header = '| ' + ' | '.join(cols) + ' |'
    sep    = '| ' + ' | '.join(['---'] * len(cols)) + ' |'

    rows = []
    for _, row in df.iterrows():
        cells = []
        for val in row:
            if val is None:
                cells.append('-')
            elif isinstance(val, float):
                cells.append(f'{val:,.2f}')
            else:
                cells.append(str(val))
        rows.append('| ' + ' | '.join(cells) + ' |')

    return '\n'.join([header, sep] + rows)


def gerar_chart_data(df: pd.DataFrame, chart_config: dict | None) -> dict | None:
    """Extrai dados do DataFrame para o formato Chart.js."""
    if df is None or df.empty or not chart_config:
        return None

    label_col = chart_config.get('label_col')
    value_col = chart_config.get('value_col')

    if label_col not in df.columns or value_col not in df.columns:
        return None

    labels = [str(v)[:25] for v in df[label_col].tolist()]
    values = []
    for v in df[value_col].tolist():
        try:
            values.append(round(float(v), 2) if v is not None else 0)
        except (TypeError, ValueError):
            values.append(0)

    return {
        'type':   chart_config['type'],
        'title':  chart_config.get('title', ''),
        'labels': labels,
        'datasets': [{
            'label': value_col.replace('_', ' '),
            'data':  values,
        }],
    }


def gerar_markdown_relatorio(config: dict, df: pd.DataFrame) -> str:
    """Constrói o Markdown completo do relatório com insights automáticos."""
    agora  = datetime.now().strftime('%d/%m/%Y às %H:%M')
    titulo = config['titulo']

    linhas = [
        f"## {titulo}",
        f"",
        f"**Resumo executivo:** {config['descricao']}",
        f"",
        f"*Gerado em: {agora}*",
        f"",
        f"### Dados",
        f"",
        df_para_markdown(df),
    ]

    # Insights automáticos das colunas numéricas
    if df is not None and not df.empty:
        num_cols = df.select_dtypes(include='number').columns.tolist()
        if num_cols:
            linhas += ["", "---", "### Análise Automática"]
            for col in num_cols[:3]:
                total  = df[col].sum()
                maximo = df[col].max()
                minimo = df[col].min()
                media  = df[col].mean()
                col_label = col.replace('_', ' ')
                linhas.append(
                    f"- **{col_label}**: total **{total:,.0f}** "
                    f"| média **{media:,.1f}** "
                    f"| máx. **{maximo:,.0f}** "
                    f"| mín. **{minimo:,.0f}**"
                )

    return "\n".join(linhas)


# ─── Views ───────────────────────────────────────────────────────────────────

@login_required(login_url='loginPage')
def relatoriosPage(request):
    # Catálogo sem SQL (o cliente não precisa das queries)
    catalogo_cliente = {
        k: {
            'id':       k,
            'titulo':   v['titulo'],
            'modulo':   v['modulo'],
            'icone':    v['icone'],
            'descricao':v['descricao'],
        }
        for k, v in CATALOGO.items()
    }
    return render(request, 'relatorios/relatorios.html', {
        'catalogo_json': json.dumps(catalogo_cliente, ensure_ascii=False),
    })


@login_required(login_url='loginPage')
def gerar_relatorio(request):
    """Endpoint AJAX — executa o SQL do relatório e devolve markdown + chart."""
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    try:
        data   = json.loads(request.body)
        rel_id = data.get('relatorio_id', '').strip()

        if rel_id not in CATALOGO:
            return JsonResponse({'erro': 'Relatório não encontrado'}, status=404)

        config     = CATALOGO[rel_id]
        df, erro   = executar_sql(config['sql'])

        if erro:
            return JsonResponse({'erro': f'Erro ao executar consulta: {erro}'}, status=500)

        markdown   = gerar_markdown_relatorio(config, df)
        chart_data = gerar_chart_data(df, config.get('chart'))

        return JsonResponse({
            'titulo':          config['titulo'],
            'markdown':        markdown,
            'chart':           chart_data,
            'total_registos':  len(df) if df is not None else 0,
        })

    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)