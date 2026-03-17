import os
import sys
import django
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, text
from langchain_community.document_loaders import DataFrameLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

# Adicionar ao path o diretório pai do projeto Django
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artemis.settings')
django.setup()

# Configurações
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDICE_FAISS = os.path.join(BASE_DIR, 'faiss_index_artemis')

# Configuração do banco
DB_CONFIG = {
    'host': 'localhost',
    'user': os.getenv('DB_USER', 'alcides'),
    'password': os.getenv('DB_PASSWORD', '1234'),
    'database': 'artemis_db',
    'charset': 'utf8mb4'
}

def conectar_banco():
    """Estabelece conexão com o MySQL usando SQLAlchemy"""
    try:
        db_user = DB_CONFIG['user']
        db_password = DB_CONFIG['password']
        db_host = DB_CONFIG['host']
        db_name = DB_CONFIG['database']

        # Usar pymysql como driver (mais compatível com caching_sha2_password)
        engine = create_engine(
            f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}',
            echo=False
        )
        conn = engine.connect()
        print("Conectado ao MySQL")
        return conn
    except Exception as e:
        print(f" Erro ao conectar: {e}")
        return None

def extrair_dados_funcionarios():
    """Extrai dados da tabela funcionarios"""
    conn = conectar_banco()
    if not conn:
        return None

    query = """
    SELECT
        f.f_id,
        f.f_nome,
        c.nome_cargo as cargo,
        d.nome_dpt as departamento,
        f.contacto,
        f.estado,
        f.avaliacao,
        f.naturalidade,
        f.nacionalidade,
        f.sexo,
        f.estado_civil,
        f.banco_nome,
        f.conta_bancaria
    FROM funcionarios f
    LEFT JOIN cargos c ON f.cargo = c.id_cargo
    LEFT JOIN departamentos d ON f.departamento_id = d.id_dpt
    WHERE f.ativo = 1
    """

    try:
        df = pd.read_sql(text(query), conn)
        conn.close()
        print(f"{len(df)} funcionários extraídos")
        return df
    except Exception as e:
        print(f" Erro ao extrair funcionários: {e}")
        conn.close()
        return None

def extrair_dados_cargos():
    """Extrai dados da tabela cargos"""
    conn = conectar_banco()
    if not conn:
        return None

    query = """
    SELECT
        id_cargo,
        nome_cargo,
        descricao,
        requisitos,
        sal_min,
        sal_base,
        sal_max,
        data_criacao,
        ativo
    FROM cargos
    WHERE ativo = 1
    """

    try:
        df = pd.read_sql(text(query), conn)
        conn.close()
        print(f"{len(df)} cargos extraídos")
        return df
    except Exception as e:
        print(f" Erro ao extrair cargos: {e}")
        conn.close()
        return None

def extrair_dados_departamentos():
    """Extrai dados da tabela departamentos"""
    conn = conectar_banco()
    if not conn:
        return None

    query = """
    SELECT
        id_dpt,
        nome_dpt,
        descricao_dpt,
        dpt_pai,
        responsavel_id,
        ativo
    FROM departamentos
    WHERE ativo = 1
    """

    try:
        df = pd.read_sql(text(query), conn)
        conn.close()
        print(f"{len(df)} departamentos extraídos")
        return df
    except Exception as e:
        print(f" Erro ao extrair departamentos: {e}")
        conn.close()
        return None

def extrair_dados_usuarios():
    """Extrai dados da tabela users (para referência)"""
    conn = conectar_banco()
    if not conn:
        return None

    query = """
    SELECT
        id,
        username,
        email,
        first_name,
        last_name,
        is_superuser,
        is_staff,
        is_active
    FROM users
    WHERE is_active = 1
    """

    try:
        df = pd.read_sql(text(query), conn)
        conn.close()
        print(f"{len(df)} usuários extraídos")
        return df
    except Exception as e:
        print(f" Erro ao extrair usuários: {e}")
        conn.close()
        return None

def criar_documentos_para_rag():
    """Cria documentos combinando todos os dados"""
    documentos = []
    
    # Carregar dados
    df_func = extrair_dados_funcionarios()
    df_cargos = extrair_dados_cargos()
    df_dept = extrair_dados_departamentos()
    df_users = extrair_dados_usuarios()
    
    if df_func is not None and not df_func.empty:
        # Criar documentos de funcionários
        for _, row in df_func.iterrows():
            texto = f"""
            FUNCIONÁRIO: {row['f_nome']}
            CARGO: {row['cargo']}
            DEPARTAMENTO: {row['departamento']}
            CONTATO: {row['contacto']}
            EMAIL: {row['email']}
            ESTADO: {row['estado']}
            AVALIAÇÃO: {row['avaliacao']}
            NATURALIDADE: {row['naturalidade']}
            NACIONALIDADE: {row['nacionalidade']}
            SEXO: {row['sexo']}
            ESTADO CIVIL: {row['estado_civil']}
            BANCO: {row['banco_nome']}
            CONTA: {row['conta_bancaria']}
            """
            documentos.append({
                'page_content': texto,
                'metadata': {
                    'tipo': 'funcionario',
                    'id': row['f_id'],
                    'nome': row['f_nome'],
                    'cargo': row['cargo']
                }
            })
    
    if df_cargos is not None and not df_cargos.empty:
        # Criar documentos de cargos
        for _, row in df_cargos.iterrows():
            texto = f"""
            CARGO: {row['nome_cargo']}
            DESCRIÇÃO: {row['descricao']}
            REQUISITOS: {row['requisitos']}
            SALÁRIO MÍNIMO: {row['sal_min']}
            SALÁRIO BASE: {row['sal_base']}
            SALÁRIO MÁXIMO: {row['sal_max']}
            DATA CRIAÇÃO: {row['data_criacao']}
            """
            documentos.append({
                'page_content': texto,
                'metadata': {
                    'tipo': 'cargo',
                    'id': row['id_cargo'],
                    'nome': row['nome_cargo']
                }
            })
    
    if df_dept is not None and not df_dept.empty:
        # Criar documentos de departamentos
        for _, row in df_dept.iterrows():
            texto = f"""
            DEPARTAMENTO: {row['nome_dpt']}
            DESCRIÇÃO: {row['descricao_dpt']}
            DEPARTAMENTO PAI: {row['dpt_pai']}
            RESPONSÁVEL ID: {row['responsavel_id']}
            """
            documentos.append({
                'page_content': texto,
                'metadata': {
                    'tipo': 'departamento',
                    'id': row['id_dpt'],
                    'nome': row['nome_dpt']
                }
            })
    
    print(f"Total de documentos criados: {len(documentos)}")
    return documentos

def criar_indice_faiss():
    """Cria índice FAISS a partir dos documentos"""
    print("\n" + "=" * 50)
    print("CRIANDO ÍNDICE FAISS DO BANCO DE DADOS")
    print("=" * 50)
    
    # Criar documentos
    documentos_dict = criar_documentos_para_rag()
    
    if not documentos_dict:
        print(" Nenhum documento criado")
        return False
    
    # Converter para formato LangChain
    from langchain_core.documents import Document
    documentos = [
        Document(
            page_content=doc['page_content'],
            metadata=doc['metadata']
        ) for doc in documentos_dict
    ]
    
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documentos)
    print(f"{len(documentos)} documentos divididos em {len(chunks)} chunks")
    
    # Criar embeddings
    print("Inicializando embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Criar e salvar índice
    print("Criando índice FAISS...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(INDICE_FAISS)
    
    print(f"Índice salvo em: {INDICE_FAISS}")
    
    # Estatísticas
    print("\nEstatísticas do índice:")
    print(f"   • Total de chunks: {len(chunks)}")
    print(f"   • Tipos de documentos:")
    
    tipos = {}
    for doc in documentos_dict:
        tipo = doc['metadata']['tipo']
        tipos[tipo] = tipos.get(tipo, 0) + 1
    
    for tipo, qtd in tipos.items():
        print(f"     - {tipo}: {qtd}")
    
    return True

def testar_consulta():
    """Testa se o índice foi criado corretamente"""
    print("\n" + "=" * 50)
    print("TESTANDO CONSULTA")
    print("=" * 50)
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    try:
        vectorstore = FAISS.load_local(
            INDICE_FAISS,
            embeddings,
            allow_dangerous_deserialization=True
        )
        
        # Testar busca
        perguntas_teste = [
            "Quem são os funcionários do departamento de Vendas?",
            "Quais são os cargos disponíveis?",
            "Informações sobre o departamento de RH",
            "Funcionários com cargo de Gerente"
        ]
        
        for pergunta in perguntas_teste:
            print(f"\n Pergunta: {pergunta}")
            docs = vectorstore.similarity_search(pergunta, k=2)
            print(f"   Encontrados: {len(docs)} documentos")
            for i, doc in enumerate(docs, 1):
                print(f"   {i}. {doc.metadata['tipo']}: {doc.metadata.get('nome', '')[:50]}")
        
        return True
        
    except Exception as e:
        print(f" Erro ao testar: {e}")
        return False

if __name__ == "__main__":
    if criar_indice_faiss():
        print("\nÍndice FAISS criado com sucesso!")
        testar_consulta()
    else:
        print("\n Falha ao criar índice FAISS")