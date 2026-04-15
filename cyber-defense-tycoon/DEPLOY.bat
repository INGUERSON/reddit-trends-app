@echo off
title Deploy - Cyber Defense Tycoon para GitHub Pages
color 0A
cls

echo ================================================
echo   DEPLOY: CYBER DEFENSE TYCOON
echo   Publicando no GitHub Pages (gratuito)
echo ================================================
echo.

:: Navega para a pasta do jogo
cd /d "%~dp0"

:: Verifica se git esta instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Git nao encontrado! Instale em: https://git-scm.com
    pause
    exit /b 1
)

echo [1/5] Inicializando repositorio git...
git init
git checkout -b main

echo [2/5] Adicionando arquivos do jogo...
git add index.html style.css game.js

echo [3/5] Fazendo commit inicial...
git commit -m "feat: Cyber Defense Tycoon v1.0 - Jogo de ciberseguranca"

echo.
echo [4/5] Configurando remote para GitHub...
echo.
echo =========================================================
echo  ACAO NECESSARIA:
echo  1. Acesse: https://github.com/new
echo  2. Crie um repositorio chamado: cyber-defense-tycoon
echo  3. Deixe PUBLICO e NAO inicialize com README
echo  4. Copie o link HTTPS do repositorio
echo  5. Cole aqui abaixo e pressione ENTER:
echo =========================================================
echo.
set /p REPO_URL="Cole o link do repositorio aqui: "

git remote add origin %REPO_URL%

echo [5/5] Enviando para o GitHub...
git push -u origin main

echo.
echo ================================================
echo  ULTIMO PASSO - GitHub Pages:
echo  1. Va em: %REPO_URL%/settings/pages
echo  2. Em "Source" selecione "Deploy from branch"
echo  3. Em "Branch" escolha "main" e pasta "/(root)"
echo  4. Clique em SAVE
echo  5. Aguarde ~2 minutos
echo.
echo  Seu jogo estara disponivel em:
echo  https://INGUERSON.github.io/cyber-defense-tycoon/
echo ================================================
echo.
pause
