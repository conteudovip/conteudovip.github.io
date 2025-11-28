@echo off
REM Script para verificar se a API está rodando
chcp 65001 >nul
echo.
echo ============================================================
echo   🔍 Verificando se a API está rodando...
echo ============================================================
echo.

REM Testa se a API responde
echo [1/3] Testando conexão com a API...
curl -s http://localhost:8080/health >nul 2>&1
if errorlevel 1 (
    echo [❌] API não está respondendo na porta 8080
    echo.
    echo 💡 SOLUÇÃO:
    echo    1. Execute: iniciar.bat
    echo    2. Ou: cd bot ^&^& python bot.py
    echo    3. Aguarde aparecer "Bot iniciado!"
    echo.
) else (
    echo [✅] API está respondendo!
    echo.
    echo [2/3] Testando endpoint de produtos...
    curl -s http://localhost:8080/products >nul 2>&1
    if errorlevel 1 (
        echo [⚠️ ] Endpoint /products não respondeu
    ) else (
        echo [✅] Endpoint /products OK
    )
    echo.
    echo [3/3] Abrindo no navegador...
    start http://localhost:8080/health
    echo [✅] Página aberta no navegador
    echo.
)

echo ============================================================
echo   📋 Status:
echo ============================================================
echo.
echo Para testar manualmente:
echo   • API Health: http://localhost:8080/health
echo   • Produtos: http://localhost:8080/products
echo.
echo Se a API não estiver rodando:
echo   1. Execute: iniciar.bat
echo   2. Aguarde aparecer "Bot iniciado!"
echo   3. Recarregue a página do site
echo.
pause

