import pytest
from unittest.mock import patch, MagicMock, call
import requests
import src.services.catalogo as catalogo

@pytest.mark.unitario_catalogo
def test_buscar_produtos_api_sucesso(mocker):
    """Testa a busca de produtos da API com sucesso"""
    mock_produtos = [
        {"id": 1, "title": "Produto A", "price": 10.0},
        {"id": 2, "title": "Produto B", "price": 20.0}
    ]
    
    mock_response = MagicMock()
    mock_response.json.return_value = mock_produtos
    mock_response.raise_for_status.return_value = None
    
    with patch('src.services.catalogo.requests.get', return_value=mock_response):
        resultado = catalogo.buscar_produtos_api()
        
        assert resultado == mock_produtos
        assert len(resultado) == 2

@pytest.mark.unitario_catalogo
def test_buscar_produtos_api_falha(mocker):
    """Testa a busca de produtos quando a API falha"""
    with patch('src.services.catalogo.requests.get', side_effect=requests.RequestException("Erro de conexão")):
        resultado = catalogo.buscar_produtos_api()
        
        assert resultado == []  # Deve retornar lista vazia em caso de erro

@pytest.mark.unitario_catalogo
def test_buscar_produtos_api_erro_http(mocker):
    """Testa a busca de produtos quando a API retorna erro HTTP"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
    
    with patch('src.services.catalogo.requests.get', return_value=mock_response):
        resultado = catalogo.buscar_produtos_api()
        
        assert resultado == []  # Deve retornar lista vazia em caso de erro HTTP

@pytest.mark.unitario_catalogo
def test_exibir_catalogo_sucesso_com_promocao(mocker):
    """Testa exibição do catálogo com filtro promocional"""
    produtos_api = [
        {"id": 1, "title": "Produto A", "price": 50.0},  # < 60
        {"id": 2, "title": "Produto B", "price": 70.0}   # >= 60
    ]
    
    produtos_locais = [
        {"id": 3, "title": "Produto Local", "price": 25.0}  # < 60
    ]
    
    # Mocks
    mocker.patch('src.services.catalogo.buscar_produtos_api', return_value=produtos_api)
    mocker.patch('src.utils.manipulacaoArquivos.lerProdutosLocais', return_value=produtos_locais)
    mocker.patch('src.interface.interface.limpar_tela')
    mocker.patch('src.interface.interface.titulo')
    mocker.patch('src.interface.interface.mostrar_tabela_produtos')
    mocker.patch('src.interface.interface.pausar')
    
    # Simula usuário escolhendo catálogo promocional
    with patch('builtins.input', return_value='S'):
        catalogo.exibir_catalogo()
        
        # Verifica se mostrou apenas produtos com preço < 60
        from src.interface.interface import mostrar_tabela_produtos
        expected_produtos = [
            {"id": 1, "title": "Produto A", "price": 50.0},
            {"id": 3, "title": "Produto Local", "price": 25.0}
        ]
        mostrar_tabela_produtos.assert_called_once_with(expected_produtos)

@pytest.mark.unitario_catalogo
def test_exibir_catalogo_sucesso_sem_promocao(mocker):
    """Testa exibição do catálogo sem filtro promocional"""
    produtos_api = [
        {"id": 1, "title": "Produto A", "price": 50.0},
        {"id": 2, "title": "Produto B", "price": 70.0}
    ]
    
    produtos_locais = [
        {"id": 3, "title": "Produto Local", "price": 25.0}
    ]
    
    # Mocks
    mocker.patch('src.services.catalogo.buscar_produtos_api', return_value=produtos_api)
    mocker.patch('src.utils.manipulacaoArquivos.lerProdutosLocais', return_value=produtos_locais)
    mocker.patch('src.interface.interface.limpar_tela')
    mocker.patch('src.interface.interface.titulo')
    mocker.patch('src.interface.interface.mostrar_tabela_produtos')
    mocker.patch('src.interface.interface.pausar')
    
    # Simula usuário escolhendo catálogo completo
    with patch('builtins.input', return_value='N'):
        catalogo.exibir_catalogo()
        
        # Verifica se mostrou todos os produtos
        from src.interface.interface import mostrar_tabela_produtos
        expected_produtos = produtos_api + produtos_locais
        mostrar_tabela_produtos.assert_called_once_with(expected_produtos)

@pytest.mark.unitario_catalogo
def test_exibir_catalogo_api_falha(mocker):
    """Testa exibição do catálogo quando a API falha"""
    produtos_locais = [
        {"id": 1, "title": "Produto Local", "price": 25.0}
    ]
    
    # Mocks
    mocker.patch('src.services.catalogo.buscar_produtos_api', return_value=[])  # API falhou
    mocker.patch('src.utils.manipulacaoArquivos.lerProdutosLocais', return_value=produtos_locais)
    mocker.patch('src.interface.interface.limpar_tela')
    mocker.patch('src.interface.interface.titulo')
    mocker.patch('src.interface.interface.mensagem_alerta')
    mocker.patch('src.interface.interface.mostrar_tabela_produtos')
    mocker.patch('src.interface.interface.pausar')
    
    with patch('builtins.input', return_value='N'):
        catalogo.exibir_catalogo()
        
        # Verifica que mostrou mensagem de alerta
        from src.interface.interface import mensagem_alerta
        mensagem_alerta.assert_called_once_with("❌ Erro ao acessar a Fake Store API.")
        
        # Verifica que mostrou os produtos locais
        from src.interface.interface import mostrar_tabela_produtos
        mostrar_tabela_produtos.assert_called_once_with(produtos_locais)

@pytest.mark.unitario_catalogo
def test_exibir_catalogo_sem_produtos(mocker):
    """Testa exibição do catálogo quando não há produtos"""
    # Mocks
    mocker.patch('src.services.catalogo.buscar_produtos_api', return_value=[])  # API vazia
    mocker.patch('src.utils.manipulacaoArquivos.lerProdutosLocais', return_value=[])  # Locais vazios
    mocker.patch('src.interface.interface.limpar_tela')
    mocker.patch('src.interface.interface.titulo')
    mock_mensagem_alerta = mocker.patch('src.interface.interface.mensagem_alerta')
    mocker.patch('src.interface.interface.mostrar_tabela_produtos')
    mocker.patch('src.interface.interface.pausar')
    
    with patch('builtins.input', return_value='N'):
        catalogo.exibir_catalogo()
        
        # Verifica que mostrou mensagem de nenhum produto
        mock_mensagem_alerta.assert_called_with("Nenhum produto para exibir.")

@pytest.mark.unitario_catalogo
def test_exibir_catalogo_input_invalido(mocker):
    """Testa exibição do catálogo com input inválido (default para não promocional)"""
    produtos_api = [
        {"id": 1, "title": "Produto A", "price": 50.0},
        {"id": 2, "title": "Produto B", "price": 70.0}
    ]
    
    # Mocks
    mocker.patch('src.services.catalogo.buscar_produtos_api', return_value=produtos_api)
    mocker.patch('src.utils.manipulacaoArquivos.lerProdutosLocais', return_value=[])
    mocker.patch('src.interface.interface.limpar_tela')
    mocker.patch('src.interface.interface.titulo')
    mocker.patch('src.interface.interface.mostrar_tabela_produtos')
    mocker.patch('src.interface.interface.pausar')
    
    # Simula input inválido (qualquer coisa que não seja 'S')
    with patch('builtins.input', return_value='X'):
        catalogo.exibir_catalogo()
        
        # Verifica que mostrou todos os produtos (comportamento default)
        from src.interface.interface import mostrar_tabela_produtos
        mostrar_tabela_produtos.assert_called_once_with(produtos_api)

@pytest.mark.integracao_catalogo
def test_exibir_catalogo_integracao(mocker):
    """Teste de integração do fluxo completo do catálogo"""
    produtos_api = [
        {"id": 1, "title": "Produto API", "price": 45.0}
    ]
    
    produtos_locais = [
        {"id": 2, "title": "Produto Local", "price": 30.0}
    ]
    
    # Mocks
    mocker.patch('src.services.catalogo.buscar_produtos_api', return_value=produtos_api)
    mocker.patch('src.utils.manipulacaoArquivos.lerProdutosLocais', return_value=produtos_locais)
    mocker.patch('src.interface.interface.limpar_tela')
    mocker.patch('src.interface.interface.titulo')
    mocker.patch('src.interface.interface.mostrar_tabela_produtos')
    mocker.patch('src.interface.interface.pausar')
    
    # Fluxo completo
    with patch('builtins.input', return_value='S'):  # Catálogo promocional
        catalogo.exibir_catalogo()
        
        # Verificações
        from src.interface.interface import mostrar_tabela_produtos
        mostrar_tabela_produtos.assert_called_once()