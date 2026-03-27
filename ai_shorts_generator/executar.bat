@echo off
echo.
echo ========================================
echo INICIANDO AI SHORTS GENERATOR
echo ========================================
echo O bot esta instalando/verificando as bibliotecas necessarias...
call .\.venv\Scripts\pip install -r requirements.txt >nul 2>&1

echo.
echo Tudo pronto! Iniciando a maquina...
echo.
.\.venv\Scripts\python main.py
pause
