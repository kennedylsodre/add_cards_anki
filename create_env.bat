@echo off
title 🐍 Criar ambiente Conda e instalar requirements
echo Criando ambiente "anki" com Python 3.11...
CALL conda create -y --name anki python=3.11

echo.
echo Ativando ambiente e instalando dependências...
CALL conda activate anki
pip install -r requirements.txt

echo.
echo ✅ Ambiente configurado com sucesso!
pause
