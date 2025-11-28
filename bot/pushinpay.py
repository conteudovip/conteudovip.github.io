from __future__ import annotations

import base64
from typing import Optional
import logging

import requests

from config import settings

log = logging.getLogger(__name__)


class PushinPayClient:
  def __init__(self):
    self._api_key: Optional[str] = settings.pushinpay_api_key
    self._base_url: str = settings.pushinpay_base_url

  def _auth_headers(self) -> dict:
    """Retorna headers de autenticação"""
    if not self._api_key:
      error_msg = "PUSHINPAY_API_KEY não configurado!"
      log.error(error_msg)
      raise ValueError(error_msg)
    
    return {
      "Authorization": f"Bearer {self._api_key}",
      "Accept": "application/json",
      "Content-Type": "application/json",
    }

  def create_pix(self, amount: float, description: str, reference_id: str) -> dict:
    """
    Cria um PIX usando a API PushinPay
    
    Args:
      amount: Valor em reais (float)
      description: Descrição do pagamento (não usado na API, mas mantido para compatibilidade)
      reference_id: ID de referência único (não usado na API, mas mantido para compatibilidade)
    
    Returns:
      dict com os dados do PIX criado
    """
    # PushinPay trabalha com valores em centavos (mínimo 50 centavos)
    amount_cents = int(amount * 100)
    
    if amount_cents < 50:
      raise ValueError("Valor mínimo é R$ 0,50 (50 centavos)")
    
    # Baseado na documentação oficial: https://app.theneo.io/pushinpay/pix/pix/criar-pix
    # Endpoint correto: /pix/cashIn
    # Body: { "value": number, "webhook_url": string (opcional), "split_rules": array (opcional) }
    payload = {
      "value": amount_cents,  # Valor em centavos (mínimo 50)
    }
    
    # URL base: https://api.pushinpay.com.br/api
    # Endpoint: /pix/cashIn
    url = f"{self._base_url}/pix/cashIn"
    
    log.info("Criando PIX PushinPay - URL: %s", url)
    log.info("Criando PIX PushinPay - Payload: %s", payload)
    log.info("Criando PIX PushinPay - API Key configurada: %s", "SIM" if self._api_key else "NÃO")
    
    try:
      headers = self._auth_headers()
      log.info("Criando PIX PushinPay - Headers (sem token): %s", {k: v[:20] + "..." if len(v) > 20 else v for k, v in headers.items()})
      
      response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=20,
      )
      
      log.info("Criando PIX PushinPay - Status: %s", response.status_code)
      log.info("Criando PIX PushinPay - Response: %s", response.text[:500])
      
      if response.status_code == 404:
        error_msg = (
          f"Endpoint não encontrado (404): {url}\n"
          f"Verifique se a URL está correta no arquivo .env\n"
          f"URL configurada: {self._base_url}"
        )
        log.error(error_msg)
        raise requests.exceptions.HTTPError(error_msg, response=response)
      
      response.raise_for_status()
      data = response.json()
      
      log.info("Criando PIX PushinPay - Sucesso! Response: %s", data)
      
      # Log específico do QR Code
      qr_base64 = data.get("qr_code_base64") or data.get("qrCodeBase64")
      if qr_base64:
        log.info(f"QR Code base64 recebido: SIM (tamanho: {len(qr_base64)} caracteres)")
        log.info(f"QR Code base64 (primeiros 50 chars): {qr_base64[:50]}...")
      else:
        log.warning("QR Code base64 NÃO recebido na resposta da API PushinPay")
        log.info("Campos disponíveis na resposta: %s", list(data.keys()))
      
      return data
      
    except requests.exceptions.HTTPError as e:
      if e.response is not None:
        log.error("Erro HTTP ao criar PIX PushinPay: %s - %s", e.response.status_code, e.response.text[:500])
      else:
        log.error("Erro HTTP ao criar PIX PushinPay: %s", str(e))
      raise
    except Exception as e:
      log.exception("Erro inesperado ao criar PIX PushinPay")
      raise

  def get_transaction(self, transaction_id: str) -> dict:
    """
    Consulta uma transação PIX
    
    Args:
      transaction_id: ID da transação
    
    Returns:
      dict com os dados da transação
    """
    # Baseado na documentação: GET /transactions/{id}
    # https://app.theneo.io/pushinpay/pix/pix/consultar-pix
    url = f"{self._base_url}/transactions/{transaction_id}"
    
    try:
      response = requests.get(
        url,
        headers=self._auth_headers(),
        timeout=20,
      )
      response.raise_for_status()
      return response.json()
    except Exception as e:
      log.exception("Erro ao consultar transação PushinPay")
      raise

  @staticmethod
  def generate_qr_base64(pix_code: str) -> str:
    """
    Gera QR Code em base64 a partir do código PIX
    
    Args:
      pix_code: Código PIX (copia e cola)
    
    Returns:
      String base64 da imagem do QR Code
    """
    import qrcode
    from io import BytesIO

    qr = qrcode.QRCode(version=4, box_size=6, border=2)
    qr.add_data(pix_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


pushinpay_client = PushinPayClient()

