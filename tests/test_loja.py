import pytest
from unittest.mock import patch, MagicMock

@pytest.mark.unitario_loja
def test_loja_import_and_cleanup():
    """
    Testa se o loja.py importa corretamente e registra a limpeza
    """
    # Mock de atexit.register
    mock_atexit_register = MagicMock()
    
    # Mock completo dos módulos
    with patch.dict('sys.modules', {
        'menu_principal': MagicMock(),
        'src.utils.manipulacaoArquivos': MagicMock(apagarArquivosTemporarios=MagicMock()),
        'src.auth.auth_loja': MagicMock(iniciar_sistema=MagicMock()),
        'atexit': MagicMock(register=mock_atexit_register)
    }):
        # Teste de importação
        try:
            import loja
            # Verificar se a limpeza foi registrada
            mock_atexit_register.assert_called_once()
            assert True
        except Exception as e:
            pytest.fail(f"Falha na importação: {e}")

@pytest.mark.unitario_loja
def test_loja_main_execution_simple():
    """
    Testa simplesmente se o módulo pode ser importado
    """
    try:
        import loja
        assert True
    except Exception as e:
        pytest.fail(f"Falha na importação do loja.py: {e}")

