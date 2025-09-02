import os
import sys
import time
import subprocess
import pyautogui

"""
Teste funcional com PyAutoGUI (simula teclado real no Terminal).

Fluxo:
  - Login (teste/teste, com pausa)
  - Cadastros -> Cadastrar Produto
  - Pedidos -> Adicionar (ID 21) -> Finalizar (Nome/CPF, com pausa)
  - Pagamentos -> 1 (PIX), com pausa
  - Sair

⚠️ Necessário deixar a janela do terminal em foco!
"""

# ===== CONFIG =====
OPEN_NEW_TERMINAL = True        # True: abre novo gnome-terminal; False: usa terminal atual
TYPE_INTERVAL = 0.10            # intervalo entre teclas (segundos) -> digitação lenta
STARTUP_WAIT = 2.0              # tempo p/ novo terminal aparecer
STEP_WAIT = 1.0                 # pausa básica entre etapas (maior = mais lento)

# Caminho do projeto
PROJ_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PYTHON = sys.executable

def write(txt):
    pyautogui.typewrite(str(txt), interval=TYPE_INTERVAL)

def press_enter(times=1):
    for _ in range(times):
        pyautogui.press("enter")
        time.sleep(STEP_WAIT)

def pause(sec=STEP_WAIT):
    time.sleep(sec)

def run_gnome_terminal():
    env = os.environ.copy()
    cmd = f'cd "{PROJ_DIR}"; "{PYTHON}" src/loja.py'
    subprocess.Popen(["gnome-terminal", "--", "bash", "-lc", cmd], env=env)

def main():
    os.chdir(PROJ_DIR)
    print(f"[INFO] cwd = {os.getcwd()}")

    for fname in ("produtos_local.txt", "Pedidos.txt"):
        try:
            os.remove(fname)
        except FileNotFoundError:
            pass

    if OPEN_NEW_TERMINAL:
        run_gnome_terminal()
        time.sleep(STARTUP_WAIT)
        pause(1.0)   # mais tempo para você clicar na janela se precisar
    else:
        print("[INFO] Usando terminal atual, certifique-se que o app já está rodando e focado.")
        time.sleep(3.0)

    # ===== LOGIN =====
    write("1"); press_enter()
    pause()

    write("teste"); press_enter()
    pause()

    write("teste"); press_enter()
    pause(1.2)

    press_enter()   # Pressione Enter pós-login

    # ===== CADASTROS =====
    write("1"); press_enter()
    pause()

    write("1"); press_enter()
    pause()

    write("1"); press_enter()  # Produto
    pause()

    write("Produto Teste"); press_enter()
    pause()

    write("12.34"); press_enter()
    pause()

    write("Gerado pelo teste funcional"); press_enter()
    pause(1.2)

    press_enter()   # pausa de sucesso
    pause()

    write("4"); press_enter()  # voltar
    pause()

    # ===== PEDIDOS =====
    write("4"); press_enter()
    pause()

    write("1"); press_enter()  # adicionar
    pause()

    write("21"); press_enter()
    pause(1.2)

    press_enter()   # pausa pós-adicionar
    pause()

    write("2"); press_enter()  # finalizar
    pause()

    write("Cliente Teste"); press_enter()
    pause()

    write("00000000000"); press_enter()
    pause(1.2)

    press_enter()   # pausa pós-finalizar
    pause()

    write("5"); press_enter()  # voltar
    pause()

    # ===== PAGAMENTOS =====
    write("2"); press_enter()
    pause(1.5)

    write("1"); press_enter()  # PIX
    pause(1.2)

    press_enter()   # pausa pós-pagamento
    pause()

    # ===== SAIR =====
    write("5"); press_enter()
    pause()

    print("[OK] Fluxo PyAutoGUI concluído.")

if __name__ == "__main__":
    main()


