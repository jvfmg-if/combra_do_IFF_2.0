@echo off
REM Script para rodar o jogo Cobra do IFF no Windows
REM Uso: clique duas vezes ou execute no cmd: run.bat

SET DIR=%~dp0

echo Instalando dependencias (caso necessario)...
pip install pygame flask opencv-python-headless requests werkzeug

echo Inicializando banco de dados...
cd /d "%DIR%"
python src\db_init.py

echo Iniciando o jogo...
cd /d "%DIR%"
python -c "import src"

pause
