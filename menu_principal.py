import cadastros
import pagamentos
import catalogo
import pedidos
import interface

def exibir_menu_principal():
    while True:
        opcoes = [
            "Cadastros",
            "Pagamentos",
            "Catálogo de Produtos",
            "Pedidos",
            "Sair"
        ]
        interface.mostrar_menu(opcoes, "🏬 MENU PRINCIPAL")
        opcao = input()

        if opcao == "1":
            menu_cadastros()
        elif opcao == "2":
            pagamentos.realizar_pagamento()
        elif opcao == "3":
            catalogo.exibir_catalogo()
        elif opcao == "4":
            pedidos.menu_pedidos()
        elif opcao == "5":
            interface.limpar_tela()
            interface.mensagem_sucesso("👋 Obrigado por usar a loja!")
            break
        else:
            interface.mensagem_alerta("❌ Opção inválida.")
            interface.pausar()

def menu_cadastros():
    while True:
        opcoes = [
            "Cadastrar Produto/Roupa",
            "Excluir Produto",
            "Editar Produto",
            "Voltar"
        ]
        interface.mostrar_menu(opcoes, "📦 MENU DE CADASTROS")
        opcao = input()

        if opcao == "1":
            cadastros.cadastrar_item()
        elif opcao == "2":
            cadastros.excluir_item()
        elif opcao == "3":
            cadastros.editar_item()
        elif opcao == "4":
            break
        else:
            interface.mensagem_alerta("❌ Opção inválida.")
            interface.pausar()
