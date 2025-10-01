@echo off
setlocal ENABLEDELAYEDEXPANSION
title Instalar dependencias do projeto (Flask + Jogo)

REM Ir para a pasta do script
cd /d %~dp0

echo.
echo [1/5] Criando ambiente virtual .venv (se nao existir)...
if not exist .venv (
  py -m venv .venv
)

echo.
echo [2/5] Ativando ambiente virtual...
call .venv\Scripts\activate
if errorlevel 1 (
  echo Falha ao ativar o ambiente virtual. Execute manualmente: .venv\Scripts\activate
  exit /b 1
)

echo.
echo [3/5] Atualizando pip/setuptools/wheel...
python -m pip install --upgrade pip setuptools wheel

echo.
if exist requirements.txt (
  echo [4/5] Instalando dependencias do requirements.txt...
  pip install -r requirements.txt
) else (
  echo [4/5] Instalando dependencias padrao (Flask, Pygame, OpenCV, Requests)...
  pip install flask pygame opencv-python requests
)

echo.
echo [5/5] Concluido!
echo Ambiente virtual: .venv
echo Para ativar depois: call .venv\Scripts\activate
echo.
echo Dica: Inicie o servidor com: flask --app flaskr run --debug
echo       E o jogo com:       python -m flaskr.main

pause
endlocal


