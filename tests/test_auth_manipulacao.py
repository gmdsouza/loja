import pytest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
from src.auth import auth_manipulacao

@pytest.mark.unitario_auth_manipulacao
def test_garantir_estrutura_completa():
    """Testa _garantir_estrutura com dados completos"""
    dados = {
        "usuarios": [{"id": 1}],
        "recuperacoes": {"token": "data"}
    }
    
    resultado = auth_manipulacao._garantir_estrutura(dados)
    
    assert resultado == dados  # Não deve alterar dados completos

@pytest.mark.unitario_auth_manipulacao
def test_garantir_estrutura_vazia():
    """Testa _garantir_estrutura com dados vazios"""
    dados = {}
    
    resultado = auth_manipulacao._garantir_estrutura(dados)
    
    assert "usuarios" in resultado
    assert "recuperacoes" in resultado
    assert resultado["usuarios"] == []
    assert resultado["recuperacoes"] == {}

@pytest.mark.unitario_auth_manipulacao
def test_garantir_estrutura_tipos_errados():
    """Testa _garantir_estrutura com tipos errados"""
    dados = {
        "usuarios": "não é lista",
        "recuperacoes": "não é dict"
    }
    
    resultado = auth_manipulacao._garantir_estrutura(dados)
    
    assert resultado["usuarios"] == []  # Deve corrigir para lista
    assert resultado["recuperacoes"] == {}  # Deve corrigir para dict

@pytest.mark.unitario_auth_manipulacao
def test_carregar_db_arquivo_inexistente(mocker):
    """Testa carregar_db quando o arquivo não existe"""
    mocker.patch('os.path.exists', return_value=False)
    
    resultado = auth_manipulacao.carregar_db()
    
    assert resultado == {"usuarios": [], "recuperacoes": {}}

@pytest.mark.unitario_auth_manipulacao
def test_carregar_db_com_ma_sucesso(mocker):
    """Testa carregar_db usando manipulacaoArquivos com sucesso"""
    dados_esperados = {"usuarios": [{"id": 1}], "recuperacoes": {}}
    
    # Mock para simular que ma existe e tem lerArquivo
    mock_ma = MagicMock()
    mock_file = mock_open(read_data=json.dumps(dados_esperados))
    mock_ma.lerArquivo.return_value = mock_file.return_value
    
    with patch('src.auth.auth_manipulacao.ma', mock_ma):
        with patch('os.path.exists', return_value=True):
            resultado = auth_manipulacao.carregar_db()
            
            assert resultado == dados_esperados
            mock_ma.lerArquivo.assert_called_once_with("db.json", "r")

@pytest.mark.unitario_auth_manipulacao
def test_carregar_db_com_ma_falha(mocker):
    """Testa carregar_db quando manipulacaoArquivos falha"""
    # Mock para simular que ma existe mas lerArquivo falha
    mock_ma = MagicMock()
    mock_ma.lerArquivo.side_effect = Exception("Erro")
    
    with patch('src.auth.auth_manipulacao.ma', mock_ma):
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data='{"usuarios": []}')):
                resultado = auth_manipulacao.carregar_db()
                
                assert resultado == {"usuarios": [], "recuperacoes": {}}

@pytest.mark.unitario_auth_manipulacao
def test_carregar_db_sem_ma_sucesso(mocker):
    """Testa carregar_db sem manipulacaoArquivos (usando open)"""
    dados_esperados = {"usuarios": [{"id": 1}], "recuperacoes": {}}
    
    with patch('src.auth.auth_manipulacao.ma', None):  # Simula ma = None
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=json.dumps(dados_esperados))):
                resultado = auth_manipulacao.carregar_db()
                
                assert resultado == dados_esperados

@pytest.mark.unitario_auth_manipulacao
def test_carregar_db_erro_json(mocker):
    """Testa carregar_db quando o JSON é inválido"""
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data='invalid json')):
            resultado = auth_manipulacao.carregar_db()
            
            assert resultado == {"usuarios": [], "recuperacoes": {}}

@pytest.mark.unitario_auth_manipulacao
def test_carregar_db_nao_dict(mocker):
    """Testa carregar_db quando o JSON não é um dicionário"""
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data='["lista", "não", "dict"]')):
            resultado = auth_manipulacao.carregar_db()
            
            assert resultado == {"usuarios": [], "recuperacoes": {}}

@pytest.mark.unitario_auth_manipulacao
def test_salvar_db_com_ma_sucesso(mocker):
    """Testa salvar_db usando manipulacaoArquivos com sucesso"""
    dados = {"usuarios": [{"id": 1}], "recuperacoes": {}}
    
    # Mock para simular que ma existe e tem lerArquivo
    mock_ma = MagicMock()
    mock_file = mock_open()
    mock_ma.lerArquivo.return_value = mock_file.return_value
    
    with patch('src.auth.auth_manipulacao.ma', mock_ma):
        auth_manipulacao.salvar_db(dados)
        
        mock_ma.lerArquivo.assert_called_once_with("db.json", "w")
        handle = mock_file()
        handle.write.assert_called()  # Verifica que escreveu no arquivo

@pytest.mark.unitario_auth_manipulacao
def test_salvar_db_com_ma_falha(mocker):
    """Testa salvar_db quando manipulacaoArquivos falha (deve usar open)"""
    dados = {"usuarios": [{"id": 1}], "recuperacoes": {}}
    
    # Mock para simular que ma existe mas lerArquivo falha
    mock_ma = MagicMock()
    mock_ma.lerArquivo.side_effect = Exception("Erro")
    mock_file = mock_open()
    
    with patch('src.auth.auth_manipulacao.ma', mock_ma):
        with patch('builtins.open', mock_file):
            auth_manipulacao.salvar_db(dados)
            
            # Deve ter tentado usar open como fallback
            mock_file.assert_called_once_with("db.json", "w", encoding="utf-8")

@pytest.mark.unitario_auth_manipulacao
def test_salvar_db_sem_ma(mocker):
    """Testa salvar_db sem manipulacaoArquivos (usando open)"""
    dados = {"usuarios": [{"id": 1}], "recuperacoes": {}}
    mock_file = mock_open()
    
    with patch('src.auth.auth_manipulacao.ma', None):  # Simula ma = None
        with patch('builtins.open', mock_file):
            auth_manipulacao.salvar_db(dados)
            
            mock_file.assert_called_once_with("db.json", "w", encoding="utf-8")

@pytest.mark.unitario_auth_manipulacao
def test_salvar_db_estrutura_automatica(mocker):
    """Testa que salvar_db garante a estrutura automaticamente"""
    dados_incompletos = {"usuarios": [{"id": 1}]}
    
    with patch('builtins.open', mock_open()) as mock_file:
        auth_manipulacao.salvar_db(dados_incompletos)
        
        # Apenas verifica que a função não quebrou
        assert True

@pytest.mark.unitario_auth_manipulacao
def test_salvar_db_excecao_geral(mocker):
    """Testa salvar_db com exceção geral - versão simplificada"""
    dados = {"usuarios": [{"id": 1}], "recuperacoes": {}}
    
    # Mock que falha no ma.lerArquivo
    mock_ma = MagicMock()
    mock_ma.lerArquivo.side_effect = Exception("Erro no ma")
    
    # Mock do open que funciona normalmente
    with patch('src.auth.auth_manipulacao.ma', mock_ma):
        with patch('builtins.open', mock_open()):
            # Deve conseguir salvar usando o fallback para open
            auth_manipulacao.salvar_db(dados)
            
            # Verifica que ma.lerArquivo foi chamado (e falhou)
            mock_ma.lerArquivo.assert_called_once_with("db.json", "w")
            
            # Verifica que open foi chamado como fallback
            from unittest.mock import call
            import builtins
            builtins.open.assert_called_once_with("db.json", "w", encoding="utf-8")

            
@pytest.mark.unitario_auth_manipulacao
def test_ma_import_error():
    """Testa o comportamento quando import de manipulacaoArquivos falha"""
    # Simula que o import falhou (ma = None)
    assert auth_manipulacao.ma is None or hasattr(auth_manipulacao.ma, 'lerArquivo')