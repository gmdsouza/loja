import requests
import manipulacaoArquivos
import interface

def exibir_catalogo():
    interface.limpar_tela()
    interface.titulo("🛍️ CATÁLOGO DE PRODUTOS")
    promocao = input("Deseja ver o catálogo promocional (preço < R$60)? [S/N]: ").strip().upper()

    try:
        res = requests.get("https://fakestoreapi.com/products")
        produtos_api = res.json() if res.status_code == 200 else []
    except:
        interface.mensagem_alerta("❌ Erro ao acessar a Fake Store API.")
        produtos_api = []

    produtos_locais = manipulacaoArquivos.lerProdutosLocais()
    todos_produtos = produtos_api + produtos_locais

    filtrados = [p for p in todos_produtos if p["price"] < 60] if promocao == "S" else todos_produtos

    interface.mostrar_tabela_produtos(filtrados)
    interface.pausar()
