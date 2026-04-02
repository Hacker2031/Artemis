# RESUMO DE MUDANÇAS - SISTEMA DE FÉRIAS

## 📁 Arquivos Modificados

### 1. `artemis/funcionarios/models.py`
- ✏️ **Classe `Controlo`**: Adicionar 10 novos campos
- ✨ **Classe `PlanamentFerias`** (NOVA): Solicitações de férias

### 2. `artemis/funcionarios/views.py`  
- ✏️ Adicionar import: `from .models import Controlo, PlanamentFerias`
- ✨ Função `salvarFuncionario()`: Auto-criar Controlo para novo funcionário

### 3. `artemis/rh/views.py`
- ✏️ Adicionar imports necessários
- ✨ Implementar 6 funções novas:
  - `solicitarFerias()`
  - `aprovarFerias()`
  - `rejeitarFerias()`
  - `obterSolicitacoesFerias()`
  - `obterFuncionariosComFerias()`
  - `paginaFerias()`
- ✨ Adicionar função utilitária: `calcular_dias_uteis()`

### 4. `artemis/rh/urls.py`
- ✨ Adicionar 6 novas rotas para gerenciar férias

### 5. `artemis/rh/templates/rh/rh.html`
- ✏️ Tab "ferias": Atualizar para carregar página dinâmica

### 6. `artemis/rh/templates/rh/ferias_new.html` (NOVO)
- ✨ Página completa de gestão de férias
- Cards de estatísticas
- Tabelas de solicitações e saldos
- Modal para criar solicitação
- Formulário POST integrado

### 7. `artemis/funcionarios/admin.py`
- ✏️ Adicionar `PlanamentFerias` aos imports
- ✨ Registar `PlanamentFeriasAdmin` com fieldsets

### 8. `artemis/funcionarios/migrations/0016_ferias_management.py` (NOVO)
- ✨ Migration com todos os novos campos

---

## 🔄 Fluxo de Dados

```
Frontend (Modal)
    ↓
POST /rh/ferias/solicitar/
    ↓
views.solicitarFerias()
    ↓
PlanamentFerias.objects.create()
    ↓
status='pendente'
    ↓
Django Admin / Views
    ↓
POST /rh/ferias/aprovar/<id>/
    ↓
views.aprovarFerias()
    ↓
status='aprovado' + Controlo.update()
    ↓
Sistema Atualizado
```

---

## 🛠️ Instalação Passo a Passo

### 1. Executar Migration
```bash
python manage.py migrate funcionarios
```

### 2. (Opcional) Testar Sistema
```bash
python manage.py shell < test_ferias.py
```

### 3. Admin Django
- Acessar `/admin/`
- Seção "Planeament Ferias"
- Ver/aprovar solicitações

### 4. Página Web
- Acessar `/rh/ferias/`
- Visualizar dashboard
- Criar novas solicitações

---

## 📊 Campos Novos adicionados à `Controlo`

| Campo | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `direito_ferias_anual` | int | 22 | Dias anuais |
| `ferias_gozadas` | int | 0 | Dias já tirados |
| `ferias_agendadas` | int | 0 | Dias marcados |
| `ferias_restantes` | int | 22 | Dias restantes |
| `baixa_medica_dias` | int | 0 | Dias baixa médica |
| `licenca_maternidade_dias` | int | 0 | Dias maternidade |
| `licenca_sem_vencimento_dias` | int | 0 | Dias sem vencimento |
| `ferias_vencidas` | int | 0 | Dias vencidos |
| `ultimo_ano_ferias` | int | 0 | Último ano atualizado |

---

## 🌐 Endpoints Criados

| Método | Rota | Função | Descrição |
|--------|------|--------|-----------|
| GET | `/rh/ferias/` | `paginaFerias()` | Página dashboard |
| POST | `/rh/ferias/solicitar/` | `solicitarFerias()` | Criar solicitação |
| POST | `/rh/ferias/aprovar/<id>/` | `aprovarFerias()` | Aprovar |
| POST | `/rh/ferias/rejeitar/<id>/` | `rejeitarFerias()` | Rejeitar |
| GET | `/rh/api/ferias/solicitacoes/` | `obterSolicitacoesFerias()` | API JSON |
| GET | `/rh/api/ferias/funcionarios/` | `obterFuncionariosComFerias()` | API JSON |

---

## ✨ Recursos Principais

✅ Criar solicitações de férias  
✅ Aprovar/rejeitar solicitações  
✅ Rastrear saldo de férias por funcionário  
✅ Calcular dias úteis (excluindo feriados)  
✅ Dashboard com estatísticas  
✅ Tabelas de saldos e solicitações  
✅ Integração com Django Admin  
✅ APIs JSON para frontend  
✅ Auto-criar Controlo para novo funcionário  
✅ Suporta múltiplos tipos de ausência  

---

## 🐛 Possíveis Problemas & Soluções

### Problema: Migration não encontra models
**Solução:** Certificar que `PlanamentFerias` está importado em `__init__.py`

### Problema: Erro ao criar Controlo
**Solução:** Garantir que `data_contratacao` do funcionário não é None

### Problema: Dias restantes incorretos
**Solução:** Verificar se `ferias_agendadas` está sendo atualizado corretamente

---

## 📝 TODO (Futuros)

- [ ] Notificações por email
- [ ] Calendário visual com cores
- [ ] Exportar PDF/Excel
- [ ] Dashboard com gráficos
- [ ] Integração com sistema de ponto
- [ ] Aprovação multi-nível
- [ ] Histórico de alterações
- [ ] Sincronização com calendário do Outlook

---

**Data de Criação:** 29 de Março de 2026  
**Status:** ✅ Implementado e Testado
