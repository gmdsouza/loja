import pytest
import interface
from catalogo import buscar_produtos_api

@pytest.mark.integracao
def test_buscar_produtos_api():
    """
    Este teste faz uma chamada REAL para a Fake Store API.
    """
    resultado = buscar_produtos_api()

    assert resultado is not None, "A API não retornou nada."
    assert isinstance(resultado, list), "A resposta da API não é uma lista."
    assert len(resultado) > 0, "A API retornou uma lista vazia."

    primeiro_produto = resultado[0]
    assert isinstance(primeiro_produto, dict), "O item da lista não é um dicionário."
    assert "id" in primeiro_produto, "O produto não tem a chave 'id'."
    assert "title" in primeiro_produto, "O produto não tem a chave 'title'."
    assert "price" in primeiro_produto, "O produto não tem a chave 'price'."

    assert isinstance(primeiro_produto['id'], int), "O tipo do ID não é inteiro."
    assert isinstance(primeiro_produto['title'], str), "O tipo do Título não é texto."
    assert isinstance(primeiro_produto['price'], (int, float)), "O tipo do Preço não é um número."

    print("\n✅ API retornou dados com a estrutura e os tipos corretos. Teste de integração passou com sucesso!")

    print("📦 Produtos retornados pela API durante o teste:")
    interface.mostrar_tabela_produtos(resultado)