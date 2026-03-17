from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# Configurações
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDICE_FAISS = os.path.join(BASE_DIR, 'faiss_index_artemis')

# Variáveis globais da IA
llm = None
embeddings = None
vectorstore = None
chain = None

def inicializar_ia():
    global llm, embeddings, vectorstore, chain
    
    if llm is not None:
        return True
    
    print("Inicializando IA...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY não encontrada")
        return False
    
    try:
        # Inicializar LLM (Gemini)
        llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash",
            temperature=0.3,
            timeout=60,
            max_retries=3,
            google_api_key=api_key
        )
        
        # Inicializar embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Carregar índice FAISS
        if os.path.exists(INDICE_FAISS):
            vectorstore = FAISS.load_local(
                INDICE_FAISS,
                embeddings,
                allow_dangerous_deserialization=True
            )
            
            # Configurar chain RAG
            retriever = vectorstore.as_retriever(
                search_kwargs={"k": 4}
            )
            
            template = """
            Você é o CRONOS, assistente de IA especializado em ERP da empresa Artemis.
            Use o contexto abaixo para responder perguntas sobre a empresa.
            Seja direto, profissional e use formatação HTML simples quando apropriado.
            Se não encontrar a resposta, sugira perguntas relacionadas.
            
            Contexto da empresa:
            {context}
            
            Histórico da conversa: {historico}
            
            Pergunta atual: {question}
            
            Resposta:
            """
            
            prompt = ChatPromptTemplate.from_template(template)
            
            def formatar_docs(docs):
                return "\n\n---\n\n".join([d.page_content for d in docs])
            
            chain = (
                {
                    "context": retriever | formatar_docs,
                    "historico": lambda x: "",  # Placeholder para histórico
                    "question": RunnablePassthrough()
                }
                | prompt
                | llm
            )
            
            print("IA inicializada com sucesso")
            return True
        else:
            print(f"Índice FAISS não encontrado. Execute carregar_do_banco.py primeiro")
            return False
            
    except Exception as e:
        print(f"Erro ao inicializar IA: {e}")
        return False

@login_required(login_url='loginPage')
def cronosPage(request):
    return render(request, "cronos/agente-ia.html")
 

@login_required(login_url='loginPage')
def perguntar(request):
    """Endpoint para processar perguntas via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        pergunta = data.get('pergunta', '').strip()
        
        if not pergunta:
            return JsonResponse({'erro': 'Pergunta vazia'}, status=400)
        
        # Inicializar IA se necessário
        if not inicializar_ia():
            return JsonResponse({
                'erro': 'IA não inicializada. Execute o carregamento da base primeiro.'
            }, status=500)
        
        # Processar pergunta
        if chain is None:
            return JsonResponse({'erro': 'Cadeia de IA não configurada'}, status=500)
        
        # Respostas rápidas para palavras-chave (fallback)
        resposta_rapida = gerar_resposta_rapida(pergunta)
        if resposta_rapida:
            return JsonResponse({
                'resposta': resposta_rapida,
                'pergunta': pergunta,
                'tipo': 'rapida'
            })
        
        # Usar RAG
        response = chain.invoke(pergunta)
        
        return JsonResponse({
            'resposta': response.content,
            'pergunta': pergunta,
            'tipo': 'rag'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)

def gerar_resposta_rapida(pergunta):
    """Gera respostas rápidas para palavras-chave comuns"""
    p = pergunta.lower()
    
    if 'venda' in p or 'vendas' in p:
        return """
        <strong>📊 Análise de Vendas</strong><br><br>
        • Total do mês: 875.500 Kz (+23.5%)<br>
        • Melhor produto: Laptop HP (245 unidades)<br>
        • Melhor vendedor: Ana Silva<br>
        • Taxa de conversão: 34.2%<br><br>
        <strong>💡 Insight:</strong> Há uma tendência de crescimento nos produtos eletrónicos. Recomendo aumentar o stock desta categoria.
        """
    
    if 'stock' in p or 'previsão' in p:
        return """
        <strong>📦 Previsão de Stock (próximos 7 dias)</strong><br><br>
        ⚠️ <strong>Alertas:</strong><br>
        • Mouse Wireless: esgota em 3 dias<br>
        • Teclado Mecânico: stock adequado (45 unidades)<br>
        • Laptop HP: demanda +45%<br><br>
        🎯 <strong>Recomendação:</strong> Reabastecer urgente: Mouse Wireless (50 unidades)
        """
    
    if 'equipe' in p or 'performance' in p or 'equipa' in p:
        return """
        <strong>👥 Performance da Equipe</strong><br><br>
        ⭐ <strong>Destaques:</strong><br>
        • Equipe TI: 15% acima da meta<br>
        • Vendas: performance excelente (92%)<br>
        • RH: dentro do esperado<br>
        • Produção: 3% abaixo da meta<br><br>
        💡 <strong>Sugestão:</strong> Considere treinamento para equipe de produção
        """
    
    if 'relatório' in p or 'relatorio' in p:
        return """
        <strong>📋 Relatórios Disponíveis</strong><br><br>
        • Relatório de Vendas (diário/semanal/mensal)<br>
        • Relatório de Stock<br>
        • Relatório de Performance<br>
        • Relatório Financeiro<br>
        • Relatório de RH<br><br>
        Qual relatório específico você precisa?
        """
    
    return None