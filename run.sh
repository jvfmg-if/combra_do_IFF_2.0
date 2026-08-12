#!/bin/bash
# Script para rodar o jogo Cobra do IFF no Linux
# Uso: ./run.sh

DIR="$(cd "$(dirname "$0")" && pwd)"
LOCAL_PKG="$DIR/.local-packages"

# .local-packages contem pygame e opencv extraidos de .deb (Python 3.14)
PYTHONPATH="$LOCAL_PKG/usr/lib/python3/dist-packages:$DIR/src:$DIR:$PYTHONPATH"
LD_LIBRARY_PATH="$LOCAL_PKG/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
export PYTHONPATH LD_LIBRARY_PATH

PYTHON=$(command -v python3 || command -v python)
echo "Usando: $PYTHON ($($PYTHON --version 2>&1))"

echo ""
echo "Verificando dependencias..."
PIP="$PYTHON -m pip"
DEPS="flask requests werkzeug"
$PYTHON -c "import flask" 2>/dev/null || {
  echo "  Instalando: $DEPS"
  $PIP install $DEPS 2>&1
}
$PYTHON -c "import pygame" 2>/dev/null || {
  echo "  pygame nao encontrado. Instalando pygame-ce (compativel com Python 3.14)..."
  $PIP install pygame-ce 2>&1 || true
}
$PYTHON -c "import cv2" 2>/dev/null || {
  echo "  opencv nao encontrado (opcional, so usado no easter egg)"
  $PIP install opencv-python-headless 2>&1 || true
}

echo ""
echo "Inicializando banco de dados..."
cd "$DIR"
$PYTHON src/db_init.py

echo ""
echo "Iniciando o jogo..."
cd "$DIR"
$PYTHON -c "import src"
