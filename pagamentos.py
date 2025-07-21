import manipulacaoArquivos
import json
import interface

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
        metodo = input("💰 Forma de pagamento (crédito/débito/dinheiro): ")
        interface.mensagem_sucesso(f"✅ Pagamento de R$ {soma:.2f} realizado via {metodo.upper()}!")

        with open("Pedidos.txt", "w") as f:
            f.truncate()

        interface.mensagem_sucesso("🧾 Pedidos quitados e arquivo zerado.")
    except FileNotFoundError:
        interface.mensagem_alerta("❌ Arquivo de pedidos não encontrado.")
    interface.pausar()
