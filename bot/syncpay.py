from __future__ import annotations

import base64
from datetime import datetime, timedelta
from typing import Optional
import logging

import requests

from config import settings

log = logging.getLogger(__name__)


class SyncPayClient:
  def __init__(self):
    self._token: Optional[str] = None
    self._expires_at: Optional[datetime] = None

  def _auth_headers(self) -> dict:
    now = datetime.utcnow()
    if not self._token or not self._expires_at or now >= self._expires_at:
      self._refresh_token()
    return {"Authorization": f"Bearer {self._token}"}

  def _refresh_token(self):
    if not settings.syncpay_client_id or not settings.syncpay_client_secret:
      error_msg = "SYNCPAY_CLIENT_ID ou SYNCPAY_CLIENT_SECRET não configurados!"
      log.error(error_msg)
      raise ValueError(error_msg)
    
    payload = {
        "client_id": settings.syncpay_client_id,
        "client_secret": settings.syncpay_client_secret,
    }
    
    log.info("Atualizando token SyncPay - URL: %s", settings.syncpay_auth_url)
    
    try:
      response = requests.post(settings.syncpay_auth_url, json=payload, timeout=20)
      log.info("Token SyncPay - Status: %s", response.status_code)
      
      if not response.ok:
        log.error("Token SyncPay - Erro: %s - %s", response.status_code, response.text)
      
      response.raise_for_status()
      data = response.json()
      self._token = data["access_token"]
      expires_in = data.get("expires_in", 3600)
      self._expires_at = datetime.utcnow() + timedelta(seconds=expires_in - 60)
      log.info("SyncPay token atualizado, expira em %s", self._expires_at)
    except requests.exceptions.HTTPError as e:
      log.error("Erro HTTP ao atualizar token: %s - %s", e.response.status_code, e.response.text)
      raise
    except Exception as e:
      log.exception("Erro inesperado ao atualizar token")
      raise

  def create_pix(self, amount: float, description: str, reference_id: str) -> dict:
    payload = {
        "amount": amount,
        "description": description[:90],
        "reference_id": reference_id,
    }
    
    log.info("Criando PIX - URL: %s", settings.syncpay_cashin_url)
    log.info("Criando PIX - Payload: %s", payload)
    log.info("Criando PIX - Client ID configurado: %s", "SIM" if settings.syncpay_client_id else "NÃO")
    
    try:
      headers = self._auth_headers()
      log.info("Criando PIX - Headers (sem token): %s", {k: v[:20] + "..." if len(v) > 20 else v for k, v in headers.items()})
      
      response = requests.post(
          settings.syncpay_cashin_url,
          json=payload,
          headers=headers,
          timeout=20,
      )
      
      log.info("Criando PIX - Status: %s", response.status_code)
      log.info("Criando PIX - Response: %s", response.text[:200])
      
      if response.status_code == 404:
        error_msg = (
          f"Endpoint não encontrado (404): {settings.syncpay_cashin_url}\n"
          f"Verifique se a URL está correta no arquivo .env\n"
          f"URL padrão sugerida: https://syncpay.apidog.io/api/partner/v1/pix/cashin"
        )
        log.error(error_msg)
        raise requests.exceptions.HTTPError(error_msg, response=response)
      
      response.raise_for_status()
      data = response.json()
      log.info("Criando PIX - Sucesso! Transaction ID: %s", data.get("transaction_id") or data.get("id"))
      return data
    except requests.exceptions.HTTPError as e:
      if e.response is not None:
        log.error("Erro HTTP ao criar PIX: %s - %s", e.response.status_code, e.response.text[:500])
      else:
        log.error("Erro HTTP ao criar PIX: %s", str(e))
      raise
    except Exception as e:
      log.exception("Erro inesperado ao criar PIX")
      raise

  def get_transaction(self, transaction_id: str) -> dict:
    url = f"{settings.syncpay_transaction_url}/{transaction_id}"
    response = requests.get(url, headers=self._auth_headers(), timeout=20)
    response.raise_for_status()
    return response.json()

  @staticmethod
  def generate_qr_base64(pix_code: str) -> str:
    import qrcode
    from io import BytesIO

    qr = qrcode.QRCode(version=4, box_size=6, border=2)
    qr.add_data(pix_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


syncpay_client = SyncPayClient()

