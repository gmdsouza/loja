import menu_principal
import manipulacaoArquivos
import atexit
from auth_loja import iniciar_sistema  # novo import

# Limpeza automática ao sair do programa
atexit.register(manipulacaoArquivos.apagarArquivosTemporarios)

if __name__ == "__main__":
    iniciar_sistema()  # inicia com login/cadastro/esqueci senha

