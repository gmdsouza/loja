import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from typing import Optional

console = Console()

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def titulo(texto):
    panel = Panel.fit(
        f"[bold cyan]{texto}[/bold cyan]",
        border_style="cyan",
        padding=(1, 4),
        title="🛍️ Nova Loja em Microsserviços",
        subtitle="Tópicos de Eng. de Software"
    )
    console.print(panel)

def cabecalho(titulo_texto: str) -> None:
    limpar_tela()
    titulo(titulo_texto)

def painel(texto: str, titulo_painel: Optional[str] = None, estilo: str = "cyan") -> None:
    try:
        console.print(
            Panel(
                Align.center(texto, vertical="middle"),
                title=titulo_painel,
                border_style=estilo,
                padding=(1, 2),
            )
        )
    except Exception:
        print(f"[{titulo_painel}] {texto}")

def mostrar_menu(opcoes, titulo_menu="MENU"):
    limpar_tela()
    titulo(titulo_menu)
    for i, opcao in enumerate(opcoes, 1):
        console.print(f"[green]{i}[/green] - {opcao}")
    console.print("[yellow]Escolha uma opção: [/yellow]", end="")

def mostrar_tabela_produtos(produtos):
    table = Table(title="📦 Produtos Disponíveis", header_style="bold magenta")
    table.add_column("ID", justify="center")
    table.add_column("Nome")
    table.add_column("Preço (R$)", justify="right")

    for p in produtos:
        table.add_row(str(p["id"]), p["title"], f"R$ {p['price']:.2f}")

    console.print(table)

def mostrar_tabela_pedidos(pedidos):
    table = Table(title="🧾 Itens no Pedido", header_style="bold yellow")
    table.add_column("#", justify="center")
    table.add_column("Nome")
    table.add_column("Preço (R$)", justify="right")

    for i, item in enumerate(pedidos, 1):
        table.add_row(str(i), item[1], f"R$ {item[2]:.2f}")

    console.print(table)

def mensagem_alerta(texto):
    console.print(f"[bold red]{texto}[/bold red]")

def mensagem_sucesso(texto):
    console.print(f"[bold green]{texto}[/bold green]")

def prompt(label: str, padrao: Optional[str] = None) -> str:
    if padrao is not None:
        return console.input(f"{label} [dim][{padrao}]: [/dim]") or padrao
    return console.input(f"{label}: ")

def prompt_senha(label: str) -> str:
    return console.input(f"{label}: ", password=True)

def confirmar(label: str, default: bool = True) -> bool:
    sufixo = "[S/n]" if default else "[s/N]"
    resp = console.input(f"{label} {sufixo}: ").strip().lower()
    if not resp:
        return default
    return resp in ("s", "sim", "y", "yes")

def pausar():
    console.print("\n[dim]Pressione [bold]Enter[/bold] para continuar...[/dim]")
    input()