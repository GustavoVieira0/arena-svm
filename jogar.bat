@echo off
title Arena SVM
cd /d "%~dp0"

rem ---- 1. Encontrar o Python (3.11 ou mais novo) ----
set "PY="
py -3 --version >nul 2>nul && set "PY=py -3"
if not defined PY python --version >nul 2>nul && set "PY=python"
if not defined PY goto sem_python
%PY% -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" || goto versao_antiga

rem ---- 2. Primeira vez: criar o ambiente e instalar as dependencias ----
if not exist ".venv\Scripts\python.exe" (
  echo Primeira execucao: criando o ambiente Python e instalando as dependencias.
  echo Isso leva alguns minutos e precisa de internet...
  %PY% -m venv .venv || goto erro
  ".venv\Scripts\python.exe" -m pip install --upgrade pip
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt || goto erro
)

rem ---- 3. Abrir o navegador so quando o servidor responder ----
start "" /b powershell -NoProfile -WindowStyle Hidden -Command "for ($i = 0; $i -lt 90; $i++) { try { Invoke-WebRequest -UseBasicParsing -TimeoutSec 5 http://127.0.0.1:5000/api/pokemon | Out-Null; Start-Process 'http://localhost:5000'; break } catch { Start-Sleep -Seconds 1 } }"

rem ---- 4. Iniciar o servidor (feche esta janela ou aperte Ctrl+C para desligar) ----
".venv\Scripts\python.exe" app\servidor.py
echo.
echo O servidor foi encerrado.
pause
exit /b 0

:sem_python
echo Python nao encontrado.
echo Instale o Python 3.12 em https://www.python.org/downloads/
echo Na instalacao, marque a opcao "Add python.exe to PATH". Depois rode este arquivo de novo.
pause
exit /b 1

:versao_antiga
echo Este projeto precisa do Python 3.11 ou mais novo. Versao encontrada:
%PY% --version
echo Instale o Python 3.12 em https://www.python.org/downloads/ e rode este arquivo de novo.
pause
exit /b 1

:erro
echo.
echo Ocorreu um erro na instalacao. Veja as mensagens acima.
echo Dica: apague a pasta .venv e rode este arquivo de novo.
pause
exit /b 1
