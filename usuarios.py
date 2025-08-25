# usuarios.py
from __future__ import annotations

import hashlib
import hmac
import secrets
import time
from typing import Dict, Any, Optional, Tuple, List

from auth_manipulacao import carregar_db, salvar_db


def _hash_texto(texto: str, salt: str) -> str:
    return hashlib.sha256((salt + texto).encode("utf-8")).hexdigest()


def _hash_senha(senha: str, salt: Optional[str] = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    return _hash_texto(senha, salt), salt


def _const_eq(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)


def listar_usuarios() -> List[Dict[str, Any]]:
    db = carregar_db()
    return db.get("usuarios", [])


def buscar_usuario_por_login(login: str) -> Optional[Dict[str, Any]]:
    db = carregar_db()
    for u in db.get("usuarios", []):
        if u.get("username") == login or u.get("email") == login:
            return u
    return None


def criar_usuario(username: str, nome: str, email: str, senha: str,
                  pergunta: str, resposta: str) -> tuple[bool, str]:
    if not username or not email or not senha:
        return False, "Preencha username, e-mail e senha."

    db = carregar_db()

    for u in db["usuarios"]:
        if u.get("username") == username:
            return False, "Já existe um usuário com esse username."
        if u.get("email") == email:
            return False, "Já existe um usuário com esse e-mail."

    senha_hash, senha_salt = _hash_senha(senha)
    resp_hash, resp_salt = _hash_senha(resposta)

    novo = {
        "id": secrets.token_hex(8),
        "username": username,
        "nome": nome,
        "email": email,
        "senha_hash": senha_hash,
        "senha_salt": senha_salt,
        "pergunta": pergunta,
        "resposta_hash": resp_hash,
        "resposta_salt": resp_salt,
        "criado_em": int(time.time()),
        "ativo": True,
        "roles": ["cliente"],
    }
    db["usuarios"].append(novo)
    salvar_db(db)
    return True, "Usuário criado com sucesso."


def validar_login(login: str, senha: str) -> tuple[bool, Optional[Dict[str, Any]], str]:
    u = buscar_usuario_por_login(login)
    if not u:
        return False, None, "Usuário não encontrado."
    if not u.get("ativo", True):
        return False, None, "Usuário inativo."

    hash_informado = _hash_texto(senha, u.get("senha_salt", ""))
    if not _const_eq(hash_informado, u.get("senha_hash", "")):
        return False, None, "Senha inválida."

    # Retorna uma versão sem hashes
    publico = {k: v for k, v in u.items() if k not in ("senha_hash", "senha_salt", "resposta_hash", "resposta_salt")}
    return True, publico, "Login OK."


def iniciar_recuperacao(login: str) -> tuple[bool, str, Optional[str]]:
    db = carregar_db()
    u = buscar_usuario_por_login(login)
    if not u:
        return False, "Usuário não encontrado.", None

    token = secrets.token_urlsafe(16)
    db.setdefault("recuperacoes", {})
    db["recuperacoes"][token] = {
        "user_id": u["id"],
        "expira_em": int(time.time()) + 15 * 60,
    }
    salvar_db(db)
    return True, token, u.get("pergunta") or "Pergunta de segurança"


def concluir_recuperacao(token: str, resposta: str, nova_senha: str) -> tuple[bool, str]:
    db = carregar_db()
    rec = db.get("recuperacoes", {}).get(token)
    if not rec:
        return False, "Token inválido."
    if rec["expira_em"] < int(time.time()):
        # expirada
        try:
            del db["recuperacoes"][token]
            salvar_db(db)
        except Exception:
            pass
        return False, "Token expirado. Inicie novamente."

    uid = rec["user_id"]
    usuario = None
    for u in db["usuarios"]:
        if u.get("id") == uid:
            usuario = u
            break
    if not usuario:
        return False, "Usuário não encontrado."

    resp_hash = _hash_texto(resposta, usuario.get("resposta_salt", ""))
    if not _const_eq(resp_hash, usuario.get("resposta_hash", "")):
        return False, "Resposta incorreta."

    nova_hash, nova_salt = _hash_senha(nova_senha)
    usuario["senha_hash"] = nova_hash
    usuario["senha_salt"] = nova_salt

    try:
        del db["recuperacoes"][token]
    except Exception:
        pass

    salvar_db(db)
    return True, "Senha redefinida com sucesso."
