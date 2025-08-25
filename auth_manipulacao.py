# auth_manipulacao.py
from __future__ import annotations

import json
import os
from typing import Any, Dict

try:
    import manipulacaoArquivos as ma  # integração com camada existente
except Exception:
    ma = None  # fallback para open()

DB_PATH = "db.json"  # segue o padrão do projeto de usar caminhos relativos (Pedidos.txt, etc.)


def _garantir_estrutura(dados: Dict[str, Any]) -> Dict[str, Any]:
    if "usuarios" not in dados or not isinstance(dados["usuarios"], list):
        dados["usuarios"] = []
    if "recuperacoes" not in dados or not isinstance(dados["recuperacoes"], dict):
        dados["recuperacoes"] = {}
    return dados


def carregar_db() -> Dict[str, Any]:
    if not os.path.exists(DB_PATH):
        return _garantir_estrutura({})
    try:
        if ma is not None and hasattr(ma, "lerArquivo"):
            f = ma.lerArquivo(DB_PATH, "r")  # type: ignore[misc]
            with f:
                dados = json.load(f)
        else:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                dados = json.load(f)
    except Exception:
        dados = {}
    if not isinstance(dados, dict):
        dados = {}
    return _garantir_estrutura(dados)


def salvar_db(dados: Dict[str, Any]) -> None:
    dados = _garantir_estrutura(dados)
    try:
        if ma is not None and hasattr(ma, "lerArquivo"):
            f = ma.lerArquivo(DB_PATH, "w")  # type: ignore[misc]
            with f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        else:
            with open(DB_PATH, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
    except Exception as e:
        # último recurso: tenta escrever via open
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
