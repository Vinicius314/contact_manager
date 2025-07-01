import json
import os

ARQUIVO = "contatos.json"

def carregar_contatos():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_contatos(contatos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(contatos, f, indent=2, ensure_ascii=False)
