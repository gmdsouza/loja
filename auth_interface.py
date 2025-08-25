# auth_interface.py
from __future__ import annotations

import interface
from typing import Optional
from rich.panel import Panel
from rich.align import Align


def cabecalho(titulo: str) -> None:
    interface.limpar_tela()
    interface.titulo(titulo)


def painel(texto: str, titulo: Optional[str] = None, estilo: str = "cyan") -> None:
    try:
        interface.console.print(
            Panel(
                Align.center(texto, vertical="middle"),
                title=titulo,
                border_style=estilo,
                padding=(1, 2),
            )
        )
    except Exception:
        # Fallback minimalista se algo mudar em interface
        print(f"[{titulo}] {texto}")


def prompt(label: str, padrao: Optional[str] = None) -> str:
    if padrao is not None:
        return input(f"{label} [{padrao}]: ") or padrao
    return input(f"{label}: ")


def prompt_senha(label: str) -> str:
    # interface não expõe prompt mascarado, então usamos input normal
    return input(f"{label}: ")


def confirmar(label: str, default: bool = True) -> bool:
    sufixo = "S/n" if default else "s/N"
    resp = input(f"{label} ({sufixo}): ").strip().lower()
    if not resp:
        return default
    return resp in ("s", "sim", "y", "yes")


def sucesso(msg: str) -> None:
    interface.mensagem_sucesso(msg)


def alerta(msg: str) -> None:
    interface.mensagem_alerta(msg)


def pausar() -> None:
    interface.pausar()
