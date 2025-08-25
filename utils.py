"""
utils.py
Funções utilitárias pequenas e reutilizáveis.
"""
from __future__ import annotations

import time
from typing import Dict, Any


def agora_epoch() -> int:
    return int(time.time())


def limpar_dict_seguro(d: Dict[str, Any], chaves_sensiveis: set[str]) -> Dict[str, Any]:
    """Retorna uma cópia sem chaves sensíveis (ex.: hashes e salts)."""
    return {k: v for k, v in d.items() if k not in chaves_sensiveis}
