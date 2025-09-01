import pytest
from unittest.mock import patch
import src.auth.auth_loja  # Importação do módulo para acessar as funções mockadas

@pytest.mark.unitarios_login
def test_login_automatico_sucesso():
    """Teste que simula login automático com usuário e senha 'teste'"""
    
    # Mock das funções de interface para evitar interação real
    with patch('src.auth.auth_loja.prompt', return_value="teste"):
        with patch('src.auth.auth_loja.prompt_senha', return_value="teste"):
            with patch('src.auth.auth_loja.validar_login', return_value=(True, {"username": "teste"}, "Login OK")):
                with patch('src.auth.auth_loja.mensagem_sucesso'):
                    with patch('src.auth.auth_loja.pausar'):
                        with patch('src.auth.auth_loja.log'):
                            # Executar a função de login
                            resultado = src.auth.auth_loja.handle_login_option()
                            
                            # Verificar se o login foi bem-sucedido
                            assert resultado is not None
                            assert resultado["username"] == "teste"

@pytest.mark.unitarios_login
def test_login_automatico_falha():
    """Teste que simula login com falha"""
    
    # Mock das funções de interface
    with patch('src.auth.auth_loja.prompt', return_value="teste"):
        with patch('src.auth.auth_loja.prompt_senha', return_value="senha_errada"):
            with patch('src.auth.auth_loja.validar_login', return_value=(False, None, "Senha inválida")):
                with patch('src.auth.auth_loja.mensagem_alerta'):
                    with patch('src.auth.auth_loja.confirmar', return_value=False):
                        with patch('src.auth.auth_loja.log'):
                            # Executar a função de login
                            resultado = src.auth.auth_loja.handle_login_option()
                            
                            # Verificar se o login falhou
                            assert resultado is None

@pytest.mark.unitarios_login
def test_esqueci_minha_senha():
    """Teste para a funcionalidade 'Esqueci minha senha'"""
    
    # Mock de todas as funções de interface
    with patch('src.auth.auth_loja.cabecalho'):
        with patch('src.auth.auth_loja.prompt', side_effect=["teste", "resposta_seguranca", "nova_senha", "nova_senha"]):
            with patch('src.auth.auth_loja.prompt_senha', side_effect=["nova_senha", "nova_senha"]):
                with patch('src.auth.auth_loja.painel'):
                    with patch('src.auth.auth_loja.mensagem_alerta'):
                        with patch('src.auth.auth_loja.mensagem_sucesso'):
                            with patch('src.auth.auth_loja.pausar'):
                                with patch('src.auth.auth_loja.log'):
                                    # Mock das funções de recuperação
                                    with patch('src.auth.auth_loja.iniciar_recuperacao', return_value=(True, "token_teste", "Qual sua cor favorita?")) as mock_iniciar:
                                        with patch('src.auth.auth_loja.concluir_recuperacao', return_value=(True, "Senha redefinida com sucesso")) as mock_concluir:
                                            # Executar a função de recuperação de senha
                                            src.auth.auth_loja.tela_esqueci_senha()
                                            
                                            # Verificar se as funções foram chamadas corretamente
                                            mock_iniciar.assert_called_once_with("teste")
                                            mock_concluir.assert_called_once_with("token_teste", "resposta_seguranca", "nova_senha")

@pytest.mark.unitarios_login
def test_cadastro_nova_conta():
    """Teste para cadastrar uma nova conta 'teste2'"""
    
    # Mock de todas as funções de interface
    with patch('src.auth.auth_loja.cabecalho'):
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
                            # Mock da função de criação de usuário
                            with patch('src.auth.auth_loja.criar_usuario', return_value=(True, "Usuário criado com sucesso")) as mock_criar:
                                # Executar a função de cadastro
                                resultado = src.auth.auth_loja.tela_cadastro()
                                
                                # Verificar se o cadastro foi bem-sucedido
                                assert resultado is True
                                
                                # Verificar se a função criar_usuario foi chamada com os parâmetros corretos
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
    
    # Mock de todas as funções de interface
    with patch('src.auth.auth_loja.cabecalho'):
        with patch('src.auth.auth_loja.prompt', side_effect=[
            "teste2",           # username
            "Usuário Teste 2",  # nome completo
            "teste2@gmail.com", # email
            "Qual sua cor favorita?",  # pergunta de segurança
            "azul"              # resposta
        ]):
            with patch('src.auth.auth_loja.prompt_senha', side_effect=["teste2", "diferente"]):  # Senhas diferentes
                with patch('src.auth.auth_loja.mensagem_alerta') as mock_alerta:
                    with patch('src.auth.auth_loja.mensagem_sucesso'):
                        # Executar a função de cadastro
                        resultado = src.auth.auth_loja.tela_cadastro()
                        
                        # Verificar se o cadastro falhou devido a senhas diferentes
                        assert resultado is False
                        
                        # Verificar se a mensagem de alerta foi chamada
                        mock_alerta.assert_called_once_with("As senhas não conferem.")