@echo off
title AI Shorts Generator - Bot de Videos Virais
color 0A
cls

echo ================================================
echo    AI SHORTS GENERATOR - INICIANDO BOT
echo ================================================
echo.

cd /d "%~dp0"

:: Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado! Instale em: https://python.org
    pause
    exit /b 1
)

:: Instala dependencias se necessario
echo [1/3] Verificando dependencias...
pip install -q openai moviepy instagrapi python-dotenv requests pillow yt-dlp numpy imageio-ffmpeg 2>nul
echo [OK] Dependencias prontas!

:: Cria pastas necessarias
if not exist "downloads" mkdir downloads
if not exist "output" mkdir output

:: Verifica .env
if not exist ".env" (
    echo [ERRO] Arquivo .env nao encontrado!
    echo Crie o arquivo .env com suas chaves de API.
    pause
    exit /b 1
)

echo [2/3] Configuracoes carregadas!
echo.
echo [3/3] Iniciando o pipeline...
echo ------------------------------------------------
python -c "import sys, os; sys.path.insert(0, '.'); from dotenv import load_dotenv; load_dotenv(); from empire_pipeline import run_single_cycle; run_single_cycle()"

echo.
echo ================================================
echo    CICLO CONCLUIDO - Verifique a pasta output/
echo ================================================
pause
