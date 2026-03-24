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
from langchain_core.runnables import RunnablePassthrough, RunnableLambda


_ = load_dotenv()

# Configurações
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDICE_FAISS = os.path.join(BASE_DIR, 'faiss_index_artemis')

# Variáveis globais da IA
llm = None
embeddings = None
vectorstore = None
chain = None
retriever = None
"""""
historico = request.session.get("chat_history", [])

historico.append(pergunta)

request.session["chat_history"] = historico[-5:]
"""""

def inicializar_ia():
    global llm, embeddings, vectorstore, chain, retriever
    
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
            model="gemini-3-flash-preview",
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
                search_type="mmr",
                search_kwargs={
                    "k": 6,
                    "fetch_k": 20
                }
            )

            
            template = """
            Você é o CRONOS, um agente de inteligência artificial integrado ao ERP da empresa.

            Função:
            Consultar dados da empresa, gerar relatórios, explicar informações e responder perguntas básicas.

            Regras:
            - Utilize apenas informações presentes no contexto fornecido ou em fatos amplamente conhecidos.
            - Nunca invente dados.
            - Se a informação não existir ou não for confiável, diga que não sabe.
            - Pode fazer inferências simples baseadas nos dados (ex: identificar o responsável ou líder de um setor).
            - Não tome decisões empresariais.
            - Evite respostas exageradas ou especulativas.
            - Responda de forma clara, objetiva e baseada em dados.
            - Sempre priorize informações presentes na base de dados da empresa.
            - Se a pergunta não estiver relacionada com a base ou não for um fato conhecido, informe que não possui dados suficientes.
            - Não invente números, nomes ou dados empresariais.
            - Caso a pergunta exija dados específicos que não estejam no contexto, responda que a informação não está disponível.
            -Se o contexto contiver dados parciais, use o que tiver disponível.
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
                    "context": (RunnableLambda(lambda x: x["question"]) | retriever | formatar_docs),
                    "historico": RunnableLambda(lambda x: x.get("historico", "")),
                    "question": RunnableLambda(lambda x: x["question"])
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
        docs = retriever.invoke(pergunta)

        if not docs:
            return JsonResponse({
                "resposta": "Não encontrei informação na base de dados.",
                "tipo": "sem_dados"
            })

        response = chain.invoke({
            "question": pergunta,
            "historico": ""
        })

        # Extrair texto da resposta
        if hasattr(response, 'content'):
            # Se for um objeto com atributo content
            if isinstance(response.content, list):
                resposta_texto = '\n'.join([
                    block.get('text', '') if isinstance(block, dict) else str(block)
                    for block in response.content
                ])
            else:
                resposta_texto = str(response.content)
        elif isinstance(response, dict):
            # Se for um dicionário
            resposta_texto = response.get('text', response.get('content', str(response)))
        else:
            # Caso contrário, converter para string
            resposta_texto = str(response)

        return JsonResponse({
            'resposta': resposta_texto,
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

    # Informações institucionais do sistema

    if 'quem criou o artemis' in p or 'criador do artemis' in p:
        return "O sistema Artemis foi desenvolvido por Alcides Nolasco como um ERP para gestão empresarial."

    if 'quem criou o cronos' in p or 'criador do cronos' in p:
        return "O Cronos foi desenvolvido por Alcides Nolasco como o agente de inteligência artificial integrado ao sistema Artemis."

    if 'o que é o artemis' in p:
        return "Artemis é um sistema ERP utilizado para gestão de dados empresariais, incluindo vendas, stock, relatórios e operações internas."

    if 'o que é o cronos' in p:
        return "Cronos é um agente de inteligência artificial integrado ao sistema Artemis responsável por consultar dados, gerar relatórios e responder perguntas sobre a empresa."

    if 'o que o cronos faz' in p or 'função do cronos' in p:
        return "Cronos analisa dados do ERP, consulta informações na base de dados, gera relatórios e auxilia na interpretação de informações empresariais."
