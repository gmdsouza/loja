import pytest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
from datetime import datetime
from src.utils import manipulacaoArquivos

@pytest.mark.unitario_arquivos
def test_gravar_produto_fakestore(mocker):
    """Testa a gravação de produto no arquivo local"""
    mock_file = mock_open()
    
    with patch('builtins.open', mock_file):
        manipulacaoArquivos.gravarProdutoFakeStore(123, "Produto Teste", 25.99, "Descrição teste")
        
        # Verifica se o arquivo foi aberto no modo append
        mock_file.assert_called_once_with("produtos_local.txt", "a")
        
        # Verifica se a linha foi escrita corretamente
        handle = mock_file()
        handle.write.assert_called_once_with("123;Produto Teste;25.99;Descrição teste\n")

@pytest.mark.unitario_arquivos
def test_ler_produtos_locais_existente(mocker):
    """Testa a leitura de produtos quando o arquivo existe"""
    conteudo_fake = "1;Produto A;10.5;Descrição A\n2;Produto B;20.0;Descrição B\n"
    
    with patch('builtins.open', mock_open(read_data=conteudo_fake)):
        resultado = manipulacaoArquivos.lerProdutosLocais()
        
        assert len(resultado) == 2
        assert resultado[0]["id"] == 1
        assert resultado[0]["title"] == "Produto A"
        assert resultado[0]["price"] == 10.5
        assert resultado[0]["description"] == "Descrição A"
        
        assert resultado[1]["id"] == 2
        assert resultado[1]["title"] == "Produto B"
        assert resultado[1]["price"] == 20.0
        assert resultado[1]["description"] == "Descrição B"

@pytest.mark.unitario_arquivos
def test_ler_produtos_locais_arquivo_inexistente(mocker):
    """Testa a leitura de produtos quando o arquivo não existe"""
    with patch('builtins.open', side_effect=FileNotFoundError):
        resultado = manipulacaoArquivos.lerProdutosLocais()
        assert resultado == []  # Deve retornar lista vazia

@pytest.mark.unitario_arquivos
def test_ler_produtos_locais_linha_invalida(mocker):
    """Testa a leitura com linha mal formatada"""
    conteudo_fake = "1;Produto A;10.5;Descrição A\nlinha_invalida\n2;Produto B;20.0;Descrição B\n"
    
    with patch('builtins.open', mock_open(read_data=conteudo_fake)):
        resultado = manipulacaoArquivos.lerProdutosLocais()
        
        # Deve ignorar a linha inválida e processar as outras
        assert len(resultado) == 2
        assert resultado[0]["id"] == 1
        assert resultado[1]["id"] == 2

@pytest.mark.unitario_arquivos
def test_gravar_pedidos(mocker):
    """Testa a gravação de pedidos"""
    mock_file = mock_open()
    lista_pedido = [
        (1, "Produto A", 10.0),
        (2, "Produto B", 20.5)
    ]
    datahora = datetime(2024, 1, 15, 10, 30, 0)
    
    with patch('builtins.open', mock_file):
        manipulacaoArquivos.gravarPedidos(lista_pedido, datahora)
        
        # Verifica se o arquivo foi aberto no modo append
        mock_file.assert_called_once_with("Pedidos.txt", "a")
        
        # Verifica se a linha foi escrita corretamente
        handle = mock_file()
        expected_json = json.dumps([{"id": 1, "nome": "Produto A", "preco": 10.0}, 
                                  {"id": 2, "nome": "Produto B", "preco": 20.5}])
        expected_line = f"2024-01-15 10:30:00;{expected_json}\n"
        handle.write.assert_called_once_with(expected_line)

@pytest.mark.unitario_arquivos
def test_ler_arquivo(mocker):
    """Testa a função genérica de leitura de arquivo"""
    mock_file = mock_open(read_data="conteúdo do arquivo")
    
    with patch('builtins.open', mock_file):
        resultado = manipulacaoArquivos.lerArquivo("teste.txt")
        mock_file.assert_called_once_with("teste.txt", "r")

@pytest.mark.unitario_arquivos
def test_ler_arquivo_modo_diferente(mocker):
    """Testa a função de leitura com modo diferente"""
    mock_file = mock_open()
    
    with patch('builtins.open', mock_file):
        resultado = manipulacaoArquivos.lerArquivo("teste.txt", "w")
        mock_file.assert_called_once_with("teste.txt", "w")

@pytest.mark.unitario_arquivos
def test_apagar_arquivos_temporarios_existentes(mocker):
    """Testa a exclusão de arquivos temporários quando existem"""
    mock_remove = mocker.patch('os.remove')
    mock_exists = mocker.patch('os.path.exists', return_value=True)
    
    manipulacaoArquivos.apagarArquivosTemporarios()
    
    # Verifica se os.remove foi chamado para cada arquivo
    assert mock_remove.call_count == 2
    mock_remove.assert_any_call("produtos_local.txt")
    mock_remove.assert_any_call("Pedidos.txt")

@pytest.mark.unitario_arquivos
def test_apagar_arquivos_temporarios_inexistentes(mocker):
    """Testa a exclusão quando os arquivos não existem"""
    mock_remove = mocker.patch('os.remove')
    mock_exists = mocker.patch('os.path.exists', return_value=False)
    
    manipulacaoArquivos.apagarArquivosTemporarios()
    
    # Verifica que os.remove não foi chamado
    mock_remove.assert_not_called()

@pytest.mark.unitario_arquivos
def test_apagar_arquivos_temporarios_misto(mocker):
    """Testa a exclusão quando um arquivo existe e outro não"""
    mock_remove = mocker.patch('os.remove')
    
    def mock_exists_side_effect(arquivo):
        return arquivo == "produtos_local.txt"  # Só produtos_local existe
    
    mocker.patch('os.path.exists', side_effect=mock_exists_side_effect)
    
    manipulacaoArquivos.apagarArquivosTemporarios()
    
    # Verifica que os.remove foi chamado apenas para o arquivo que existe
    mock_remove.assert_called_once_with("produtos_local.txt")