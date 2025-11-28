from __future__ import annotations

import base64
import logging
import threading
from datetime import datetime
from io import BytesIO
from typing import Optional
from uuid import uuid4

import uvicorn

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from config import settings
from storage import store, Product, Payment
from pushinpay import pushinpay_client
from pathlib import Path

# Importa a API para iniciá-la junto com o bot
from api import app as api_app

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

# Importa gerador de páginas (depois do log)
try:
    from page_generator import generate_product_page
    PAGE_GENERATOR_AVAILABLE = True
except ImportError:
    PAGE_GENERATOR_AVAILABLE = False
    log.warning("page_generator não disponível - páginas não serão geradas automaticamente")

# Estados da conversa para adicionar produto
WAITING_IMAGE, WAITING_TITLE, WAITING_PRICE, WAITING_DESCRIPTION, WAITING_LINK = range(5)


def is_admin(user_id: Optional[int]) -> bool:
  return bool(user_id) and user_id in settings.telegram_admin_ids


def normalize_price(value: str) -> float:
  value = value.replace("R$", "").replace(",", ".").strip()
  return float(value)


def format_currency(value: float) -> str:
  return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


async def reply_admin_only(update: Update):
  await update.message.reply_text("Apenas administradores podem usar este comando.")


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  # Verifica se foi chamado com parâmetro (ex: /start pix-vip-pro)
  if context.args and len(context.args) > 0:
    param = context.args[0]
    if param.startswith("pix-"):
      # Redireciona para o comando /pix
      product_id = param.replace("pix-", "").strip()
      # Chama a função cmd_pix diretamente
      context.args = [product_id]
      return await cmd_pix(update, context)
  
  # Comando /start normal
  await update.message.reply_text(
      "🤖 *Painel Telegram Secrets*\n\n"
      "Comandos disponíveis:\n"
      "/produtos - Lista todos os produtos\n"
      "/addproduct - Adiciona um produto (interativo)\n"
      "/delproduct <id> - Remove um produto\n"
      "/stats - Estatísticas de vendas\n"
      "/pix <produto_id> - Gera Pix para um produto\n\n"
      "_Para comandos admin, você precisa estar na lista de administradores._",
      parse_mode="Markdown"
  )


async def cmd_produtos(update: Update, context: ContextTypes.DEFAULT_TYPE):
  products = store.list_products()
  if not products:
    await update.message.reply_text("Nenhum produto cadastrado.")
    return
  lines = ["Produtos disponíveis:"]
  for product in products:
    lines.append(f"- {product.product_id}: {product.title} ({format_currency(product.price)})")
  await update.message.reply_text("\n".join(lines))


async def cmd_add_product_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Inicia o fluxo de adição de produto"""
  if not is_admin(update.effective_user.id if update.effective_user else None):
    return await reply_admin_only(update)
  
  await update.message.reply_text(
      "📸 *Adicionar Novo Produto*\n\n"
      "Por favor, envie a imagem do produto:\n"
      "• Envie uma foto diretamente\n"
      "• Ou envie uma URL da imagem\n"
      "• Ou digite 'pular' para continuar sem imagem\n\n"
      "_Use /cancel para cancelar._",
      parse_mode="Markdown"
  )
  return WAITING_IMAGE


async def receive_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Recebe a imagem do produto (foto ou URL)"""
  image_url = None
  
  # Verifica se é uma foto
  if update.message.photo:
    photo = update.message.photo[-1]  # Foto de maior resolução
    file = await context.bot.get_file(photo.file_id)
    # Usa o file_path do Telegram (pode expirar, mas é a melhor opção por agora)
    image_url = file.file_path
  # Verifica se é uma URL de texto
  elif update.message.text and (
      update.message.text.startswith("http://") or
      update.message.text.startswith("https://")
  ):
    image_url = update.message.text.strip()
  elif update.message.text and update.message.text.lower() in ["pular", "skip", "sem imagem"]:
    image_url = None  # Sem imagem
  else:
    await update.message.reply_text(
        "📸 Por favor, envie uma imagem ou URL de imagem.\n\n"
        "_Você também pode digitar 'pular' para continuar sem imagem._\n"
        "_Ou envie /cancel para cancelar._",
        parse_mode="Markdown"
    )
    return WAITING_IMAGE
  
  context.user_data["product_image_url"] = image_url
  
  if image_url:
    msg = "✅ Imagem recebida!"
    if not image_url.startswith("http"):
      msg += "\n⚠️ _Para melhor compatibilidade, use URLs de imagem permanentes na próxima vez._"
  else:
    msg = "✅ Continuando sem imagem."
  
  await update.message.reply_text(
      f"{msg}\n\n"
      "📝 Agora envie o *título* do produto:\n\n"
      "_Ou envie /cancel para cancelar._",
      parse_mode="Markdown"
  )
  return WAITING_TITLE


async def receive_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Recebe o título do produto"""
  title = update.message.text.strip()
  
  if not title:
    await update.message.reply_text(
        "❌ O título não pode estar vazio!\n\n"
        "Por favor, envie o título do produto:\n"
        "_Ou envie /cancel para cancelar._",
        parse_mode="Markdown"
    )
    return WAITING_TITLE
  
  context.user_data["product_title"] = title
  
  await update.message.reply_text(
      f"✅ Título recebido: *{title}*\n\n"
      "💰 Agora envie o *preço* do produto:\n"
      "Exemplo: `29.90` ou `29,90`\n\n"
      "_Ou envie /cancel para cancelar._",
      parse_mode="Markdown"
  )
  return WAITING_PRICE


async def receive_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Recebe o preço do produto"""
  try:
    price_str = update.message.text.strip()
    
    if not price_str:
      await update.message.reply_text(
          "❌ O preço não pode estar vazio!\n\n"
          "Por favor, envie o preço do produto:\n"
          "Exemplo: `29.90` ou `29,90`\n\n"
          "_Ou envie /cancel para cancelar._",
          parse_mode="Markdown"
      )
      return WAITING_PRICE
    
    price = normalize_price(price_str)
    
    if price <= 0:
      await update.message.reply_text(
          "❌ O preço deve ser maior que zero!\n\n"
          "Por favor, envie um preço válido:\n"
          "Exemplo: `29.90` ou `29,90`\n\n"
          "_Ou envie /cancel para cancelar._",
          parse_mode="Markdown"
      )
      return WAITING_PRICE
    
    context.user_data["product_price"] = price
    
    await update.message.reply_text(
        f"✅ Preço recebido: *{format_currency(price)}*\n\n"
        "📝 Agora envie a *descrição* do produto:\n\n"
        "_Ou envie /cancel para cancelar._",
        parse_mode="Markdown"
    )
    return WAITING_DESCRIPTION
    
  except ValueError:
    await update.message.reply_text(
        "❌ Formato de preço inválido!\n\n"
        "Use um formato válido, exemplo: `29.90` ou `29,90`\n\n"
        "_Ou envie /cancel para cancelar._",
        parse_mode="Markdown"
    )
    return WAITING_PRICE


async def receive_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Recebe a descrição do produto"""
  description = update.message.text.strip()
  
  if not description:
    await update.message.reply_text(
        "❌ A descrição não pode estar vazia!\n\n"
        "Por favor, envie a descrição do produto:\n\n"
        "_Ou envie /cancel para cancelar._",
        parse_mode="Markdown"
    )
    return WAITING_DESCRIPTION
  
  context.user_data["product_description"] = description
  
  await update.message.reply_text(
      f"✅ Descrição recebida!\n\n"
      "🔗 Agora envie o *link secreto* do produto:\n"
      "Exemplo: `https://t.me/+vipproaccess` ou `https://meusite.com/vip`\n\n"
      "_Ou envie /cancel para cancelar._",
      parse_mode="Markdown"
  )
  return WAITING_LINK


async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Recebe o link secreto e finaliza a criação do produto"""
  try:
    secret_link = update.message.text.strip()
    
    if not secret_link:
      await update.message.reply_text(
          "❌ O link secreto não pode estar vazio!\n\n"
          "Por favor, envie o link secreto do produto:\n"
          "Exemplo: `https://t.me/+vipproaccess`\n\n"
          "_Ou envie /cancel para cancelar._",
          parse_mode="Markdown"
      )
      return WAITING_LINK
    
    # Recupera todos os dados do contexto
    title = context.user_data.get("product_title")
    price = context.user_data.get("product_price")
    description = context.user_data.get("product_description")
    image_url = context.user_data.get("product_image_url")
    
    if not all([title, price, description]):
      await update.message.reply_text(
          "❌ Erro: dados incompletos. Por favor, inicie novamente com /addproduct",
          parse_mode="Markdown"
      )
      # Limpa dados
      context.user_data.pop("product_title", None)
      context.user_data.pop("product_price", None)
      context.user_data.pop("product_description", None)
      context.user_data.pop("product_image_url", None)
      return ConversationHandler.END
    
    product_id = title.lower().replace(" ", "-").replace("/", "-")
    
    product = Product(
        product_id=product_id,
        title=title,
        price=price,
        currency="BRL",
        description=description,
        secret_link=secret_link,
        media_type="image",
        media_src=image_url,
        benefits=[],
        note="Liberação imediata",
        lifetime_text="Acesso vitalício incluído",
        category="Premium",
    )
    
    store.save_product(product)
    
    # Gera página HTML estática para o produto
    page_info = ""
    if PAGE_GENERATOR_AVAILABLE:
        try:
            # Pasta raiz do projeto (subindo um nível de bot/)
            project_root = Path(__file__).parent.parent
            page_path = generate_product_page(product, project_root)
            page_info = f"\n📄 *Página criada:* `{page_path.name}`"
            log.info(f"Página gerada: {page_path}")
        except Exception as e:
            log.warning(f"Erro ao gerar página para produto {product.product_id}: {e}")
    
    # Gera arquivo JSON estático para GitHub Pages
    try:
        import json
        project_root = Path(__file__).parent.parent
        json_file = project_root / "products.json"
        products = store.list_products()
        products_data = []
        for p in products:
            products_data.append({
                "product_id": p.product_id,
                "title": p.title,
                "price": p.price,
                "currency": p.currency,
                "description": p.description,
                "media_type": p.media_type,
                "media_src": p.media_src,
                "media_poster": p.media_poster,
                "benefits": p.benefits,
                "note": p.note,
                "lifetime_text": p.lifetime_text,
                "category": p.category,
            })
        json_file.write_text(
            json.dumps(products_data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        log.info(f"Arquivo products.json atualizado com {len(products_data)} produto(s)")
    except Exception as e:
        log.warning(f"Erro ao gerar products.json: {e}")
    
    # Limpa dados temporários
    context.user_data.pop("product_title", None)
    context.user_data.pop("product_price", None)
    context.user_data.pop("product_description", None)
    context.user_data.pop("product_image_url", None)
    
    await update.message.reply_text(
        f"✅ *Produto criado com sucesso!*\n\n"
        f"📦 *Título:* {product.title}\n"
        f"💰 *Preço:* {format_currency(product.price)}\n"
        f"📝 *Descrição:* {product.description}\n"
        f"🔗 *Link:* {product.secret_link}\n"
        f"🆔 *ID:* `{product.product_id}`"
        f"{page_info}\n\n"
        f"O produto já está disponível no site!",
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END
    
  except Exception as e:
    log.exception("Erro ao criar produto")
    await update.message.reply_text(
        f"❌ Erro ao criar produto: {e}\n\n"
        "Tente novamente ou envie /cancel para cancelar.",
        parse_mode="Markdown"
    )
    return WAITING_LINK


async def cancel_add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Cancela a adição de produto"""
  # Limpa todos os dados temporários
  context.user_data.pop("product_image_url", None)
  context.user_data.pop("product_title", None)
  context.user_data.pop("product_price", None)
  context.user_data.pop("product_description", None)
  await update.message.reply_text("❌ Operação cancelada.")
  return ConversationHandler.END


async def cmd_del_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not is_admin(update.effective_user.id if update.effective_user else None):
    return await reply_admin_only(update)
  if not context.args:
    return await update.message.reply_text("Use /delproduct <produto_id>")
  product_id = context.args[0]
  store.delete_product(product_id)
  await update.message.reply_text(f"Produto '{product_id}' removido (se existia).")


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not is_admin(update.effective_user.id if update.effective_user else None):
    return await reply_admin_only(update)
  products = store.list_products()
  payments = store.list_payments()
  pending = sum(1 for p in payments if p.status == "pending")
  paid = sum(1 for p in payments if p.status == "paid")
  total_revenue = sum(p.price for p in payments if p.status == "paid")
  await update.message.reply_text(
      f"Produtos: {len(products)}\n"
      f"Pagamentos pendentes: {pending}\n"
      f"Pagamentos confirmados: {paid}\n"
      f"Receita confirmada: {format_currency(total_revenue)}"
  )


async def cmd_pix(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Gera PIX para um produto. Pode ser chamado via /pix <id> ou /start pix-<id>"""
  product_id = None
  
  # Verifica se foi chamado via /start pix-<id>
  if update.message and update.message.text:
    text = update.message.text.strip()
    if text.startswith("/start pix-"):
      product_id = text.replace("/start pix-", "").strip()
    elif len(context.args) >= 1:
      product_id = context.args[0]
  elif len(context.args) >= 1:
    product_id = context.args[0]
  
  if not product_id:
    return await update.message.reply_text(
      "💳 *Gerar PIX*\n\n"
      "Use: `/pix <produto_id>`\n"
      "Exemplo: `/pix vip-pro`\n\n"
      "Ou acesse o produto no site e clique em 'Gerar PIX'",
      parse_mode="Markdown"
    )
  
  product = store.get_product(product_id)
  if not product:
    return await update.message.reply_text(
      f"❌ Produto `{product_id}` não encontrado.\n\n"
      "Use `/produtos` para ver a lista de produtos disponíveis.",
      parse_mode="Markdown"
    )

  customer_id = update.effective_user.id if update.effective_user else 0
  payment_id = f"{product.product_id}-{uuid4().hex[:8]}"
  try:
    pix = pushinpay_client.create_pix(product.price, product.description, payment_id)
  except Exception as exc:
    log.exception("Erro ao criar Pix")
    return await update.message.reply_text(f"Erro ao gerar Pix: {exc}")

  # PushinPay retorna: { "id", "qr_code", "status", "value", "qr_code_base64", ... }
  pix_code = pix.get("qr_code") or ""
  if not pix_code:
    return await update.message.reply_text("Gateway não retornou código Pix.")
  qr_base64 = (
    pix.get("qr_code_base64") 
    or pushinpay_client.generate_qr_base64(pix_code)
  )

  payment = Payment(
      payment_id=payment_id,
      product_id=product.product_id,
      product_title=product.title,
      customer_id=customer_id,
      customer_ref=str(customer_id or uuid4()),
      price=product.price,
      pix_code=pix_code,
      qr_base64=qr_base64,
      status="pending",
      created_at=datetime.utcnow().isoformat(),
      updated_at=datetime.utcnow().isoformat(),
      # PushinPay retorna "id" como identificador único da transação
      syncpay_id=pix.get("id") or payment_id,
      secret_link=product.secret_link or settings.secret_access_url,
  )
  store.save_payment(payment)

  message = (
      f"💳 Pagamento gerado para *{product.title}*\n"
      f"Valor: {format_currency(product.price)}\n"
      f"Código Pix (copia e cola):\n`{pix_code}`\n\n"
      "Assim que o Pix for confirmado você receberá o link automaticamente."
  )
  await update.message.reply_markdown(message)

  if qr_base64:
    image = BytesIO(base64.b64decode(qr_base64))
    image.name = "pix.png"
    await update.message.reply_photo(photo=image, caption="Escaneie o QR Code para pagar.")


async def payment_monitor(app: Application):
  pending = store.find_pending_payments()
  for payment in pending:
    if not payment.syncpay_id:
      continue
    try:
      data = pushinpay_client.get_transaction(payment.syncpay_id)
    except Exception:
      continue
    # PushinPay retorna: "created" | "paid" | "canceled"
    status = data.get("status", "").lower()
    if status == "paid":
      store.update_payment_status(payment.payment_id, "paid")
      link = payment.secret_link or settings.secret_access_url
      if payment.customer_id:
        try:
          await app.bot.send_message(
              chat_id=payment.customer_id,
              text=(
                  f"✅ Pagamento confirmado para {payment.product_title}!\n"
                  f"Link liberado: {link}"
              ),
          )
        except Exception as exc:
          log.warning("Falha ao enviar link para %s: %s", payment.customer_id, exc)


async def payment_job(context: ContextTypes.DEFAULT_TYPE):
  await payment_monitor(context.application)


def start_api_server():
  """Inicia o servidor FastAPI em uma thread separada"""
  api_host = "0.0.0.0"
  api_port = 8080
  
  log.info(f"Iniciando API na porta {api_port}...")
  uvicorn.run(
      api_app,
      host=api_host,
      port=api_port,
      log_level="info",
      access_log=False,  # Reduz logs para não poluir
  )


def main():
  if not settings.telegram_token:
    raise RuntimeError("TELEGRAM_BOT_TOKEN não configurado.")

  # Inicia a API em uma thread separada
  api_thread = threading.Thread(target=start_api_server, daemon=True)
  api_thread.start()
  log.info("API iniciada em thread separada. Aguardando inicialização...")
  
  # Dá um tempo para a API inicializar
  import time
  time.sleep(2)

  application = Application.builder().token(settings.telegram_token).build()
  
  # Obtém username do bot automaticamente
  async def get_bot_username(context: ContextTypes.DEFAULT_TYPE):
    try:
      bot_info = await application.bot.get_me()
      if bot_info.username:
        settings.telegram_bot_username = bot_info.username
        log.info(f"Bot username detectado: @{bot_info.username}")
    except Exception as e:
      log.warning(f"Não foi possível obter username do bot: {e}")
  
  # Handler conversacional para adicionar produto
  add_product_handler = ConversationHandler(
      entry_points=[CommandHandler("addproduct", cmd_add_product_start)],
      states={
          WAITING_IMAGE: [
              MessageHandler(filters.PHOTO | filters.TEXT, receive_image),
              CommandHandler("cancel", cancel_add_product),
          ],
          WAITING_TITLE: [
              MessageHandler(filters.TEXT & ~filters.COMMAND, receive_title),
              CommandHandler("cancel", cancel_add_product),
          ],
          WAITING_PRICE: [
              MessageHandler(filters.TEXT & ~filters.COMMAND, receive_price),
              CommandHandler("cancel", cancel_add_product),
          ],
          WAITING_DESCRIPTION: [
              MessageHandler(filters.TEXT & ~filters.COMMAND, receive_description),
              CommandHandler("cancel", cancel_add_product),
          ],
          WAITING_LINK: [
              MessageHandler(filters.TEXT & ~filters.COMMAND, receive_link),
              CommandHandler("cancel", cancel_add_product),
          ],
      },
      fallbacks=[CommandHandler("cancel", cancel_add_product)],
  )
  
  application.add_handler(CommandHandler("start", cmd_start))
  application.add_handler(CommandHandler("help", cmd_start))
  application.add_handler(CommandHandler("produtos", cmd_produtos))
  application.add_handler(add_product_handler)
  application.add_handler(CommandHandler("delproduct", cmd_del_product))
  application.add_handler(CommandHandler("stats", cmd_stats))
  application.add_handler(CommandHandler("pix", cmd_pix))

  application.job_queue.run_repeating(payment_job, interval=30, first=5)
  
  # Agenda obtenção do username após o bot iniciar
  application.job_queue.run_once(get_bot_username, when=1)

  log.info("🤖 Bot iniciado! API rodando na porta 8080.")
  log.info("✅ Tudo funcionando! Use /start no Telegram para começar.")
  
  application.run_polling()


if __name__ == "__main__":
  main()

