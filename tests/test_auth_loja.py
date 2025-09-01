import pytest
from unittest.mock import patch, MagicMock, call
from src.auth import auth_loja

# Fixture para mockar TODAS as funções de interface automaticamente
@pytest.fixture(autouse=True)
def mock_all_interface_functions():
    """Mock automático de todas as funções de interface"""
    with patch('src.auth.auth_loja.pausar'):
        with patch('src.auth.auth_loja.mensagem_alerta'):
            with patch('src.auth.auth_loja.mensagem_sucesso'):
                with patch('src.auth.auth_loja.cabecalho'):
                    with patch('src.auth.auth_loja.mostrar_menu'):
                        with patch('src.auth.auth_loja.prompt'):
                            with patch('src.auth.auth_loja.prompt_senha'):
                                with patch('src.auth.auth_loja.confirmar'):
                                    with patch('src.auth.auth_loja.painel'):
                                        with patch('src.auth.auth_loja.log'):
                                            yield

@pytest.mark.unitario_auth_loja
def test_abrir_menu_pos_login_sucesso(mocker):
    """Testa abertura do menu pós-login com sucesso"""
    usuario = {"username": "testuser", "nome": "Test User"}
    
    mock_menu_principal = MagicMock()
    mock_menu_principal.exibir_menu_principal = MagicMock()
    
    with patch.dict('sys.modules', {'menu_principal': mock_menu_principal}):
        auth_loja._abrir_menu_pos_login(usuario)
        mock_menu_principal.exibir_menu_principal.assert_called_once()

@pytest.mark.unitario_auth_loja
def test_abrir_menu_pos_login_modulo_nao_encontrado(mocker):
    """Testa abertura do menu quando módulo não é encontrado"""
    usuario = {"username": "testuser"}
    
    with patch.dict('sys.modules', {'menu_principal': None}):
        auth_loja._abrir_menu_pos_login(usuario)
        # A fixture já mocka todas as funções de interface

@pytest.mark.unitario_auth_loja
def test_tela_login_opcao_sair(mocker):
    """Testa tela_login com opção sair"""
    with patch('builtins.input', return_value='4'):  # Sair
        resultado = auth_loja.tela_login()
        assert resultado is None

@pytest.mark.unitario_auth_loja
def test_tela_login_opcao_invalida(mocker):
    """Testa tela_login com opção inválida"""
    with patch('builtins.input', side_effect=['99', '4']):  # Inválido, depois sair
        auth_loja.tela_login()
        # A função handle_invalid_option está mockada pela fixture

@pytest.mark.unitario_auth_loja
def test_handle_login_option_sucesso(mocker):
    """Testa handle_login_option com sucesso"""
    usuario = {"username": "testuser", "nome": "Test User"}
    
    with patch('src.auth.auth_loja.prompt', side_effect=["testuser", "senha123"]):
        with patch('src.auth.auth_loja.validar_login', return_value=(True, usuario, "Login OK")):
            resultado = auth_loja.handle_login_option()
            assert resultado == usuario

@pytest.mark.unitario_auth_loja
def test_handle_login_option_falha(mocker):
    """Testa handle_login_option com falha"""
    with patch('src.auth.auth_loja.prompt', side_effect=["testuser", "senhaerrada"]):
        with patch('src.auth.auth_loja.validar_login', return_value=(False, None, "Senha inválida")):
            with patch('src.auth.auth_loja.confirmar', return_value=False):  # Não tentar novamente
                resultado = auth_loja.handle_login_option()
                assert resultado is None

@pytest.mark.unitario_auth_loja
def test_handle_signup_option_sucesso(mocker):
    """Testa handle_signup_option com sucesso"""
    with patch('src.auth.auth_loja.tela_cadastro', return_value=True):
        auth_loja.handle_signup_option()
        # A mensagem de sucesso está mockada pela fixture

@pytest.mark.unitario_auth_loja
def test_handle_forgot_password_option(mocker):
    """Testa handle_forgot_password_option"""
    with patch('src.auth.auth_loja.tela_esqueci_senha') as mock_esqueci:
        auth_loja.handle_forgot_password_option()
        mock_esqueci.assert_called_once()

@pytest.mark.unitario_auth_loja
def test_handle_invalid_option(mocker):
    """Testa handle_invalid_option"""
    auth_loja.handle_invalid_option()
    # As funções de interface estão mockadas pela fixture

@pytest.mark.unitario_auth_loja
def test_tela_cadastro_sucesso(mocker):
    """Testa tela_cadastro com sucesso"""
    with patch('src.auth.auth_loja.prompt', side_effect=[
        "novouser", "Nome Completo", "email@test.com", "senha123", "senha123",
        "Pergunta", "Resposta"
    ]):
        with patch('src.auth.auth_loja.prompt_senha', side_effect=["senha123", "senha123"]):
            with patch('src.auth.auth_loja.criar_usuario', return_value=(True, "Sucesso")):
                resultado = auth_loja.tela_cadastro()
                assert resultado == True

@pytest.mark.unitario_auth_loja
def test_tela_cadastro_senhas_diferentes(mocker):
    """Testa tela_cadastro com senhas diferentes"""
    with patch('src.auth.auth_loja.prompt', side_effect=["user", "nome", "email"]):
        with patch('src.auth.auth_loja.prompt_senha', side_effect=["senha1", "senha2"]):
            resultado = auth_loja.tela_cadastro()
            assert resultado == False

@pytest.mark.unitario_auth_loja
def test_tela_esqueci_senha_sucesso(mocker):
    """Testa tela_esqueci_senha com sucesso"""
    with patch('src.auth.auth_loja.prompt', side_effect=["user", "resposta", "novasenha", "novasenha"]):
        with patch('src.auth.auth_loja.prompt_senha', side_effect=["novasenha", "novasenha"]):
            with patch('src.auth.auth_loja.iniciar_recuperacao', return_value=(True, "token", "Pergunta")):
                with patch('src.auth.auth_loja.concluir_recuperacao', return_value=(True, "Sucesso")):
                    auth_loja.tela_esqueci_senha()
                    # Todas as funções de interface estão mockadas

@pytest.mark.unitario_auth_loja
def test_tela_esqueci_senha_falha_inicio(mocker):
    """Testa tela_esqueci_senha com falha no início"""
    with patch('src.auth.auth_loja.prompt', return_value="user"):
        with patch('src.auth.auth_loja.iniciar_recuperacao', return_value=(False, "Erro", None)):
            auth_loja.tela_esqueci_senha()

@pytest.mark.unitario_auth_loja
def test_tela_esqueci_senha_senhas_diferentes(mocker):
    """Testa tela_esqueci_senha com senhas diferentes"""
    with patch('src.auth.auth_loja.prompt', side_effect=["user", "resposta"]):
        with patch('src.auth.auth_loja.prompt_senha', side_effect=["senha1", "senha2"]):
            with patch('src.auth.auth_loja.iniciar_recuperacao', return_value=(True, "token", "Pergunta")):
                auth_loja.tela_esqueci_senha()

@pytest.mark.unitario_auth_loja
def test_iniciar_sistema_com_usuario(mocker):
    """Testa iniciar_sistema com usuário logado"""
    usuario = {"username": "testuser"}
    
    with patch('src.auth.auth_loja.tela_login', return_value=usuario):
        with patch('src.auth.auth_loja._abrir_menu_pos_login') as mock_abrir:
            auth_loja.iniciar_sistema()
            mock_abrir.assert_called_once_with(usuario)

@pytest.mark.unitario_auth_loja
def test_iniciar_sistema_sem_usuario(mocker):
    """Testa iniciar_sistema sem usuário logado"""
    with patch('src.auth.auth_loja.tela_login', return_value=None):
        with patch('src.auth.auth_loja._abrir_menu_pos_login') as mock_abrir:
            auth_loja.iniciar_sistema()
            mock_abrir.assert_not_called()