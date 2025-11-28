#!/usr/bin/env python3
"""
Script unificado para iniciar Bot + API juntos
"""
from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from telegram.ext import Application

from bot import create_app, setup_handlers
from config import settings

# Configuração de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)


async def main():
    """Inicia Bot e API juntos"""
    
    # Verifica configurações essenciais
    if not settings.telegram_token:
        log.error("❌ TELEGRAM_BOT_TOKEN não configurado!")
        log.error("   Configure no arquivo bot/.env")
        sys.exit(1)
    
    if not settings.pushinpay_api_key:
        log.warning("⚠️ PUSHINPAY_API_KEY não configurado!")
        log.warning("   O sistema funcionará, mas não poderá gerar PIX")
    
    log.info("=" * 60)
    log.info("🚀 Iniciando Telegram Secrets Bot + API")
    log.info("=" * 60)
    
    # Cria aplicação do bot
    log.info("📱 Criando aplicação do Telegram Bot...")
    bot_app = Application.builder().token(settings.telegram_token).build()
    
    # Configura handlers
    log.info("⚙️ Configurando handlers do bot...")
    setup_handlers(bot_app)
    
    # Cria aplicação FastAPI
    log.info("🌐 Criando aplicação FastAPI...")
    api_app = create_app()
    
    # Configura uvicorn para rodar em background
    log.info("🔧 Configurando servidor HTTP...")
    
    config = uvicorn.Config(
        api_app,
        host="0.0.0.0",
        port=8080,
        log_level="info",
    )
    server = uvicorn.Server(config)
    
    # Inicia servidor HTTP em background
    log.info("✅ Servidor HTTP iniciando na porta 8080...")
    server_task = asyncio.create_task(server.serve())
    
    # Aguarda um pouco para o servidor iniciar
    await asyncio.sleep(1)
    
    log.info("=" * 60)
    log.info("✅ Sistema iniciado com sucesso!")
    log.info("")
    log.info("📱 Bot Telegram: Ativo")
    log.info("🌐 API HTTP: http://0.0.0.0:8080")
    log.info("")
    log.info("🛑 Para parar: Pressione CTRL+C")
    log.info("=" * 60)
    
    try:
        # Inicia o bot (bloqueia até CTRL+C)
        await bot_app.initialize()
        await bot_app.start()
        await bot_app.updater.start_polling()
        
        # Aguarda indefinidamente
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        log.info("\n🛑 Parando sistema...")
    finally:
        # Para o servidor HTTP
        server.should_exit = True
        await server_task
        
        # Para o bot
        await bot_app.updater.stop()
        await bot_app.stop()
        await bot_app.shutdown()
        
        log.info("✅ Sistema parado com sucesso!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("\n👋 Até logo!")
        sys.exit(0)

