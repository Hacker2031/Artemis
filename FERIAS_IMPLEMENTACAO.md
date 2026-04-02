# 📋 IMPLEMENTAÇÃO - SISTEMA DE GESTÃO DE FÉRIAS

## ✅ O que foi feito:

### 🗄️ **Base de Dados**
1. **Model `Controlo` expandida** com novos campos:
   - `direito_ferias_anual` - dias de férias por lei (default: 22)
   - `ferias_gozadas` - dias já tirados
   - `ferias_agendadas` - dias marcados
   - `ferias_restantes` - dias restantes (calculado)
   - Campos para other ausências: médica, maternidade, sem vencimento, vencidas

2. **Nova Model `PlanamentFerias`** (solicitações):
   - Funcionário + Tipo de ausência + Datas
   - Status: Pendente → Aprovado/Rejeitado
   - Rastreamento completo (criado_em, aprovado_por, etc)

3. **Migration criada** (0016_ferias_management.py)
   - Pronta para aplicar: `python manage.py migrate`

---

### 🎯 **Backend (Views)**

#### 1. **Criar Solicitação**
```
POST /rh/ferias/solicitar/
- Parâmetros: funcionario_id, tipo_ausencia, data_inicio, data_fim, observacoes
- Valida: datas, dias disponíveis
- Calcula: dias úteis automaticamente
```

#### 2. **Aprovar/Rejeitar**
```
POST /rh/ferias/aprovar/<id>/
POST /rh/ferias/rejeitar/<id>/
- Atualiza status em PlanamentFerias
- Se aprovado: deduz dias do Controlo
```

#### 3. **APIs JSON**
```
GET /rh/api/ferias/solicitacoes/
GET /rh/api/ferias/funcionarios/
- Retorna dados estruturados para frontend
```

#### 4. **Página de Férias**
```
GET /rh/ferias/
- Template: ferias_new.html
- Mostra: solicitações, saldos, estatísticas
```

---

### 🎨 **Frontend**

#### **Nova Página: `/rh/ferias/`**
- **Cards de Estatísticas:**
  - Total de solicitações
  - Aprovadas
  - Pendentes
  - Em férias hoje

- **Tabelas:**
  - Solicitações (com ações: aprovar/rejeitar)
  - Saldos por funcionário (direito/gozado/agendado/restante)

- **Modal de Criação:**
  - Select de funcionário
  - Tipo de ausência
  - Datas (início/fim)
  - Observações

---

### 🔌 **Integrações**

✅ Views pronta  
✅ URLs configuradas  
✅ Admin Django registado  
✅ Models criadas  
✅ Migration gerada  

⏳ **Pendente:**
- Executar `python manage.py migrate`
- Testar endpoints

---

## 🚀 Como Usar

### 1. **Aplicar Migration**
```bash
python manage.py migrate funcionarios
```

### 2. **Acessar Página**
- Na página RH, clique na tab "Férias"
- Ou acesse: `/rh/ferias/`

### 3. **Criar Solicitação**
- Clique "Nova Solicitação"
- Preencha formulário
- Clique "Salvar"

### 4. **Aprovar via Admin**
- Vá para Django Admin
- Seção "Planeament Ferias"
- Selecione solicitação
- Clique "Aprovar"

---

## 📊 Estrutura de Dados

### **Controlo (Expandida)**
```
- id_controlo (PK)
- fun_id (FK) → Funcionarios
- Campos anteriores...
- + direito_ferias_anual (22)
- + ferias_gozadas (0)
- + ferias_agendadas (0)
- + ferias_restantes (22)
- + baixa_medica_dias (0)
- + ficenca_maternidade_dias (0)
- + licenca_sem_vencimento_dias (0)
- + ferias_vencidas (0)
- + ultimo_ano_ferias (0)
```

### **PlanamentFerias (Nova)**
```
- id_solicitacao (PK)
- funcionario (FK) → Funcionarios
- tipo_ausencia (choice: ferias/medica/maternidade/sem_vencimento)
- data_inicio (date)
- data_fim (date)
- dias_uteis (int, calculado)
- status (choice: pendente/aprovado/rejeitado/cancelado)
- observacoes (text, optional)
- criado_em (datetime, auto)
- atualizado_em (datetime, auto)
- aprovado_por (FK) → Funcionarios, optional
- data_aprovacao (datetime, optional)
```

---

## 📝 Notas Importantes

1. **Dias Úteis**: Calculated excluindo fins de semana + feriados 2026
2. **Novo Funcionário**: Auto-cria Controlo com values padrão
3. **Admin Django**: Totalmente configurado para gestão manual
4. **Feriados 2026**: Codificados na função `calcular_dias_uteis()`

---

## 🔭 Próximos Passos (Opcional)

- Notificações por email (aprovação/rejeição)
- Calendário visual com férias marcadas
- Exportação em PDF/Excel
- Dashboard com gráficos de férias
- Integração com sistema de ponto

---

**Status**: ✅ Implementação Completa - Pronto para testes
