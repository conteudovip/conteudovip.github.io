from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
  load_dotenv(ENV_PATH)
else:
  load_dotenv()


def _csv_to_list(value: str | None) -> List[int]:
  if not value:
    return []
  ids = []
  for chunk in value.split(","):
    chunk = chunk.strip()
    if not chunk:
      continue
    try:
      ids.append(int(chunk))
    except ValueError:
      continue
  return ids


@dataclass
class Settings:
  telegram_token: str
  telegram_admin_ids: List[int]
  syncpay_auth_url: str
  syncpay_cashin_url: str
  syncpay_transaction_url: str
  syncpay_client_id: str
  syncpay_client_secret: str
  pushinpay_api_key: str
  pushinpay_base_url: str
  web_base_url: str
  secret_access_url: str
  admin_api_token: str
  allowed_origins: List[str]
  data_dir: Path = BASE_DIR / "data"


def load_settings() -> Settings:
  data_dir = BASE_DIR / "data"
  data_dir.mkdir(exist_ok=True)

  return Settings(
      telegram_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
      telegram_admin_ids=_csv_to_list(os.getenv("TELEGRAM_ADMIN_IDS", "")),
      syncpay_auth_url=os.getenv("SYNCPAY_AUTH_URL", "https://syncpay.apidog.io/api/partner/v1/auth-token"),
      syncpay_cashin_url=os.getenv("SYNCPAY_CASHIN_URL", "https://syncpay.apidog.io/api/partner/v1/pix/cashin"),
      syncpay_transaction_url=os.getenv("SYNCPAY_TRANSACTION_URL", "https://syncpay.apidog.io/api/partner/v1/transactions"),
      syncpay_client_id=os.getenv("SYNCPAY_CLIENT_ID", ""),
      syncpay_client_secret=os.getenv("SYNCPAY_CLIENT_SECRET", ""),
      pushinpay_api_key=os.getenv("PUSHINPAY_API_KEY", ""),
      pushinpay_base_url=os.getenv("PUSHINPAY_BASE_URL", "https://api.pushinpay.com.br/api"),
      web_base_url=os.getenv("WEB_BASE_URL", "https://example.com"),
      secret_access_url=os.getenv("SECRET_ACCESS_URL", "https://example.com/secret"),
      admin_api_token=os.getenv("ADMIN_API_TOKEN", ""),
      allowed_origins=[origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",") if origin.strip()],
      data_dir=data_dir,
  )


settings = load_settings()

