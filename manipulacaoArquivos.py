import os
import json
from datetime import datetime

def gravarProdutoFakeStore(id, title, price, description):
    with open("produtos_local.txt", "a") as f:
        f.write(f"{id};{title};{price};{description}\n")

def lerProdutosLocais():
    try:
        with open("produtos_local.txt", "r") as f:
            produtos = []
            for linha in f:
                partes = linha.strip().split(";")
                if len(partes) == 4:
                    id_, title, price, description = partes
                    produtos.append({
                        "id": int(id_),
                        "title": title,
                        "price": float(price),
                        "description": description
                    })
            return produtos
    except FileNotFoundError:
        return []

def gravarPedidos(listaPedido, datahora):
    # Convertemos para lista de dicts para evitar problemas com json.dumps em tuplas
    lista_dict = [{"id": item[0], "nome": item[1], "preco": item[2]} for item in listaPedido]
    with open("Pedidos.txt", "a") as f:
        f.write(f"{datahora};{json.dumps(lista_dict)}\n")

def lerArquivo(nome, modo="r"):
    return open(nome, modo)

def apagarArquivosTemporarios():
    for arquivo in ["produtos_local.txt", "Pedidos.txt"]:
        if os.path.exists(arquivo):
            os.remove(arquivo)
