# Guia Completo do Projeto Artemis (Django)

## Introdução ao Django e Conceitos Básicos

### O que é Django?
Django é um framework web **high-level** em Python que permite desenvolver aplicações web rapidamente com **bateria incluída**. É baseado no padrão **MVC** (Model-View-Template):

- **Model**: Define a estrutura dos dados (tabelas do banco)
- **View**: Lógica de negócio e processamento (funções que recebem requests)
- **Template**: Apresentação HTML (páginas renderizadas)

### Conceitos Essenciais

**URL (Uniform Resource Locator)**: Endereço da página. Ex: `/funcionarios/`
- Definidas em arquivos `urls.py`
- Mapeiam URLs → Views através de `path('padrão/', views.minha_view)`

**View (Vista)**: Função Python que:
1. Recebe **request** (dados do browser)
2. Processa lógica (consulta BD, valida forms, etc.)
3. Retorna **response** (HTML, JSON, redirect, etc.)

**Exemplo simples de View**:
```python
def minha_view(request):
    return render(request, 'template.html', {'dados': 'valor'})
```

**App**: Módulo independente que representa uma funcionalidade. Ex: `rh/`, `stock/`, `funcionarios/`

## Estrutura do Projeto Artemis

```
artemis/
├── manage.py              # Comando principal Django
├── artemis/              # Configuração principal
│   ├── settings.py       # Configurações (DB, apps instalados)
│   └── urls.py           # URLs principais (roteamento global)
├── login/                # Autenticação
├── dashboard/            # Painel administrativo
├── funcionarios/         # Gestão de funcionários
├── rh/                  # Recrutamento e férias
├── stock/               # Inventário
├── relatorios/           # Relatórios analíticos
├── definicoes/          # Usuários/sistema
└── cronos/              # [Excluído conforme pedido]
```

## URLs Principais (artemis/urls.py)

| Prefixo | App | Descrição |
|---------|-----|-----------|
| `/` | - | Redireciona para `/agente-ia/` |
| `/login/` | login | Autenticação |
| `/dashboard/` | dashboard | Painel executivo |
| `/funcionarios/` | funcionarios | CRUD funcionários |
| `/rh/` | rh | Recrutamento + Férias |
| `/stock/` | stock | Gestão de stock |
| `/relatorios/` | relatorios | Análises |
| `/sistema/` | definicoes | Gestão de usuários |

## Resumo Completo por App

### 1. **Login** (`/login/`)
**URLs principais**:
```
path("", views.loginPage, name="loginPage")    # GET/POST login
path("logout/", views.logoutUser, name="logout") # Logout
```

**Views**:
- `loginPage()`: Formulário de login → autentica → redireciona para home
- `logoutUser()`: Faz logout → redireciona para login

### 2. **Dashboard** (`/dashboard/`)
**URL**: `path('', views.ShowDashboard, name="Dashboard")`

**View `ShowDashboard()`**:
- Métricas: total funcionários, vagas abertas, férias hoje, solicitações pendentes
- Gráficos: Distribuição por departamento, candidaturas por vaga
- Tabela: Próximas férias aprovadas
- **Requer login**

### 3. **Definições/Sistema** (`/sistema/`)
**URLs**:
```
path('', views.sistemaPage, name='sistema')      # Lista usuários
path('create-user/', views.create_user, name='create_user') # Cria usuário
```

**Views**:
- `sistemaPage()`: Lista usuários Django + dropdown funcionários (apenas admin/Programador)
- `create_user()`: Cria usuário Django customizado (`Users`) vinculado a funcionário opcional

### 4. **Funcionários** (`/funcionarios/`) ⭐ **Mais Completo**
**URLs principais**:
```
""                    → FuncionariosPage()          # Dashboard + filtros
"novo/"               → NovoFuncionario()           # Form novo
"editar/<id>/"        → EditarFuncionario()         # Form edição
"salvar-funcionario/" → salvarFuncionario()         # POST salvar/criar
"delete/<id>/"        → deletarFuncionario()        # DELETE
"demitir/<id>/"       → demitirFuncionario()        # SET ativo='demitido'
"export-pdf/"         → export_pdf()                # PDF lista
"detalhes/<id>/"      → DetalhesFuncionario()
"promover-candidato/<id>/" → PromoverCandidato()  # RH → Funcionário
```

**Funcionalidades**:
- Dashboard com aniversariantes, gráficos (idade, dept, crescimento)
- CRUD completo com validações
- **Promoção**: Candidato (RH) → Funcionário
- **Export PDF** com ReportLab
- **Demissão**: Marca `ativo='demitido'` + `data_demissao`

### 5. **RH** (`/rh/`) ⭐ **Recrutamento + Férias**
**URLs principais**:
```
""                    → rhPage()                    # Dashboard completo
"salvar-Vaga/"        → salvarVaga()                # Cria vaga
"salvar-candidato/"   → salvarCandidato()           # Cria candidato
"ferias/"             → paginaFerias()              # Gestão férias
"ferias/solicitar/"   → solicitarFerias()           # POST nova solicitação
"ferias/aprovar/<id>/"→ aprovarFerias()             # Aprova
"ferias/rejeitar/<id>/"→ rejeitarFerias()          # Rejeita
"api/ferias/*"        → APIs JSON férias
"api/processos/*"     → APIs processos seletivos
"baixar-cv/<id>/"     → baixarCV()                  # Download CV
```

**Funcionalidades**:
- **Recrutamento**: Vagas → Candidatos → Processos seletivos (etapas/notas)
- **Férias complexas**: Solicitações, aprovação automática de saldos, feriados 2026, dias úteis
- **APIs JSON** para frontend dinâmico (Chart.js)
- **Download CVs** armazenados

### 6. **Stock** (`/stock/`)
**URLs**:
```
""                 → stockPage()                   # Dashboard inventário
"adicionar/"       → adicionarProduto()            # CRUD produto
"exportar-pdf/"    → export_inventario()           # PDF inventário
"adicionar-fornecedor/" → adicionarFornecedor()
"movimentar/"      → registarMovimentacao()        # Entrada/Saída
```

**Funcionalidades**:
- Stock atual = Entradas - Saídas
- Alertas: esgotados, abaixo do mínimo
- CRUD produtos/fornecedores
- **PDF valorizado** (quantidade × custo)

### 7. **Relatórios** (`/relatorios/`)
**URLs**:
```
""        → relatoriosPage()                    # Catálogo interativo
"gerar/"  → gerar_relatorio()                   # AJAX + SQL dinâmico
```

**Funcionalidades únicas**:
- **20+ relatórios pré-definidos** (RH, Stock, Recrutamento)
- **SQL parametrizado** + Pandas para análise
- **Markdown + Chart.js** gerado dinamicamente
- **Insights automáticos** (médias, totais, max/min)

## Fluxo de Autenticação

```
Login (/login/) → Autentica Users → Redireciona /agente-ia/
↓ Todas as views têm @login_required
Qualquer página → Verifica sessão → Redireciona login
```

## Como Executar o Projeto

1. `python manage.py migrate`
2. `python manage.py createsuperuser`
3. `python manage.py runserver`
4. Acesse `http://127.0.0.1:8000`

## Pontos Fortes do Código

✅ **Produção-ready**: Login, permissões, validações
✅ **APIs modernas**: JSON + frontend dinâmico
✅ **Relatórios avançados**: SQL dinâmico + gráficos
✅ **PDFs profissionais**: ReportLab
✅ **Gestão férias complexa**: Feriados, dias úteis, saldos automáticos
✅ **Integrações**: Candidato → Funcionário

## Como Ler o Código

1. **Comece por `artemis/urls.py`** → Veja roteamento global
2. **Para cada app**: `app/urls.py` → `app/views.py` → `app/models.py`
3. **Templates**: `app/templates/app/nome.html`
4. **Models → Migrations**: Veja `app/migrations/`

**Exemplo completo**: `/rh/` → `rh/urls.py` → `rh/views.py#rhPage()` → `rh/templates/rh/rh.html`

---

*Documento gerado automaticamente por BLACKBOXAI. Resumo exclui app `cronos` conforme solicitado.*

