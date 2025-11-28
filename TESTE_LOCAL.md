# 🧪 Como Testar a Loja Localmente

## ✅ Você pode testar TUDO no seu PC sem precisar do GitHub!

---

## 📋 Passo a Passo para Testar

### 1️⃣ Configure o Bot (Primeira vez)

```powershell
cd bot
```

Crie um arquivo `.env` na pasta `bot` com suas credenciais:

```env
TELEGRAM_BOT_TOKEN=seu_token_aqui
TELEGRAM_ADMIN_IDS=seu_id_telegram
SYNCPAY_CLIENT_ID=seu_client_id
SYNCPAY_CLIENT_SECRET=seu_client_secret
SYNCPAY_AUTH_URL=https://syncpay.apidog.io/api/partner/v1/auth-token
SYNCPAY_CASHIN_URL=https://syncpay.apidog.io/api/partner/v1/pix/cashin
SYNCPAY_TRANSACTION_URL=https://syncpay.apidog.io/api/partner/v1/transactions
WEB_BASE_URL=http://localhost:3000
SECRET_ACCESS_URL=https://example.com/secret
ADMIN_API_TOKEN=seu_token_admin
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 2️⃣ Instale as Dependências (Só uma vez)

```powershell
pip install -r requirements.txt
```

### 3️⃣ Inicie o Bot e a API

```powershell
python bot.py
```

**Isso inicia:**
- ✅ Bot do Telegram (comandos admin)
- ✅ API na porta 8080 (para o site se conectar)

**Mantenha este terminal aberto!**

### 4️⃣ Abra o Site Localmente

**Opção A: Servidor HTTP simples (Recomendado)**

Abra um **NOVO terminal** (PowerShell) e execute:

```powershell
cd C:\Users\vini\Desktop\site
python -m http.server 3000
```

Depois acesse no navegador:
```
http://localhost:3000
```

**Opção B: Abrir direto (pode ter problemas de CORS)**

Se tentar abrir o `index.html` direto, pode dar erro de CORS. Use a Opção A!

---

## 🧪 Testando o Sistema Completo

### Teste 1: Adicionar Produto via Bot

1. Abra o Telegram
2. Envie `/addproduct` para o bot
3. Siga o fluxo:
   - Envie imagem ou digite "pular"
   - Envie o título: `Produto Teste`
   - Envie o preço: `29.90`
   - Envie a descrição: `Descrição do produto teste`
   - Envie o link: `https://t.me/+teste123`

4. ✅ Produto criado! Verifique no site

### Teste 2: Ver Produtos no Site

1. Abra `http://localhost:3000` no navegador
2. Os produtos devem aparecer automaticamente
3. Se não aparecer, verifique:
   - Bot está rodando? (terminal aberto)
   - API está na porta 8080?
   - Abra o console do navegador (F12) para ver erros

### Teste 3: Gerar PIX

1. No site, clique em "Gerar Pix" em um produto
2. Deve aparecer:
   - Código PIX (copia e cola)
   - QR Code
   - Status "Aguardando pagamento"

### Teste 4: Simular Pagamento (Teste)

**Para testar sem pagar de verdade:**

1. Gere um PIX no site
2. Anote o `payment_id` (aparece na URL ou console)
3. No terminal do bot, você pode editar manualmente o status em `bot/data/payments.json`:
   ```json
   {
     "produto-teste-abc123": {
       "status": "paid",
       ...
     }
   }
   ```
4. Recarregue a página do site
5. O link deve aparecer automaticamente!

---

## 🔍 Verificando se Está Funcionando

### ✅ Checklist

- [ ] Bot está rodando? (terminal mostra "Bot iniciado!")
- [ ] API está ativa? Acesse: `http://localhost:8080/health`
- [ ] Site está rodando? `http://localhost:3000`
- [ ] Produtos aparecem no site?
- [ ] PIX é gerado quando clica em "Gerar Pix"?

### 🐛 Problemas Comuns

**Erro: "Erro ao conectar com a API"**
- ✅ Verifique se o bot está rodando
- ✅ Acesse `http://localhost:8080/health` no navegador
- ✅ Deve retornar: `{"status":"ok"}`

**Produtos não aparecem**
- ✅ Adicione um produto via `/addproduct` no Telegram
- ✅ Verifique `bot/data/products.json` (deve ter produtos)
- ✅ Abra o console do navegador (F12) e veja os erros

**CORS Error**
- ✅ Use `python -m http.server 3000` (não abra HTML direto)
- ✅ Verifique `ALLOWED_ORIGINS` no `.env`

---

## 📝 Resumo Rápido

```powershell
# Terminal 1: Bot e API
cd bot
python bot.py

# Terminal 2: Site
cd C:\Users\vini\Desktop\site
python -m http.server 3000

# Navegador
http://localhost:3000
```

**Pronto! Tudo funcionando localmente! 🎉**

---

## 💡 Dica

Você **NÃO precisa** do GitHub para testar! Só precisa quando quiser colocar online para outras pessoas acessarem.

Para testar localmente, basta:
1. Bot rodando (porta 8080)
2. Site rodando (porta 3000)
3. Tudo no mesmo PC!
