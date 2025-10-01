@echo off
setlocal

cd /d %~dp0

REM Ativar venv se existir
if exist .venv\Scripts\activate.bat (
  call .venv\Scripts\activate.bat
)


python "flaskr\__init__.py"

endlocal