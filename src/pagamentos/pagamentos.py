import src.utils.manipulacaoArquivos as manipulacaoArquivos
import json
import src.interface.interface as interface

def realizar_pagamento():
    interface.limpar_tela()
    interface.titulo("💳 PAGAMENTO DE PEDIDOS")

    try:
        arquivo = manipulacaoArquivos.lerArquivo("Pedidos.txt", "r")
        pedidos = arquivo.readlines()
        arquivo.close()

        if not pedidos:
            interface.mensagem_alerta("⚠️ Nenhum pedido encontrado.")
            interface.pausar()
            return

        soma = 0.0
        for linha in pedidos:
            try:
                partes = linha.strip().split(";", 1)
                if len(partes) < 2:
                    continue
                lista = json.loads(partes[1])
                for item in lista:
                    soma += float(item["preco"])
            except Exception as e:
                interface.mensagem_alerta(f"Erro ao processar linha: {linha} → {e}")

        print(f"\n🧾 Valor total dos pedidos: R$ {soma:.2f}")
        print("\nSelecione a forma de pagamento:")
        print("1 - Crédito")
        print("2 - Débito")
        print("3 - Dinheiro")

        opcao = input("\nDigite o número da opção: ").strip()

        metodos = {"1": "crédito", "2": "débito", "3": "dinheiro"}

        if opcao not in metodos:
            interface.mensagem_alerta("❌ Opção inválida. Pressione ENTER para voltar ao menu.")
            input()
            return

        metodo = metodos[opcao]
        interface.mensagem_sucesso(f"✅ Pagamento de R$ {soma:.2f} realizado via {metodo.upper()}!")

        with open("Pedidos.txt", "w") as f:
            f.truncate()

        interface.mensagem_sucesso("🧾 Pedidos quitados e arquivo zerado.")
    except FileNotFoundError:
        interface.mensagem_alerta("❌ Arquivo de pedidos não encontrado.")

    interface.pausar()
