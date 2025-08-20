@echo off
setlocal

:: Caminho relativo para o Python do WinPython
set WINPY=..\Python Portatil\WPy64-31241\python-3.12.4.amd64\python.exe

:: Verifica se o Python do WinPython existe
if exist "%WINPY%" (
    echo Usando Python do WinPython
    "%WINPY%" Start.py
) else (
    echo >> WinPython não encontrado. Usando Python do sistema.
    python Start.py
)

pause