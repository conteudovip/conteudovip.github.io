# Backend Telegram + API Pix

Este diretório concentra tudo que roda na VPS:

1. **Bot do Telegram (`bot.py`)**: painel administrativo para listar produtos, criar/remover itens, gerar Pix manualmente e receber estatísticas.
2. **API FastAPI (`api.py`)**: alimenta o site (lista produtos, gera Pix para os clientes, consulta pagamentos e recebe webhooks).
3. **Camada SyncPay (`syncpay.py`)**: gera/renova tokens automaticamente e cria/consulta cobranças Pix.
4. **Armazenamento (`storage.py`)**: salva produtos e pagamentos em `bot/data/*.json`.

O front (GitHub Pages) fala somente com a API; as chaves do gateway ficam na VPS.

## Pré-requisitos

- Python 3.11+
- Acesso a uma VPS (para manter bot + API rodando)
- Credenciais do Telegram (BotFather)
- Credenciais SyncPay (`client_id` e `client_secret`)

## Configuração

1. Dentro da pasta `bot/`, crie o `.env`:

```bash
cd bot
cp env.example .env
```

Preencha:

| Variável | Descrição |
|----------|-----------|
| `TELEGRAM_BOT_TOKEN` | Token do bot (BotFather). |
| `TELEGRAM_ADMIN_IDS` | IDs numéricos autorizados a gerenciar tudo (separados por vírgula). |
| `SYNCPAY_*` | URLs e credenciais oficiais do gateway. |
| `WEB_BASE_URL` | Domínio público do site (usado em links de status). |
| `SECRET_ACCESS_URL` | Link padrão liberado após pagamento (cada produto pode sobrescrever). |
| `ADMIN_API_TOKEN` | Chave para usar `POST /products` e `DELETE /products`. |
| `ALLOWED_ORIGINS` | Domínios permitidos a consumir a API (ex.: `https://seusite.com`). |

2. Instale dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Executando

### Tudo em um único comando! 🚀

O bot agora inicia **automaticamente** tanto o Telegram quanto a API:

```bash
python bot.py
# ou, para manter em background:
nohup python bot.py > bot.log 2>&1 &
```

**Isso é tudo que você precisa!** Ao iniciar o bot:
- ✅ Bot do Telegram fica ativo (comandos admin)
- ✅ API HTTP inicia automaticamente na porta 8080
- ✅ Site pode se conectar e buscar produtos
- ✅ Pagamentos Pix funcionam normalmente

### Comandos do Telegram

| Comando | Descrição |
|---------|-----------|
| `/start` ou `/help` | Mostra ajuda rápida. |
| `/produtos` | Lista catálogo atual. |
| `/addproduct` | Adiciona produto interativo (envia imagem, depois dados). |
| `/delproduct <id>` | Remove um produto (admins). |
| `/stats` | Mostra resumo (produtos, pendentes, pagos, receita). |
| `/pix <produto_id>` | Gera Pix manual e monitora até confirmar, enviando o link VIP. |

### API automática

A API inicia automaticamente na porta **8080** junto com o bot. Não é necessário rodar separadamente!

**Endpoints disponíveis:**

| Método | Rota | Uso |
|--------|------|-----|
| GET | `/health` | Status. |
| GET | `/products` | Lista catálogo (usado pelo site). |
| POST | `/products` | Cria/atualiza produto (requer `X-Admin-Token`). |
| DELETE | `/products/{id}` | Remove produto (requer `X-Admin-Token`). |
| POST | `/checkout` | Gera Pix (retorna `payment_id`, copia e cola e QR base64). |
| GET | `/payments/{id}` | Retorna status; quando `paid`, inclui `secret_link`. |
| POST | `/webhooks/syncpay` | Endpoint para webhook oficial da SyncPay. |

Há um monitor interno que consulta a SyncPay a cada 25 s, garantindo atualização mesmo se o webhook falhar.

## Integração com o site

1. No `index.html`, defina `window.__API_BASE_URL__ = "https://sua-vps/api";`.
2. `assets/products.js` busca `GET /products` para montar os cards.
3. Ao clicar em “Gerar Pix”, o site chama `POST /checkout`, mostra o QR/copia-e-cola e fica consultando `GET /payments/{payment_id}`. Quando a API retorna `status: "paid"`, o link secreto é exibido imediatamente.

## Produtos e pagamentos

- `data/products.json`: catálogo (edite manualmente ou via comandos/API).
- `data/payments.json`: histórico de cobranças. Faça backup periódico ou migre para um banco se precisar de mais robustez.

## Observações

- Nunca commite `.env` com credenciais reais.
- Configure HTTPS (Nginx/Caddy/Cloudflare) para expor a API/publicar webhooks.
- Garanta que `ALLOWED_ORIGINS` contenha apenas os domínios do seu site em produção.

