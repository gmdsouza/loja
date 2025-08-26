from __future__ import annotations

from typing import Optional, Dict, Any
from interface import pausar, mensagem_alerta, mensagem_sucesso, cabecalho, mostrar_menu, prompt, prompt_senha, confirmar, painel
from usuarios import criar_usuario, validar_login, iniciar_recuperacao, concluir_recuperacao
from logs import get_logger

log = get_logger("auth")


def _abrir_menu_pos_login(usuario: Dict[str, Any]) -> None:
    try:
        import menu_principal as mp  # type: ignore
    except Exception:
        log.exception("menu_principal não encontrado")
        mensagem_alerta("Login ok, mas não encontrei o módulo 'menu_principal'.")
        pausar()
        return

    fn = getattr(mp, "exibir_menu_principal", None)
    if callable(fn):
        try:
            fn()  # o menu atual não recebe usuário
            return
        except Exception as e:
            log.exception("Erro abrindo menu_principal")
            mensagem_alerta(f"Erro ao abrir o menu: {e}")
            pausar()
            return

    mensagem_alerta("Não encontrei a função 'exibir_menu_principal' em menu_principal.")
    pausar()


def tela_login() -> Optional[Dict[str, Any]]:
    while True:
        cabecalho("🔐 LOGIN")
        opcoes = [
            "Entrar",
            "Cadastrar Conta",
            "Esqueci Minha Senha",
            "Sair"
        ]
        mostrar_menu(opcoes, "🔐 BEM-VINDO À LOJA")
        opcao = input()
        
        if opcao == "1":
            result = handle_login_option()
            if result is not None:
                return result
        elif opcao == "2":
            handle_signup_option()
        elif opcao == "3":
            handle_forgot_password_option()
        elif opcao == "4":
            return None
        else:
            handle_invalid_option()


def handle_login_option() -> Optional[Dict[str, Any]]:
    login = prompt("Usuário ou e-mail")
    senha = prompt_senha("Senha")
    ok, usuario, msg = validar_login(login, senha)
    
    if ok and usuario:
        log.info("Login bem-sucedido para '%s'", login)
        mensagem_sucesso("✅ Login realizado com sucesso!")
        pausar()
        return usuario
    else:
        log.info("Falha de login para '%s': %s", login, msg)
        mensagem_alerta(msg)
        if not confirmar("Tentar novamente?"):
            return None
    return None


def handle_signup_option():
    if tela_cadastro():
        mensagem_sucesso("Conta criada! Faça login.")
        pausar()


def handle_forgot_password_option():
    tela_esqueci_senha()


def handle_invalid_option():
    mensagem_alerta("Opção inválida.")
    pausar()


def tela_cadastro() -> bool:
    cabecalho("🆕 CADASTRO DE USUÁRIO")
    
    # Usar a função prompt do interface consolidado
    username = prompt("Username")
    nome = prompt("Nome completo")
    email = prompt("E-mail")
    senha = prompt_senha("Senha")
    confirma = prompt_senha("Confirmar senha")

    if senha != confirma:
        mensagem_alerta("As senhas não conferem.")
        return False

    pergunta = prompt("Pergunta de segurança (para recuperar senha)")
    resposta = prompt("Resposta")

    ok, msg = criar_usuario(username, nome, email, senha, pergunta, resposta)
    if not ok:
        mensagem_alerta(msg)
        return False
        
    log.info("Usuário criado: %s", username)
    mensagem_sucesso("✅ Usuário criado com sucesso!")
    return True


def tela_esqueci_senha() -> None:
    cabecalho("❓ ESQUECI MINHA SENHA")
    login = prompt("Informe seu usuário ou e-mail")
    ok, token, pergunta = iniciar_recuperacao(login)
    
    if not ok:
        mensagem_alerta(token)
        pausar()
        return

    # Usar painel do interface consolidado
    painel(
        f"Responda à pergunta de segurança:\n\n[b]{pergunta}[/b]\n\n"
        f"[dim]Um token temporário foi gerado e expira em 15 minutos.[/dim]",
        "Verificação",
        "cyan"
    )
    
    resposta = prompt("Resposta")
    nova1 = prompt_senha("Nova senha")
    nova2 = prompt_senha("Confirmar nova senha")
    
    if nova1 != nova2:
        mensagem_alerta("As senhas não conferem.")
        pausar()
        return

    ok2, msg2 = concluir_recuperacao(token, resposta, nova1)
    if ok2:
        log.info("Senha redefinida para login '%s'", login)
        mensagem_sucesso(msg2)
    else:
        log.info("Falha na redefinição de senha para '%s': %s", login, msg2)
        mensagem_alerta(msg2)
        
    pausar()


def iniciar_sistema() -> None:
    log.info("Aplicação iniciada")
    usuario = tela_login()
    if usuario:
        _abrir_menu_pos_login(usuario)

