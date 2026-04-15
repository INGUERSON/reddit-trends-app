@echo off
set "dest=C:\Users\ingue\Downloads\Projetos_Arquivados"

echo Criando pasta "Projetos_Arquivados" em Downloads...
mkdir "%dest%" 2>nul

echo Movendo pastas de projetos...
move "Agentic-Design-Study" "%dest%\" 2>nul

echo Arquivando ai_shorts_generator...
set TIMESTAMP=%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%
set TIMESTAMP=%TIMESTAMP: =0%
move "ai_shorts_generator" "%dest%\ai_shorts_generator_%TIMESTAMP%" 2>nul

move "animated_site_study" "%dest%\" 2>nul
move "beginner-portfolio" "%dest%\" 2>nul
move "cybersecurity_tools" "%dest%\"
move "dashboard_saas" "%dest%\"
move "igor-portfolio" "%dest%\"
move "laia_assistant" "%dest%\"
move "landing_page_renda" "%dest%\"
move "linda_assistant" "%dest%\"
move "news_summarizer_bot" "%dest%\"

echo Movendo arquivos avulsos...
move "Controle_Laboratorio_Odontologia.xlsx" "%dest%\"
move "arquivo_suspeito_teste.txt" "%dest%\"
move "news_summarizer_bot_files.zip" "%dest%\"
move "reddit_trends_*.md" "%dest%\"
move "GEMINI-Construtor-de-Sites.md.txt" "%dest%\"

echo.
echo === LIMPEZA CONCLUÍDA! ===
echo Tudo foi movido para: C:\Users\ingue\Downloads\Projetos_Arquivados
echo Pressione qualquer tecla para sair...
pause
