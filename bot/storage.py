from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from config import settings


@dataclass
class Product:
  product_id: str
  title: str
  price: float
  currency: str
  description: str
  secret_link: str
  media_type: str = "image"
  media_src: Optional[str] = None
  media_poster: Optional[str] = None
  benefits: List[str] = field(default_factory=list)
  note: str = "Liberação imediata"
  lifetime_text: str = "Acesso vitalício incluído"
  category: str = "Premium"


@dataclass
class Payment:
  payment_id: str
  product_id: str
  product_title: str
  customer_id: int
  customer_ref: str
  price: float
  pix_code: str
  qr_base64: Optional[str]
  status: str
  created_at: str
  updated_at: str
  syncpay_id: Optional[str] = None
  secret_link: str = ""


class DataStore:
  def __init__(self, base_dir: Path = settings.data_dir):
    self.base_dir = base_dir
    self.products_file = self.base_dir / "products.json"
    self.payments_file = self.base_dir / "payments.json"
    self.products_file.touch(exist_ok=True)
    self.payments_file.touch(exist_ok=True)

  def _read(self, path: Path) -> Dict:
    try:
      # Tenta UTF-8 primeiro, depois latin-1 (compatível com Windows)
      try:
        content = path.read_text(encoding="utf-8")
      except UnicodeDecodeError:
        content = path.read_text(encoding="latin-1")
      return json.loads(content or "{}")
    except json.JSONDecodeError:
      return {}

  def _write(self, path: Path, data: Dict):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

  # Products
  def list_products(self) -> List[Product]:
    raw = self._read(self.products_file)
    items = []
    import logging
    log = logging.getLogger(__name__)
    log.info(f"Lendo produtos do arquivo: {self.products_file}")
    log.info(f"Produtos brutos encontrados: {len(raw)}")
    for obj in raw.values():
      try:
        # Garante que todos os campos obrigatórios existem
        product_data = {
          "product_id": obj.get("product_id", ""),
          "title": obj.get("title", ""),
          "price": float(obj.get("price", 0)),
          "currency": obj.get("currency", "BRL"),
          "description": obj.get("description", ""),
          "secret_link": obj.get("secret_link", ""),
          "media_type": obj.get("media_type", "image"),
          "media_src": obj.get("media_src"),
          "media_poster": obj.get("media_poster"),
          "benefits": obj.get("benefits", []),
          "note": obj.get("note", "Liberação imediata"),
          "lifetime_text": obj.get("lifetime_text", "Acesso vitalício incluído"),
          "category": obj.get("category", "Premium"),
        }
        items.append(Product(**product_data))
      except (TypeError, KeyError, ValueError) as e:
        log.warning(f"Erro ao criar Product: {e}, dados: {obj}")
        continue
    log.info(f"Produtos válidos retornados: {len(items)}")
    return items

  def save_product(self, product: Product):
    data = self._read(self.products_file)
    data[product.product_id] = asdict(product)
    self._write(self.products_file, data)

  def get_product(self, product_id: str) -> Optional[Product]:
    data = self._read(self.products_file)
    obj = data.get(product_id)
    if not obj:
      return None
    return Product(**obj)

  def delete_product(self, product_id: str):
    data = self._read(self.products_file)
    if product_id in data:
      data.pop(product_id)
      self._write(self.products_file, data)

  # Payments
  def save_payment(self, payment: Payment):
    data = self._read(self.payments_file)
    data[payment.payment_id] = asdict(payment)
    self._write(self.payments_file, data)

  def update_payment_status(self, payment_id: str, status: str):
    data = self._read(self.payments_file)
    if payment_id not in data:
      return
    data[payment_id]["status"] = status
    data[payment_id]["updated_at"] = datetime.utcnow().isoformat()
    self._write(self.payments_file, data)

  def get_payment(self, payment_id: str) -> Optional[Payment]:
    data = self._read(self.payments_file)
    obj = data.get(payment_id)
    if not obj:
      return None
    return Payment(**obj)

  def find_pending_payments(self) -> List[Payment]:
    data = self._read(self.payments_file)
    pending = []
    for obj in data.values():
      if obj.get("status") == "pending":
        pending.append(Payment(**obj))
    return pending

  def list_payments(self) -> List[Payment]:
    data = self._read(self.payments_file)
    payments: List[Payment] = []
    for obj in data.values():
      try:
        payments.append(Payment(**obj))
      except TypeError:
        continue
    return payments


store = DataStore()

