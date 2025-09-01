import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import menu_principal
import src.utils.manipulacaoArquivos as manipulacaoArquivos
import atexit
from src.auth.auth_loja import iniciar_sistema  # novo import

# Limpeza automática ao sair do programa
atexit.register(manipulacaoArquivos.apagarArquivosTemporarios)

if __name__ == "__main__":
    iniciar_sistema()  # inicia com login/cadastro/esqueci senha

