@echo off
REM Script para iniciar Bot + API com um único comando
REM Uso: iniciar.bat (ou clique duas vezes)

chcp 65001 >nul
echo.
echo ============================================================
echo   🚀 Iniciando Bot e API...
echo ============================================================
echo.

REM Verifica se está na pasta correta
if not exist "bot\bot.py" (
    echo [❌ ERRO] Execute este script na pasta raiz do projeto!
    echo           Pasta atual: %CD%
    echo.
    pause
    exit /b 1
)

REM Verifica se o .env existe
if not exist "bot\.env" (
    echo [⚠️  AVISO] Arquivo bot\.env nao encontrado!
    echo             Crie o arquivo .env na pasta bot/ com suas credenciais
    echo.
)

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [❌ ERRO] Python nao encontrado!
    echo          Instale Python de: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [✅ OK] Python encontrado: %PYTHON_VERSION%

REM Verifica dependências básicas
echo [🔍] Verificando dependências...
python -c "import telegram; import fastapi; import uvicorn" >nul 2>&1
if errorlevel 1 (
    echo [⚠️  ] Instalando dependências...
    cd bot
    pip install -r requirements.txt
    cd ..
    echo [✅] Dependências instaladas
) else (
    echo [✅] Dependências OK
)

echo.
echo ============================================================
echo   🤖 Iniciando Bot do Telegram + API (porta 8080)
echo ============================================================
echo.
echo 📝 O que esta rodando:
echo    • Bot do Telegram (comandos admin)
echo    • API HTTP na porta 8080
echo    • Monitoramento de pagamentos
echo.
echo 💡 Para testar o site:
echo    Abra outro terminal e execute: python -m http.server 3000
echo    Depois acesse: http://localhost:3000
echo.
echo 🛑 Para parar: Pressione CTRL+C
echo.
echo ============================================================
echo.

REM Inicia o bot (que já inicia a API automaticamente)
cd bot
python bot.py

REM Se der erro, tente:
REM python -m bot.bot

