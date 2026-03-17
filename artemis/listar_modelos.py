import os
import sys

# Carregar API key do arquivo .env manualmente
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('GOOGLE_API_KEY'):
            api_key = line.split('=')[1].strip()
            break

import google.generativeai as genai
genai.configure(api_key=api_key)

print("Modelos disponíveis:\n")
for model in genai.list_models():
    name = str(model.name).replace('models/', '')
    print(f"- {name}")
