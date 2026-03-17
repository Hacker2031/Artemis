#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artemis.settings')
django.setup()

from dotenv import load_dotenv
load_dotenv(override=True)

print("Teste Completo: FAISS + Gemini RAG\n")
print("=" * 60)

# Importar as variáveis globais
from cronos import views

# Inicializar
if not views.inicializar_ia():
    print("[ERRO] Falha ao inicializar IA")
    sys.exit(1)

print("[OK] IA Inicializada\n")

# Testar pergunta
pergunta_teste = "O que você sabe sobre os departamentos?"
print(f"[PERGUNTA] {pergunta_teste}\n")

try:
    resposta = views.chain.invoke(pergunta_teste)
    print(f"[RESPOSTA DO GEMINI]\n")
    print(f"{resposta.content}\n")
    print("=" * 60)
    print("\n[SUCESSO] Sistema funcionando perfeitamente!")

except Exception as e:
    print(f"[ERRO] Falha ao processar: {e}")
    import traceback
    traceback.print_exc()
