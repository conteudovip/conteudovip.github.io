#!/bin/bash
# Script unificado para iniciar Bot + API
# Uso: ./start.sh

cd "$(dirname "$0")/bot" || exit 1

echo "============================================================"
echo "  🚀 Iniciando Bot e API..."
echo "============================================================"
echo ""

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Verifica .env
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo "   Crie o arquivo .env na pasta bot/ com suas credenciais"
    echo ""
fi

# Verifica dependências
echo "🔍 Verificando dependências..."
if ! python3 -c "import telegram; import fastapi; import uvicorn" 2>/dev/null; then
    echo "⚠️  Instalando dependências..."
    pip3 install -r requirements.txt
fi

echo ""
echo "============================================================"
echo "  🤖 Iniciando Bot do Telegram + API (porta 8080)"
echo "============================================================"
echo ""
echo "📝 O que está rodando:"
echo "   • Bot do Telegram (comandos admin)"
echo "   • API HTTP na porta 8080"
echo "   • Monitoramento de pagamentos"
echo ""
echo "🛑 Para parar: Pressione CTRL+C"
echo ""
echo "============================================================"
echo ""

# Inicia o bot (que já inicia a API automaticamente)
python3 bot.py

