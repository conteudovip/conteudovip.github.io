# ✅ Configuração PushinPay - COMPLETA

## 🎯 Sistema Totalmente Ajustado para PushinPay

O sistema foi **completamente ajustado** para usar a API oficial do PushinPay conforme a documentação:
- **Documentação**: https://app.theneo.io/pushinpay/pix/pix/criar-pix
- **Endpoint**: `/pix/cashIn`
- **Base URL**: `https://api.pushinpay.com.br/api`

---

## 📝 Configuração Obrigatória

### 1. Criar arquivo `bot/.env`

Crie o arquivo `bot/.env` com o seguinte conteúdo:

```env
# PushinPay - OBRIGATÓRIO
PUSHINPAY_API_KEY=55678|wHO1Ac5gTxKWLRZHR9QF71gISLLubooh8viZXNe18a290bbe
PUSHINPAY_BASE_URL=https://api.pushinpay.com.br/api

# Telegram Bot (se ainda não configurado)
TELEGRAM_BOT_TOKEN=seu_token_telegram
TELEGRAM_ADMIN_IDS=123456789

# Web
WEB_BASE_URL=http://localhost:3000
SECRET_ACCESS_URL=https://example.com/secret
ADMIN_API_TOKEN=seu_token_admin
```

### 2. Reiniciar a API

Após criar o arquivo `.env`, **reinicie a API**:

```bash
# Windows
iniciar.bat

# Ou manualmente
python bot/api.py
```

---

## 🔍 Verificação

Para verificar se está configurado corretamente:

```bash
cd bot
python -c "from config import settings; print('PUSHINPAY_API_KEY:', 'OK ✅' if settings.pushinpay_api_key else 'FALTANDO ❌'); print('PUSHINPAY_BASE_URL:', settings.pushinpay_base_url)"
```

---

## 📚 Especificações Técnicas

### Endpoint
- **URL**: `POST https://api.pushinpay.com.br/api/pix/cashIn`
- **Headers**:
  - `Authorization: Bearer {TOKEN}`
  - `Accept: application/json`
  - `Content-Type: application/json`

### Request Body
```json
{
  "value": 100,  // Valor em centavos (mínimo 50)
  "webhook_url": "https://seu-webhook.com"  // Opcional
}
```

### Response
```json
{
  "id": "9c29870c-9f69-4bb6-90d3-2dce9453bb45",
  "qr_code": "00020101021226770014BR.GOV.BCB.PIX...",
  "status": "created",
  "value": 100,
  "qr_code_base64": "data:image/png;base64,iVBORw0KGgo...",
  "webhook_url": "https://seu-webhook.com",
  "end_to_end_id": null,
  "payer_name": null,
  "payer_national_registration": null
}
```

### Status Possíveis
- `created`: PIX criado, aguardando pagamento
- `paid`: PIX pago
- `canceled`: PIX cancelado/expirado

---

## ✅ O que foi ajustado

1. ✅ **Endpoint correto**: `/pix/cashIn` (não `/pix/criar-pix`)
2. ✅ **Headers corretos**: `Authorization: Bearer`, `Accept`, `Content-Type`
3. ✅ **Payload correto**: Apenas `value` (em centavos)
4. ✅ **Mapeamento de resposta**: `qr_code`, `id`, `qr_code_base64`
5. ✅ **Validação**: Valor mínimo de 50 centavos
6. ✅ **Logs detalhados**: Para debug
7. ✅ **Tratamento de erros**: Mensagens claras

---

## 🧪 Teste

1. Crie o arquivo `.env` com o token
2. Reinicie a API
3. Acesse: `http://localhost:3000/produto-vip-pro.html`
4. Clique em "Gerar Código Pix"
5. Verifique os logs no console do navegador (F12)

---

## 🐛 Troubleshooting

### Erro 401 (Unauthorized)
- Verifique se o token está correto no `.env`
- Token deve estar no formato: `55678|wHO1Ac5gTxKWLRZHR9QF71gISLLubooh8viZXNe18a290bbe`

### Erro 422 (Valor mínimo)
- Valor mínimo é R$ 0,50 (50 centavos)
- Verifique se o produto tem valor >= 0.50

### Erro 404 (Not Found)
- Verifique se a URL base está correta: `https://api.pushinpay.com.br/api`
- Endpoint deve ser: `/pix/cashIn`

---

## 📞 Suporte

- **Documentação**: https://app.theneo.io/pushinpay/pix/pix/criar-pix
- **Token fornecido**: `55678|wHO1Ac5gTxKWLRZHR9QF71gISLLubooh8viZXNe18a290bbe`
