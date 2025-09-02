import pytest
from unittest.mock import patch, MagicMock
import src.auth.auth_loja 

# Mock completo de todas as funções de interface que podem causar interação
@pytest.fixture(autouse=True)
def mock_all_interface_functions():
    """Mock automático de todas as funções de interface que pedem input"""
    with patch('src.auth.auth_loja.pausar'):  # Remove a pausa
        with patch('src.auth.auth_loja.cabecalho'):  # Remove cabecalho
            with patch('src.auth.auth_loja.painel'):  # Remove painel
                # REMOVIDO: with patch('src.auth.auth_loja.limpar_tela') - não existe em auth_loja
                yield

@pytest.mark.unitarios_login
def test_login_automatico_sucesso():
    """Teste que simula login automático com usuário e senha 'teste'"""
    
    with patch('src.auth.auth_loja.prompt', return_value="teste"):
        with patch('src.auth.auth_loja.prompt_senha', return_value="teste"):
            with patch('src.auth.auth_loja.validar_login', return_value=(True, {"username": "teste"}, "Login OK")):
                with patch('src.auth.auth_loja.mensagem_sucesso'):
                    with patch('src.auth.auth_loja.log'):
                        resultado = src.auth.auth_loja.handle_login_option()
                        assert resultado is not None
                        assert resultado["username"] == "teste"

@pytest.mark.unitarios_login
def test_login_automatico_falha():
    """Teste que simula login com falha"""
    
    with patch('src.auth.auth_loja.prompt', return_value="teste"):
        with patch('src.auth.auth_loja.prompt_senha', return_value="senha_errada"):
            with patch('src.auth.auth_loja.validar_login', return_value=(False, None, "Senha inválida")):
                with patch('src.auth.auth_loja.mensagem_alerta'):
                    with patch('src.auth.auth_loja.confirmar', return_value=False):
                        with patch('src.auth.auth_loja.log'):
                            resultado = src.auth.auth_loja.handle_login_option()
                            assert resultado is None



import pytest
from unittest.mock import patch
import src.auth.auth_loja as auth

@pytest.mark.unitarios_login
def test_esqueci_minha_senha():
    """Teste automático da funcionalidade 'Esqueci minha senha'"""

    with patch('src.auth.auth_loja.prompt', side_effect=[
        "teste",                # usuário
        "resposta_seg",         # resposta da pergunta de segurança
        "nova_senha",           # nova senha
        "nova_senha"            # confirmação
    ]):
        with patch('src.auth.auth_loja.prompt_senha', side_effect=[
            "nova_senha", "nova_senha"  # caso prompt_senha seja chamado
        ]):
            with patch('src.auth.auth_loja.iniciar_recuperacao', return_value=(True, "token_teste", "Qual sua cor favorita?")) as mock_iniciar:
                with patch('src.auth.auth_loja.concluir_recuperacao', return_value=(True, "Senha redefinida com sucesso")) as mock_concluir:
                    with patch('src.auth.auth_loja.mensagem_alerta'):
                        with patch('src.auth.auth_loja.mensagem_sucesso'):
                            with patch('src.auth.auth_loja.pausar', return_value=None):
                                with patch('src.auth.auth_loja.log'):
                                    with patch('src.auth.auth_loja.painel'):
                                        # executa função
                                        auth.tela_esqueci_senha()
                                        # verifica chamadas críticas
                                        mock_iniciar.assert_called_once_with("teste")
                                        mock_concluir.assert_called_once_with("token_teste", "resposta_seg", "nova_senha")


@pytest.mark.unitarios_login
def test_esqueci_senha_usuario_cancela():
    """Deve encerrar imediatamente quando o usuário cancela no prompt"""

    with patch('src.auth.auth_loja.prompt', return_value="") as mock_prompt, \
         patch('src.auth.auth_loja.confirmar') as mock_confirmar, \
         patch('src.auth.auth_loja.mensagem_alerta') as mock_alerta, \
         patch('src.auth.auth_loja.log') as mock_log:

        resultado = src.auth.auth_loja.tela_esqueci_senha()

    # Prompt foi chamado
    mock_prompt.assert_called_once()

    # Como o usuário cancelou no prompt, não deve chamar confirmar
    mock_confirmar.assert_not_called()

    # Deve avisar cancelamento ou registrar log
    assert mock_alerta.called or mock_log.called, \
        "Cancelamento não foi informado nem registrado."

    if mock_alerta.called:
        args, _ = mock_alerta.call_args
        # Basta garantir que uma mensagem não-vazia foi passada
        assert any(str(a).strip() for a in args), \
            "mensagem_alerta foi chamada mas sem mensagem significativa."

    # Função deve retornar None (ou algo falsy)
    assert resultado is None

@pytest.mark.unitarios_login
def test_cadastro_nova_conta():
    """Teste para cadastrar uma nova conta 'teste2'"""
    
    with patch('src.auth.auth_loja.prompt', side_effect=[
        "teste2",           # username
        "Usuário Teste 2",  # nome completo
        "teste2@gmail.com", # email
        "Qual sua cor favorita?",  # pergunta de segurança
        "azul"              # resposta
    ]):
        with patch('src.auth.auth_loja.prompt_senha', side_effect=["teste2", "teste2"]):
            with patch('src.auth.auth_loja.mensagem_alerta'):
                with patch('src.auth.auth_loja.mensagem_sucesso'):
                    with patch('src.auth.auth_loja.log'):
                        with patch('src.auth.auth_loja.criar_usuario', return_value=(True, "Usuário criado com sucesso")) as mock_criar:
                            resultado = src.auth.auth_loja.tela_cadastro()
                            assert resultado is True
                            mock_criar.assert_called_once_with(
                                "teste2", 
                                "Usuário Teste 2", 
                                "teste2@gmail.com", 
                                "teste2", 
                                "Qual sua cor favorita?", 
                                "azul"
                            )

@pytest.mark.unitarios_login
def test_cadastro_senhas_nao_conferem():
    """Teste para verificar se o cadastro detecta quando as senhas não conferem"""
    
    with patch('src.auth.auth_loja.prompt', side_effect=[
        "teste2",           # username
        "Usuário Teste 2",  # nome completo
        "teste2@gmail.com", # email
        "Qual sua cor favorita?",  # pergunta de segurança
        "azul"              # resposta
    ]):
        with patch('src.auth.auth_loja.prompt_senha', side_effect=["teste2", "diferente"]):
            with patch('src.auth.auth_loja.mensagem_alerta') as mock_alerta:
                with patch('src.auth.auth_loja.mensagem_sucesso'):
                    with patch('src.auth.auth_loja.log'):
                        resultado = src.auth.auth_loja.tela_cadastro()
                        assert resultado is False
                        mock_alerta.assert_called_once_with("As senhas não conferem.")

@pytest.mark.unitarios_login
def test_cadastro_usuario_existente():
    """Teste quando tenta cadastrar usuário que já existe"""
    
    with patch('src.auth.auth_loja.prompt', side_effect=[
        "usuario_existente", "Nome", "email", "pergunta", "resposta"
    ]):
        with patch('src.auth.auth_loja.prompt_senha', return_value="senha"):
            with patch('src.auth.auth_loja.criar_usuario', return_value=(False, "Usuário já existe")):
                with patch('src.auth.auth_loja.mensagem_alerta') as mock_alerta:
                    with patch('src.auth.auth_loja.log'):
                        resultado = src.auth.auth_loja.tela_cadastro()
                        assert resultado is False
                        mock_alerta.assert_called_once_with("Usuário já existe")

