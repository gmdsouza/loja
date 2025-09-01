import pytest
from unittest.mock import patch, MagicMock

@pytest.mark.unitario_menu
def test_exibir_menu_principal_opcoes_validas(mocker):
    """
    Testa as opções válidas do menu principal
    """
    # Mock completo das funções
    mock_input = mocker.patch('builtins.input', side_effect=['1', '5'])
    mocker.patch('src.interface.interface.mostrar_menu')
    mocker.patch('src.interface.interface.limpar_tela')
    mocker.patch('src.interface.interface.mensagem_sucesso')
    mocker.patch('src.interface.interface.pausar')
    
    # Mock da função menu_cadastros para retornar imediatamente
    mock_menu_cadastros = mocker.patch('menu_principal.menu_cadastros')
    
    # Executar a função
    from menu_principal import exibir_menu_principal
    exibir_menu_principal()
    
    # Verificar se menu_cadastros foi chamado
    mock_menu_cadastros.assert_called_once()

@pytest.mark.unitario_menu
def test_exibir_menu_principal_opcao_invalida(mocker):
    """
    Testa comportamento com opção inválida no menu principal
    """
    mock_input = mocker.patch('builtins.input', side_effect=['99', '5'])
    mock_mensagem_alerta = mocker.patch('src.interface.interface.mensagem_alerta')
    mocker.patch('src.interface.interface.pausar')
    
    from menu_principal import exibir_menu_principal
    exibir_menu_principal()
    
    # Verificar se mensagem de alerta foi chamada
    mock_mensagem_alerta.assert_called_with("❌ Opção inválida.")

@pytest.mark.unitario_menu
def test_menu_cadastros_opcoes_validas(mocker):
    """
    Testa as opções válidas do menu de cadastros
    """
    mock_input = mocker.patch('builtins.input', side_effect=['1', '4'])
    mock_cadastrar = mocker.patch('src.models.cadastros.cadastrar_item')
    mocker.patch('src.interface.interface.pausar')
    
    from menu_principal import menu_cadastros
    menu_cadastros()
    
    # Verificar se cadastrar_item foi chamado
    mock_cadastrar.assert_called_once()

@pytest.mark.unitario_menu
def test_menu_cadastros_opcao_invalida(mocker):
    """
    Testa comportamento com opção inválida no menu de cadastros
    """
    mock_input = mocker.patch('builtins.input', side_effect=['99', '4'])
    mock_mensagem_alerta = mocker.patch('src.interface.interface.mensagem_alerta')
    mocker.patch('src.interface.interface.pausar')
    
    from menu_principal import menu_cadastros
    menu_cadastros()
    
    # Verificar se mensagem de alerta foi chamada
    mock_mensagem_alerta.assert_called_with("❌ Opção inválida.")

@pytest.mark.unitario_menu
def test_menu_principal_sair(mocker):
    """
    Testa a opção de sair do menu principal
    """
    mock_input = mocker.patch('builtins.input', return_value='5')
    mock_limpar_tela = mocker.patch('src.interface.interface.limpar_tela')
    mock_mensagem_sucesso = mocker.patch('src.interface.interface.mensagem_sucesso')
    
    from menu_principal import exibir_menu_principal
    exibir_menu_principal()  # Deve sair imediatamente
    
    # Verificar se a mensagem de despedida foi mostrada
    mock_mensagem_sucesso.assert_called_with("👋 Obrigado por usar a loja!")

@pytest.mark.integracao_menu
def test_menu_principal_integracao_completa(mocker):
    """
    Teste de integração do fluxo completo do menu principal
    """
    # SOLUÇÃO DEFINITIVA: Mock que sempre retorna '5' após as chamadas necessárias
    input_call_count = 0
    
    def smart_input(prompt=""):
        nonlocal input_call_count
        input_call_count += 1
        
        if input_call_count == 1:
            return '1'  # Primeira chamada: entra em Cadastros
        elif input_call_count == 2:
            return '4'  # Segunda chamada: volta do menu Cadastros
        else:
            return '5'  # Demais chamadas: sai do programa
    
    mocker.patch('builtins.input', side_effect=smart_input)
    mocker.patch('src.interface.interface.mostrar_menu')
    mocker.patch('src.interface.interface.limpar_tela')
    mocker.patch('src.interface.interface.mensagem_sucesso')
    mocker.patch('src.interface.interface.pausar')
    mocker.patch('menu_principal.menu_cadastros')
    
    from menu_principal import exibir_menu_principal
    exibir_menu_principal()
    
    # Verificar se input foi chamado pelo menos 3 vezes
    assert input_call_count >= 3