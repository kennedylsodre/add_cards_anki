@echo off
title 🚀 AddCardAnki - Execução via config.json
echo ==========================================
echo Lendo configuração...
echo ==========================================

REM Lê o ambiente Conda do config.json
FOR /F "tokens=2 delims=:," %%A IN ('findstr /i "conda_env" config.json') DO set ENV=%%~A
set ENV=%ENV:"=%
set ENV=%ENV: =%

REM Ativa o ambiente Conda
CALL conda activate %ENV%

cd /d "%~dp0src"
REM Executa o script Python
python main.py

echo.
echo ✅ Finalizado com sucesso!
pause
