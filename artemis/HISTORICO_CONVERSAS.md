# Histórico de Conversas - Sistema CRONOS

## 📋 O que foi implementado

### Tabelas de Banco de Dados

#### 1. **ConversaCronos** (cronos_conversas)
Armazena cada conversa/sessão com o CRONOS

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT (PK) | ID único |
| usuario | FK → Users | Utilizador da conversa |
| titulo | VARCHAR(200) | Título descritivo da conversa |
| resumo | TEXT | Resumo automático (opcional) |
| data_inicio | DATETIME | Quando começou |
| data_fim | DATETIME | Quando terminou (nullable) |
| ativa | BOOLEAN | Se está aberta ou fechada |
| num_mensagens | INT | Total de mensagens na conversa |

**Índices:**
- `usuario, -data_inicio` (para listar conversas do utilizador)
- `ativa` (para filtrar conversas activas)

#### 2. **MensagemCronos** (cronos_mensagens)
Armazena cada mensagem dentro de uma conversa

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT (PK) | ID único |
| conversa | FK → ConversaCronos | Conversa a que pertence |
| tipo | ENUM | 'user' ou 'assistant' |
| conteudo | TEXT | Texto da mensagem |
| tipo_resposta | ENUM | 'fixa', 'sql', 'text' |
| sql_gerado | TEXT | SQL executado (opcional) |
| resultado_sql | TEXT | Resultado do SQL (opcional) |
| data_criacao | DATETIME | Timestamp |
| tokens_utilizados | INT | Para análise de custos |

**Índices:**
- `conversa, data_criacao` (para carregar mensagens ordenadas)
- `tipo` (para análises)

---

## 🔧 Funcionalidades

### Backend (Python/Django - cronos/views.py)

**Funções criadas:**

1. **`obter_conversa_ativa(usuario)`**
   - Obtém ou cria a conversa activa para o utilizador
   - Se não houver conversa aberta, cria uma nova

2. **`salvar_mensagens(conversa, pergunta, resposta, tipo_resposta)`**
   - Salva a pergunta e resposta no banco
   - Atualiza contador de mensagens na conversa

3. **`fechar_conversa(conversa)`**
   - Marca a conversa como inactiva
   - Define `data_fim`

**Endpoints AJAX (JSON):**

1. **POST `/cronos/perguntar/`**
   - Agora salva automaticamente cada pergunta/resposta no banco
   - Antes: apenas em sessionStorage
   - Após resposta fixa ou SQL, chama `salvar_mensagens()`

2. **GET `/cronos/conversas/`**
   - Lista todas as conversas do utilizador autenticado
   - Retorna: `{ conversas: [...], total: N }`
   - Cada conversa: `{ id, titulo, data_inicio, num_mensagens, ativa }`

3. **GET `/cronos/conversas/<id>/`**
   - Carrega todas as mensagens de uma conversa específica
   - Retorna: `{ conversa: {...}, mensagens: [...] }`
   - Cada mensagem: `{ id, tipo, conteudo, tipo_resposta, data_criacao }`

4. **POST `/cronos/limpar/`**
   - Fecha a conversa actual (marca como inactiva)
   - Limpa a sessão

---

## 🎨 Frontend (JavaScript/HTML)

### Painel de Histórico

**Mudanças:**

1. **`abrirHistorico()` (MODIFICADA)**
   - Antes: Carregava do sessionStorage
   - Agora: Faz fetch de `/cronos/conversas/`
   - Mostra lista de conversas do banco com data, hora, número de mensagens e status (🔵 ativa / ⚪ inactiva)

2. **`carregarConversa(conversa_id)` (NOVA)**
   - Carrega uma conversa específica do banco
   - Renderiza todas as mensagens (user + assistant) no chat
   - **Não reenvia a pergunta** - apenas exibe o histórico
   - Mantém os botões de copiar e exportar

3. **`fecharHistorico()` (MANTIDA)**
   - Fecha o painel de histórico

4. **`limparHistoricoLocal()` (MODIFICADA)**
   - Agora chama `/cronos/limpar/` para fechar a conversa
   - Remove sessionStorage

5. **Removidas:**
   - `guardarHistorico()` - não precisa mais (salva no banco)
   - `obterHistorico()` - não precisa mais
   - `actualizarContadorHist()` - não precisa mais
   - `reenviarHistorico()` - não precisa mais

---

## 📊 Fluxo de Dados

```
User envia pergunta
        ↓
enviarMensagem() renderiza localmente
        ↓
Fetch para /cronos/perguntar/
        ↓
Backend:
  - obter_conversa_ativa(user)
  - processar resposta (fixa/sql)
  - salvar_mensagens() → banco de dados
        ↓
Frontend mostra resposta
```

**Ao abrir histórico:**
```
Click "Histórico"
        ↓
abrirHistorico() → fetch /cronos/conversas/
        ↓
Backend: retorna lista de conversas do utilizador
        ↓
UI: exibe conversas em painel lateral
        ↓
Click conversa anterior
        ↓
carregarConversa(id) → fetch /cronos/conversas/{id}/
        ↓
Backend: retorna mensagens daquela conversa
        ↓
UI: renderiza chat com histórico (SEM REENVIDAR)
```

---

## 🛡️ Segurança

- ✅ Todas as views protegidas com `@login_required`
- ✅ Utilizador só pode ver suas próprias conversas (filtro `usuario=request.user`)
- ✅ Modelo usa `on_delete=CASCADE` para limpar mensagens quando conversa é apagada

---

## 📝 Admin Django

Registadas as classes:

- **ConversaCronosAdmin**: Gerenciar conversas (lista, filtros, busca)
- **MensagemCronosAdmin**: Gerenciar mensagens (lista, filtros, busca)

Acesso em: `http://localhost:8000/admin/`

---

## 🧪 Testar

1. **Enviar perguntas normalmente**
   - Devem ser salvas automaticamente no banco

2. **Clicar "Histórico"**
   - Deve carregar lista de conversas do banco
   - Mostrar data, hora, número de mensagens, status

3. **Clicar em conversa anterior**
   - Chat deve mostrar as mensagens antigas
   - Sem reenvidar nada

4. **"Nova Conversa"**
   - Fecha conversa actual
   - Limpa chat
   - Próxima pergunta cria nova conversa no banco

---

## 📁 Arquivos Modificados

- `cronos/models.py` - Adicionados ConversaCronos, MensagemCronos
- `cronos/admin.py` - Registrados nas classes admin
- `cronos/views.py` - Adicionadas funções e endpoints
- `cronos/urls.py` - Já existiam as rotas
- `cronos/templates/cronos/agente-ia.html` - Atualizado JavaScript
- `cronos/migrations/0001_initial.py` - Criado automaticamente (não editar)

---

## ⚙️ Configuração

Nenhuma configuração adicional necessária. O sistema usa:
- Django ORM automático
- Session de utilizador autenticado
- Timestamps automáticos (auto_now_add)

---

## 🚀 Próximas Melhorias Possíveis

- [ ] Renomear conversa
- [ ] Apagar conversa específica
- [ ] Exportar conversa completa como PDF
- [ ] Busca dentro do histórico
- [ ] Estatísticas por utilizador (total conversas, mensagens, etc)
- [ ] Marcar mensagens como favoritas
