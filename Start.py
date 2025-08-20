import os
import subprocess
import sys
import webbrowser
import platform
import time
import urllib.request

# Caminho do diretório atual (onde está o Start.py)
current_folder = os.path.dirname(os.path.abspath(__file__))
app_file = "Manha_do_Conhecimento.py"

# Caminho relativo para o Python do WinPython
winpython_path = os.path.abspath(
    os.path.join(current_folder, "..", "Python Portatil", "WPy64-31241", "python-3.12.4.amd64", "python.exe")
)

# Fallback: Python do sistema
sistema = platform.system()
python_fallback = "python" if sistema == "Windows" else "python3"

# Decide qual Python usar
if os.path.exists(winpython_path):
    print(">> Usando Python do WinPython.")
    python_cmd = winpython_path
else:
    print(">> Pasta 'Python Portatil' não encontrada. Usando Python do sistema.")
    python_cmd = python_fallback

# Ir para a pasta do app
os.chdir(current_folder)

# ✅ Etapa 1: Atualizar o pip
print("Verificando se o pip pode ser atualizado...")
try:
    subprocess.check_call([python_cmd, "-m", "pip", "install", "--upgrade", "pip"])
    print("pip atualizado com sucesso.")
except subprocess.CalledProcessError:
    print("Falha ao atualizar o pip. Continuando mesmo assim.")

# ✅ Etapa 2: Verifica/instala Flask
try:
    subprocess.check_call([python_cmd, "-c", "import flask"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    print("Flask não está instalado. Instalando...")
    try:
        subprocess.check_call([python_cmd, "-m", "pip", "install", "flask"])
        print("Flask instalado com sucesso.")
    except subprocess.CalledProcessError:
        print("Erro ao tentar instalar o Flask.")
        sys.exit(1)

# ✅ Etapa 3: Verifica/instala sympy
try:
    subprocess.check_call([python_cmd, "-c", "import sympy"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    print("Sympy não está instalado. Instalando...")
    try:
        subprocess.check_call([python_cmd, "-m", "pip", "install", "sympy"])
        print("Sympy instalado com sucesso.")
    except subprocess.CalledProcessError:
        print("Erro ao tentar instalar o Sympy.")
        sys.exit(1)

# ✅ Etapa 4: Atualiza o watchdog
print("Atualizando watchdog...")
try:
    subprocess.check_call([python_cmd, "-m", "pip", "install", "--upgrade", "watchdog"])
    print("Watchdog atualizado com sucesso.")
except subprocess.CalledProcessError:
    print("Erro ao atualizar o watchdog. O modo debug pode não funcionar corretamente.")

# ✅ Etapa 5: Executa o app Flask e aguarda ele estar online
try:
    print("Iniciando o servidor Flask...")
    flask_process = subprocess.Popen([python_cmd, app_file])

    # Esperar até que o servidor Flask esteja disponível
    url = "http://127.0.0.1:5000"
    max_tentativas = 20
    tentativas = 0

    while tentativas < max_tentativas:
        try:
            resposta = urllib.request.urlopen(url)
            if resposta.status == 200:
                print("Servidor online. Abrindo o navegador...")
                webbrowser.open(url)
                break
        except Exception:
            pass
        time.sleep(0.5)  # espera meio segundo antes de tentar de novo
        tentativas += 1

    if tentativas == max_tentativas:
        print("O servidor demorou muito para iniciar. Acesse manualmente:", url)

except Exception as e:
    print(f"Erro ao iniciar o aplicativo: {e}")