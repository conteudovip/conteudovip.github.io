# Script para iniciar Bot + API com um único comando
# Uso: powershell -ExecutionPolicy Bypass -File iniciar.ps1

Write-Host "🚀 Iniciando Bot e API..." -ForegroundColor Green
Write-Host ""

# Verifica se está na pasta correta
if (-not (Test-Path "bot\bot.py")) {
    Write-Host "❌ Erro: Execute este script na pasta raiz do projeto!" -ForegroundColor Red
    Write-Host "   Pasta atual: $(Get-Location)" -ForegroundColor Yellow
    exit 1
}

# Verifica se o .env existe
if (-not (Test-Path "bot\.env")) {
    Write-Host "⚠️  AVISO: Arquivo bot\.env não encontrado!" -ForegroundColor Yellow
    Write-Host "   Crie o arquivo .env na pasta bot/ com suas credenciais" -ForegroundColor Yellow
    Write-Host ""
}

# Verifica se Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro: Python não encontrado!" -ForegroundColor Red
    Write-Host "   Instale Python de: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Verifica se as dependências estão instaladas
Write-Host "🔍 Verificando dependências..." -ForegroundColor Cyan
try {
    python -c "import telegram; import fastapi; import uvicorn" 2>&1 | Out-Null
    Write-Host "✅ Dependências OK" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Instalando dependências..." -ForegroundColor Yellow
    Set-Location bot
    pip install -r requirements.txt
    Set-Location ..
    Write-Host "✅ Dependências instaladas" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "🤖 Iniciando Bot do Telegram + API (porta 8080)" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 O que está rodando:" -ForegroundColor Yellow
Write-Host "   • Bot do Telegram (comandos admin)" -ForegroundColor White
Write-Host "   • API HTTP na porta 8080" -ForegroundColor White
Write-Host "   • Monitoramento de pagamentos" -ForegroundColor White
Write-Host ""
Write-Host "💡 Para testar o site:" -ForegroundColor Yellow
Write-Host "   Abra outro terminal e execute:" -ForegroundColor White
Write-Host "   python -m http.server 3000" -ForegroundColor Cyan
Write-Host "   Depois acesse: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "🛑 Para parar: Pressione CTRL+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Inicia o bot (que já inicia a API automaticamente)
Set-Location bot
python bot.py

