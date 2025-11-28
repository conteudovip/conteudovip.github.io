from __future__ import annotations

import asyncio
from dataclasses import asdict
from datetime import datetime
from typing import Optional, List
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from config import settings
from storage import store, Product, Payment
from pushinpay import pushinpay_client
import requests

app = FastAPI(title="Telegram Secrets Backend")

# Configuração de CORS
# Permite origens configuradas ou todas por padrão
origins = settings.allowed_origins or ["*"]

# Garante que localhost está sempre permitido para desenvolvimento
if not origins or origins == ["*"] or "*" in origins:
    allow_origins = ["*"]
else:
    # Adiciona localhost mesmo se não estiver na lista
    allow_origins = list(set(origins + [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]))

# Aplica o middleware CORS - IMPORTANTE: deve ser adicionado antes de qualquer rota
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


class CheckoutRequest(BaseModel):
  product_id: str
  customer_ref: Optional[str] = None


class CheckoutResponse(BaseModel):
  payment_id: str
  product_id: str
  product_title: str
  price: float
  status: str
  pix_code: str
  qr_base64: Optional[str]
  note: Optional[str] = None
  lifetime_text: Optional[str] = None


class WebhookPayload(BaseModel):
  reference_id: str
  status: str


class ProductPayload(BaseModel):
  product_id: str
  title: str
  price: float
  currency: str = "BRL"
  description: str
  secret_link: str
  media_type: str = Field(default="image", pattern="^(image|video)$")
  media_src: Optional[str] = None
  media_poster: Optional[str] = None
  benefits: List[str] = Field(default_factory=list)
  note: str = "Liberação imediata"
  lifetime_text: str = "Acesso vitalício incluído"
  category: str = "Premium"


def require_admin(token: Optional[str] = Header(None, alias="X-Admin-Token")):
  if settings.admin_api_token and token != settings.admin_api_token:
    raise HTTPException(status_code=403, detail="Unauthorized")


@app.get("/")
def root():
  """Rota raiz - informações da API"""
  return {
    "status": "ok",
    "api": "Telegram Secrets Backend",
    "endpoints": {
      "health": "/health",
      "products": "/products",
      "checkout": "/checkout (POST)",
      "payment_status": "/payments/{payment_id}"
    }
  }


@app.get("/health")
def health():
  return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.get("/products")
def list_products():
  """Lista todos os produtos disponíveis"""
  try:
    products = store.list_products()
    result = [asdict(product) for product in products]
    # Log para debug
    import logging
    log = logging.getLogger(__name__)
    log.info(f"Listando produtos: {len(result)} encontrado(s)")
    return result
  except Exception as e:
    import logging
    log = logging.getLogger(__name__)
    log.exception("Erro ao listar produtos")
    raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")


@app.post("/products", dependencies=[Depends(require_admin)])
def create_product(payload: ProductPayload):
  product = Product(**payload.dict())
  store.save_product(product)
  return {"status": "saved"}


@app.delete("/products/{product_id}", dependencies=[Depends(require_admin)])
def delete_product(product_id: str):
  store.delete_product(product_id)
  return {"status": "removed"}


@app.post("/checkout", response_model=CheckoutResponse)
def create_checkout(payload: CheckoutRequest):
  product = store.get_product(payload.product_id)
  if not product:
    raise HTTPException(status_code=404, detail="Produto não encontrado.")

  payment_id = f"{product.product_id}-{uuid4().hex[:8]}"
  customer_ref = payload.customer_ref or uuid4().hex

  try:
    pix = pushinpay_client.create_pix(
        amount=product.price,
        description=product.description,
        reference_id=payment_id,
    )
  except ValueError as exc:
    # Erro de configuração (credenciais faltando)
    raise HTTPException(status_code=500, detail=f"Configuração PushinPay inválida: {exc}") from exc
  except requests.exceptions.HTTPError as exc:
    # Erro HTTP da API PushinPay
    error_detail = f"Erro ao gerar Pix: {exc}"
    if exc.response is not None:
      status_code = exc.response.status_code
      if status_code == 404:
        error_detail = (
          f"Endpoint PushinPay não encontrado (404). "
          f"Verifique se a URL está correta no arquivo .env: {settings.pushinpay_base_url}. "
          f"URL padrão: https://api.pushinpay.com.br"
        )
      else:
        try:
          error_data = exc.response.json()
          error_detail = f"Erro ao gerar Pix ({status_code}): {error_data.get('detail', error_data.get('message', error_data.get('error', str(exc))))}"
        except:
          error_detail = f"Erro ao gerar Pix ({status_code}): {exc.response.text[:200]}"
    raise HTTPException(status_code=502, detail=error_detail) from exc
  except Exception as exc:
    raise HTTPException(status_code=502, detail=f"Erro ao gerar Pix: {exc}") from exc

  # PushinPay retorna: { "id", "qr_code", "status", "value", "qr_code_base64", ... }
  # Baseado na documentação oficial: https://app.theneo.io/pushinpay/pix/pix/criar-pix
  pix_code = pix.get("qr_code") or ""
  
  if not pix_code:
    raise HTTPException(status_code=502, detail="Gateway não retornou o código Pix.")

  # PushinPay retorna qr_code_base64 diretamente
  # Pode vir como "qr_code_base64" ou "qrCodeBase64" ou precisamos gerar
  qr_base64 = (
      pix.get("qr_code_base64")
      or pix.get("qrCodeBase64")
      or pushinpay_client.generate_qr_base64(pix_code)
  )
  
  # Log para debug
  import logging
  log = logging.getLogger(__name__)
  log.info(f"QR Code base64: {'SIM' if qr_base64 else 'NÃO'} (tamanho: {len(qr_base64) if qr_base64 else 0})")

  payment = Payment(
      payment_id=payment_id,
      product_id=product.product_id,
      product_title=product.title,
      customer_id=0,
      customer_ref=customer_ref,
      price=product.price,
      pix_code=pix_code,
      qr_base64=qr_base64,
      status="pending",
      created_at=datetime.utcnow().isoformat(),
      updated_at=datetime.utcnow().isoformat(),
      # PushinPay retorna "id" como identificador único da transação
      syncpay_id=pix.get("id") or payment_id,
      secret_link=product.secret_link,
  )
  store.save_payment(payment)

  return CheckoutResponse(
      payment_id=payment.payment_id,
      product_id=product.product_id,
      product_title=product.title,
      price=product.price,
      status=payment.status,
      pix_code=pix_code,
      qr_base64=qr_base64,
      note=product.note,
      lifetime_text=product.lifetime_text,
  )


@app.get("/payments/{payment_id}")
def payment_status(payment_id: str):
  payment = store.get_payment(payment_id)
  if not payment:
    raise HTTPException(status_code=404, detail="Pagamento não encontrado.")
  response = payment.__dict__.copy()
  if payment.status != "paid":
    response.pop("secret_link", None)
  return response


@app.post("/webhooks/syncpay")
def syncpay_webhook(payload: WebhookPayload):
  status = payload.status.lower()
  store.update_payment_status(payload.reference_id, status)
  return {"status": "received"}


async def monitor_payments():
  while True:
    await asyncio.sleep(25)
    pending = store.find_pending_payments()
    for payment in pending:
      try:
        data = pushinpay_client.get_transaction(payment.syncpay_id or payment.payment_id)
      except Exception:
        continue
      # PushinPay retorna: "created" | "paid" | "canceled"
      status = data.get("status", "").lower()
      if status == "paid":
        store.update_payment_status(payment.payment_id, "paid")


@app.on_event("startup")
async def on_start():
  if not getattr(app.state, "monitor_task", None):
    app.state.monitor_task = asyncio.create_task(monitor_payments())

