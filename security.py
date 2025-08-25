"""
security.py
Utilitários de segurança simples e sem dependências externas.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Tuple


def hash_texto(texto: str, salt: str) -> str:
    """Retorna o hexdigest SHA-256 de (salt + texto)."""
    return hashlib.sha256((salt + texto).encode("utf-8")).hexdigest()


def hash_senha(senha: str, salt: str | None = None) -> Tuple[str, str]:
    """Gera hash+salt para senha (compatível com a base do projeto)."""
    if salt is None:
        salt = secrets.token_hex(16)  # 16 bytes em hex
    return hash_texto(senha, salt), salt


def consteq(a: str, b: str) -> bool:
    """Comparação em tempo constante."""
    return hmac.compare_digest(a, b)
