import pytest
from unittest.mock import patch, MagicMock
import time
import secrets
from src.auth import usuarios

@pytest.mark.unitario_usuarios
def test_hash_texto():
    """Testa a função de hash de texto"""
    salt = "salt123"
    texto = "password123"
    
    resultado = usuarios._hash_texto(texto, salt)
    
    # Hash deve ser consistente
    assert isinstance(resultado, str)
    assert len(resultado) == 64  # SHA256 hex digest length
    assert resultado == usuarios._hash_texto(texto, salt)  # Deve ser igual

@pytest.mark.unitario_usuarios
def test_hash_senha():
    """Testa a função de hash de senha"""
    senha = "minhasenha123"
    
    hash_resultado, salt = usuarios._hash_senha(senha)
    
    assert isinstance(hash_resultado, str)
    assert isinstance(salt, str)
    assert len(hash_resultado) == 64
    assert len(salt) == 32  # 16 bytes em hex
    
    # Teste com salt específico
    hash2, salt2 = usuarios._hash_senha(senha, salt)
    assert hash2 == hash_resultado
    assert salt2 == salt

@pytest.mark.unitario_usuarios
def test_const_eq():
    """Testa a comparação constante de strings"""
    assert usuarios._const_eq("abc", "abc") == True
    assert usuarios._const_eq("abc", "abcd") == False
    assert usuarios._const_eq("", "") == True

@pytest.mark.unitario_usuarios
def test_listar_usuarios(mocker):
    """Testa listagem de usuários"""
    usuarios_fake = [{"username": "user1"}, {"username": "user2"}]
    
    with patch('src.auth.usuarios.carregar_db', return_value={"usuarios": usuarios_fake}):
        resultado = usuarios.listar_usuarios()
        
        assert resultado == usuarios_fake
        assert len(resultado) == 2

@pytest.mark.unitario_usuarios
def test_listar_usuarios_vazio(mocker):
    """Testa listagem quando não há usuários"""
    with patch('src.auth.usuarios.carregar_db', return_value={}):
        resultado = usuarios.listar_usuarios()
        
        assert resultado == []

@pytest.mark.unitario_usuarios
def test_buscar_usuario_por_login_encontrado(mocker):
    """Testa busca de usuário por login (encontrado)"""
    usuarios_fake = [
        {"username": "user1", "email": "user1@email.com"},
        {"username": "user2", "email": "user2@email.com"}
    ]
    
    with patch('src.auth.usuarios.carregar_db', return_value={"usuarios": usuarios_fake}):
        # Busca por username
        resultado = usuarios.buscar_usuario_por_login("user1")
        assert resultado == usuarios_fake[0]
        
        # Busca por email
        resultado = usuarios.buscar_usuario_por_login("user2@email.com")
        assert resultado == usuarios_fake[1]

@pytest.mark.unitario_usuarios
def test_buscar_usuario_por_login_nao_encontrado(mocker):
    """Testa busca de usuário por login (não encontrado)"""
    usuarios_fake = [{"username": "user1", "email": "user1@email.com"}]
    
    with patch('src.auth.usuarios.carregar_db', return_value={"usuarios": usuarios_fake}):
        resultado = usuarios.buscar_usuario_por_login("inexistente")
        assert resultado is None

@pytest.mark.unitario_usuarios
def test_criar_usuario_sucesso(mocker):
    """Testa criação de usuário com sucesso"""
    db_vazio = {"usuarios": []}
    mocker.patch('src.auth.usuarios.carregar_db', return_value=db_vazio)
    mock_salvar = mocker.patch('src.auth.usuarios.salvar_db')
    
    resultado, mensagem = usuarios.criar_usuario(
        "novouser", "Novo Usuário", "novo@email.com", "senha123", 
        "Qual sua cor favorita?", "azul"
    )
    
    assert resultado == True
    assert "sucesso" in mensagem.lower()
    mock_salvar.assert_called_once()

@pytest.mark.unitario_usuarios
def test_criar_usuario_campos_obrigatorios(mocker):
    """Testa criação de usuário com campos obrigatórios faltando"""
    resultado, mensagem = usuarios.criar_usuario("", "Nome", "email@test.com", "senha", "pergunta", "resposta")
    assert resultado == False
    assert "preencha" in mensagem.lower()

@pytest.mark.unitario_usuarios
def test_criar_usuario_duplicado(mocker):
    """Testa criação de usuário com username/email duplicado"""
    usuarios_existentes = [
        {"username": "existente", "email": "existente@email.com"}
    ]
    
    with patch('src.auth.usuarios.carregar_db', return_value={"usuarios": usuarios_existentes}):
        # Username duplicado
        resultado, mensagem = usuarios.criar_usuario(
            "existente", "Nome", "novo@email.com", "senha", "pergunta", "resposta"
        )
        assert resultado == False
        assert "username" in mensagem.lower()
        
        # Email duplicado
        resultado, mensagem = usuarios.criar_usuario(
            "novouser", "Nome", "existente@email.com", "senha", "pergunta", "resposta"
        )
        assert resultado == False
        assert "e-mail" in mensagem.lower()

@pytest.mark.unitario_usuarios
def test_validar_login_sucesso(mocker):
    """Testa validação de login com sucesso"""
    usuario_fake = {
        "username": "testuser",
        "senha_salt": "salt123",
        "senha_hash": usuarios._hash_texto("senha123", "salt123"),
        "ativo": True
    }
    
    with patch('src.auth.usuarios.buscar_usuario_por_login', return_value=usuario_fake):
        resultado, usuario_publico, mensagem = usuarios.validar_login("testuser", "senha123")
        
        assert resultado == True
        assert usuario_publico is not None
        assert "ok" in mensagem.lower()
        # Verifica que dados sensíveis foram removidos
        assert "senha_hash" not in usuario_publico
        assert "senha_salt" not in usuario_publico

@pytest.mark.unitario_usuarios
def test_validar_login_usuario_nao_encontrado(mocker):
    """Testa validação de login com usuário não encontrado"""
    with patch('src.auth.usuarios.buscar_usuario_por_login', return_value=None):
        resultado, usuario_publico, mensagem = usuarios.validar_login("inexistente", "senha123")
        
        assert resultado == False
        assert usuario_publico is None
        assert "não encontrado" in mensagem.lower()

@pytest.mark.unitario_usuarios
def test_validar_login_senha_incorreta(mocker):
    """Testa validação de login com senha incorreta"""
    usuario_fake = {
        "username": "testuser",
        "senha_salt": "salt123",
        "senha_hash": usuarios._hash_texto("senhacorreta", "salt123"),
        "ativo": True
    }
    
    with patch('src.auth.usuarios.buscar_usuario_por_login', return_value=usuario_fake):
        resultado, usuario_publico, mensagem = usuarios.validar_login("testuser", "senhaerrada")
        
        assert resultado == False
        assert usuario_publico is None
        assert "inválida" in mensagem.lower()

@pytest.mark.unitario_usuarios
def test_validar_login_usuario_inativo(mocker):
    """Testa validação de login com usuário inativo"""
    usuario_fake = {
        "username": "testuser",
        "senha_salt": "salt123",
        "senha_hash": usuarios._hash_texto("senha123", "salt123"),
        "ativo": False
    }
    
    with patch('src.auth.usuarios.buscar_usuario_por_login', return_value=usuario_fake):
        resultado, usuario_publico, mensagem = usuarios.validar_login("testuser", "senha123")  # CORREÇÃO: validar_login
        
        assert resultado == False
        assert usuario_publico is None
        assert "inativo" in mensagem.lower()

@pytest.mark.unitario_usuarios
def test_iniciar_recuperacao_sucesso(mocker):
    """Testa início de recuperação de senha com sucesso"""
    usuario_fake = {
        "id": "user123",
        "username": "testuser",
        "pergunta": "Qual sua cor favorita?"
    }
    
    mocker.patch('src.auth.usuarios.carregar_db', return_value={"usuarios": [usuario_fake]})
    mock_salvar = mocker.patch('src.auth.usuarios.salvar_db')
    
    with patch('src.auth.usuarios.buscar_usuario_por_login', return_value=usuario_fake):
        resultado, token, pergunta = usuarios.iniciar_recuperacao("testuser")
        
        assert resultado == True
        assert isinstance(token, str)
        assert pergunta == "Qual sua cor favorita?"
        mock_salvar.assert_called_once()

@pytest.mark.unitario_usuarios
def test_iniciar_recuperacao_usuario_nao_encontrado(mocker):
    """Testa início de recuperação com usuário não encontrado"""
    with patch('src.auth.usuarios.buscar_usuario_por_login', return_value=None):
        resultado, token, pergunta = usuarios.iniciar_recuperacao("inexistente")
        
        assert resultado == False
        assert "não encontrado" in token.lower()
        assert pergunta is None

@pytest.mark.unitario_usuarios
def test_concluir_recuperacao_sucesso(mocker):
    """Testa conclusão de recuperação de senha com sucesso"""
    usuario_fake = {
        "id": "user123",
        "resposta_salt": "salt123",
        "resposta_hash": usuarios._hash_texto("respostacorreta", "salt123")
    }
    
    db_fake = {
        "usuarios": [usuario_fake],
        "recuperacoes": {
            "token123": {
                "user_id": "user123",
                "expira_em": int(time.time()) + 3600  # 1 hora no futuro
            }
        }
    }
    
    mocker.patch('src.auth.usuarios.carregar_db', return_value=db_fake)
    mock_salvar = mocker.patch('src.auth.usuarios.salvar_db')
    
    resultado, mensagem = usuarios.concluir_recuperacao("token123", "respostacorreta", "novasenha")
    
    assert resultado == True
    assert "sucesso" in mensagem.lower()
    mock_salvar.assert_called_once()

@pytest.mark.unitario_usuarios
def test_concluir_recuperacao_token_invalido(mocker):
    """Testa conclusão com token inválido"""
    with patch('src.auth.usuarios.carregar_db', return_value={"recuperacoes": {}}):
        resultado, mensagem = usuarios.concluir_recuperacao("token_invalido", "resposta", "novasenha")
        
        assert resultado == False
        assert "inválido" in mensagem.lower()

@pytest.mark.unitario_usuarios
def test_concluir_recuperacao_token_expirado(mocker):
    """Testa conclusão com token expirado"""
    db_fake = {
        "recuperacoes": {
            "token123": {
                "user_id": "user123",
                "expira_em": int(time.time()) - 3600  # 1 hora no passado
            }
        }
    }
    
    with patch('src.auth.usuarios.carregar_db', return_value=db_fake):
        with patch('src.auth.usuarios.salvar_db'):
            resultado, mensagem = usuarios.concluir_recuperacao("token123", "resposta", "novasenha")
            
            assert resultado == False
            assert "expirado" in mensagem.lower()

@pytest.mark.unitario_usuarios
def test_concluir_recuperacao_resposta_incorreta(mocker):
    """Testa conclusão com resposta incorreta"""
    usuario_fake = {
        "id": "user123",
        "resposta_salt": "salt123",
        "resposta_hash": usuarios._hash_texto("respostacorreta", "salt123")
    }
    
    db_fake = {
        "usuarios": [usuario_fake],
        "recuperacoes": {
            "token123": {
                "user_id": "user123",
                "expira_em": int(time.time()) + 3600
            }
        }
    }
    
    with patch('src.auth.usuarios.carregar_db', return_value=db_fake):
        resultado, mensagem = usuarios.concluir_recuperacao("token123", "respostaerrada", "novasenha")
        
        assert resultado == False
        assert "incorreta" in mensagem.lower()