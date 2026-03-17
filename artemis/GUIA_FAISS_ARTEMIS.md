# 🤖 Guia de Integração FAISS com Artemis

## ✅ Status Atual
- **FAISS Vector Index**: ✅ Criado e Funcional
- **LangChain RAG Chain**: ✅ Configurado
- **Frontend Chat**: ✅ Interface HTML pronta
- **API Endpoint**: ✅ `/cronos/perguntar/` funcional

## 🚀 Próximos Passos

### 1. Configurar GOOGLE_API_KEY
Edite o arquivo `.env` na raiz do projeto e adicione sua chave:

```bash
# .env
GOOGLE_API_KEY=sua_chave_do_google_aqui
```

Para obter a chave:
1. Acesse [Google AI Studio](https://aistudio.google.com/apikey)
2. Clique em "Create API Key"
3. Copie a chave e cole no `.env`

### 2. Testar a Integração
```bash
python manage.py runserver
```

Acesse: `http://localhost:8000/cronos/` (após fazer login)

### 3. Atualizar o Índice FAISS Regularmente

O script `cronos/refresh.py` está configurado para executar diariamente às 02:00:

```bash
# Executar manualmente:
python cronos/carregar_do_banco.py
```

## 📊 Arquitetura

```
┌─────────────────┐
│   Frontend      │  (agente-ia.html)
│   Chat UI       │◄───── Mensagens AJAX
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Django View   │  (views.py - endpoint: perguntar)
│   /cronos/      │
└────────┬────────┘
         │
         ├──────────────────┬──────────────────┐
         ▼                  ▼                  ▼
    ┌─────────┐     ┌──────────────┐    ┌──────────┐
    │ FAISS   │     │ HuggingFace  │    │ Gemini   │
    │ Index   │     │ Embeddings   │    │ LLM      │
    │(RAG)    │     │(all-MiniLM)  │    │(2.0)     │
    └─────────┘     └──────────────┘    └──────────┘
         │                                    │
         └────────────────┬────────────────────┘
                          ▼
                    ┌────────────┐
                    │ Response   │
                    │ to User    │
                    └────────────┘
```

## 🔧 Componentes Integrados

### Views.py
- `cronosPage()`: Renderiza a página do chat
- `perguntar()`: Endpoint AJAX para processar perguntas
- `inicializar_ia()`: Carrega FAISS e LLM
- `gerar_resposta_rapida()`: Respostas rápidas para palavras-chave

### URLs
```
GET  /cronos/              → cronosPage (exibe chat)
POST /cronos/perguntar/    → perguntar (processa pergunta)
```

### Templates
- `agente-ia.html`: Interface completa do chat
- `layout.html`: Layout base com navegação

### Dados Disponíveis no FAISS

O índice contém informações sobre:
- 📋 **Cargos**: 10 documentos
- 🏢 **Departamentos**: 20 documentos
- 👥 **Usuários**: 5 documentos
- 💼 **Funcionários**: 0 documentos (nenhum registro ativo)

**Total**: 30 documentos embedados

## 💡 Exemplos de Perguntas Possíveis

```
"Fale sobre nossos departamentos"
"Quais são os cargos disponíveis?"
"Como está organizada a empresa?"
"Qual é a função do RH?"
"Quem são os usuários do sistema?"
```

## 🐛 Troubleshooting

### Erro: "Índice FAISS não encontrado"
```
Solução: Execute novamente
python cronos/carregar_do_banco.py
```

### Erro: "GOOGLE_API_KEY não encontrada"
```
Solução:
1. Edite .env e adicione GOOGLE_API_KEY
2. Reinicie o servidor Django
```

### Chat não responde
```
1. Verifique logs do servidor: python manage.py runserver
2. Verifique GOOGLE_API_KEY no .env
3. Tente uma pergunta mais simples
```

## 📈 Procurar de Atualização Automática

O arquivo `refresh.py` já está configurado com APScheduler para:
- Executar **diariamente às 02:00**
- Recarregar dados do banco
- Reconstruir índice FAISS
- Não interrompe o funcionamento do site

Para modificar o horário, edite `refresh.py`:
```python
scheduler.add_job(func=carregar_indice_faiss, trigger="cron", hour=2, minute=0)
```

## 🔐 Segurança

- ✅ Login obrigatório (`@login_required`)
- ✅ CSRF protection no formulário
- ✅ Sanitização de HTML no frontend
- ✅ Tratamento de erros seguro

## 📝 Próximos Passos Futuros

1. **Histórico de Conversas**: Salvar em BD para cada utilizador
2. **Feedback**: Permitir que utilizadores avaliem respostas
3. **Analytics**: Ver perguntas mais frequentes
4. **Custom Knowledge**: Adicionar documentos específicos da empresa
5. **Multi-language**: Suporte para múltiplas idiomas

---

**Status**: 🟢 Pronto para Produção (apenas falta GOOGLE_API_KEY)
