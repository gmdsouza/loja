"""
validators.py
Validações de campos de usuário e utilidades de sanitização.
"""
from __future__ import annotations

import re
from typing import Tuple


RE_EMAIL = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
RE_USERNAME = re.compile(r"^[a-zA-Z0-9_.-]{3,20}$")


def validar_email(email: str) -> Tuple[bool, str]:
    if not email:
        return False, "E-mail é obrigatório."
    if not RE_EMAIL.match(email):
        return False, "E-mail inválido."
    return True, ""


def validar_username(username: str) -> Tuple[bool, str]:
    if not username:
        return False, "Username é obrigatório."
    if not RE_USERNAME.match(username):
        return False, "Username deve ter 3-20 caracteres e conter apenas letras, números e ._-."
    return True, ""


def validar_senha(senha: str) -> Tuple[bool, str]:
    """
    Critérios práticos para CLI:
    - mínimo 6 caracteres
    - deve conter letra e número
    """
    if not senha or len(senha) < 6:
        return False, "Senha deve ter pelo menos 6 caracteres."
    if not any(c.isalpha() for c in senha) or not any(c.isdigit() for c in senha):
        return False, "Senha deve conter letras e números."
    return True, ""
