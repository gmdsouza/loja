import pytest
from src.pagamentos import pagamentos
from src.interface import interface
from src.utils import manipulacaoArquivos
from unittest.mock import ANY

@pytest.mark.unitario_pagamento
def test_realizar_pagamento(mocker):
    """
    Testa o cenário de realizar pagamento.
    """
    pedidos_falsos = (
    '2025-08-18;[{"id": 1, "nome": "Produto A", "preco": 10.0}]\n'
    '2025-08-18;[{"id": 2, "nome": "Produto B", "preco": 20.0}, {"id": 3, "nome": "Produto C", "preco": 5.50}]'
    )

    # CORREÇÕES NOS PATHS DOS MOCKS:
    mocker.patch('src.utils.manipulacaoArquivos.lerArquivo', mocker.mock_open(read_data=pedidos_falsos))
    mock_abrir_arquivo = mocker.patch('builtins.open', mocker.mock_open())
    
    mocker.patch('builtins.input', return_value='1')
    mock_mensagem_sucesso = mocker.patch('src.interface.interface.mensagem_sucesso')

    mocker.patch('src.interface.interface.limpar_tela')
    mocker.patch('src.interface.interface.titulo')
    mocker.patch('src.interface.interface.pausar')

    pagamentos.realizar_pagamento()
    mock_mensagem_sucesso.assert_any_call("✅ Pagamento de R$ 35.50 realizado via CRÉDITO!")

    mock_abrir_arquivo.assert_called_once_with("Pedidos.txt", "w")

    handle = mock_abrir_arquivo()
    handle.truncate.assert_called_once()

    print("\n✅ O teste de realizar pagamento passou com sucesso")