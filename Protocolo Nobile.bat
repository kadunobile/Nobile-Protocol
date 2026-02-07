@echo off
chcp 65001 > nul
color 0A
mode con: cols=80 lines=30
title Protocolo Nóbile - Iniciando...

cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                                                                    ║
echo ║           🎯  PROTOCOLO NÓBILE                                     ║
echo ║           Sistema de Inteligência de Carreira Executiva           ║
echo ║                                                                    ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERRO: Python não encontrado!
    echo.
    echo Instale Python em: https://www.python.org/downloads/
    echo IMPORTANTE: Marque "Add Python to PATH" durante instalação
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ %PYTHON_VERSION% detectado
echo.

echo [2/4] Verificando arquivo de configuração...
if not exist config.py (
    if not exist .env (
        echo.
        echo ⚠️  Arquivo config.py não encontrado!
        echo.
        echo Criando config.py...
        echo OPENAI_API_KEY = "sua-chave-aqui" > config.py
        echo.
        echo 📝 Abra o arquivo config.py e adicione sua OpenAI API Key
        notepad config.py
        echo.
        echo Após salvar a chave, execute este arquivo novamente.
        echo.
        pause
        exit /b 1
    )
)
echo ✅ Configuração encontrada
echo.

echo [3/4] Verificando dependências...
python -c "import streamlit, openai, PyPDF2" >nul 2>&1
if errorlevel 1 (
    echo.
    echo 📦 Instalando pacotes necessários...
    echo    Isso pode levar 2-3 minutos na primeira vez...
    echo.
    python -m pip install --quiet --upgrade pip
    python -m pip install --quiet streamlit openai PyPDF2 python-dotenv
    if errorlevel 1 (
        echo.
        echo ❌ Erro ao instalar dependências
        pause
        exit /b 1
    )
    echo ✅ Instalação concluída!
) else (
    echo ✅ Todas as dependências instaladas
)
echo.

echo [4/4] Iniciando aplicação...
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                                                                    ║
echo ║  ✅ Sistema iniciado com sucesso!                                  ║
echo ║                                                                    ║
echo ║  🌐 O navegador abrirá automaticamente em instantes...            ║
echo ║                                                                    ║
echo ║  📍 Endereço local: http://localhost:8501                         ║
echo ║                                                                    ║
echo ║  ⚠️  Para ENCERRAR: Feche esta janela ou pressione Ctrl+C        ║
echo ║                                                                    ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo Aguardando carregamento...
echo.

python -m streamlit run app.py --server.headless true --server.port 8501

echo.
echo.
echo ═══════════════════════════════════════════════════════════════════
echo   Aplicação encerrada.
echo ═══════════════════════════════════════════════════════════════════
echo.
pause