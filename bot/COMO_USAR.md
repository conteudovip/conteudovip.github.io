# 🚀 Como Usar - Tudo em Um Só Comando!

## ✅ Agora é Super Simples!

Apenas **um comando** inicia tudo:
- 🤖 Bot do Telegram (comandos admin)
- 🌐 API HTTP para o site (porta 8080)
- 💳 Sistema de pagamento Pix
- 📦 Gerenciamento de produtos

---

## 📋 Passo a Passo

### 1. Configure o `.env`

```bash
cd bot
cp env.example .env
# Edite o .env com suas credenciais
```

### 2. Instale as dependências (só uma vez)

```bash
pip install -r requirements.txt
```

### 3. Inicie TUDO com um único comando

```bash
python bot.py
```

**Pronto!** Agora você tem:
- ✅ Bot Telegram funcionando
- ✅ API na porta 8080
- ✅ Site pode se conectar

---

## 💬 Comandos no Telegram

### `/start` ou `/help`
Mostra a ajuda com todos os comandos

### `/produtos`
Lista todos os produtos cadastrados

### `/addproduct`
Fluxo interativo para adicionar produto:
1. Bot pede a imagem (ou envie URL, ou digite "pular")
2. Bot pede as informações: `Título|Preço|Descrição|LinkSecreto`
3. Produto é criado e já aparece no site!

### `/delproduct <id>`
Remove um produto pelo ID

### `/stats`
Mostra estatísticas: produtos, pagamentos pendentes/confirmados, receita

### `/pix <produto_id>`
Gera um Pix para um produto e monitora até confirmar

---

## 🌐 Testando o Site

### Localmente

1. Com o bot rodando (porta 8080 ativa)
2. Abra o `index.html` no navegador
3. Ou use um servidor HTTP simples:
   ```bash
   python -m http.server 3000
   # Acesse: http://localhost:3000
   ```

### Em Produção (VPS)

1. Configure `WEB_BASE_URL` no `.env` para seu domínio
2. Configure `ALLOWED_ORIGINS` para permitir o domínio do site
3. No `index.html`, defina:
   ```html
   <script>
     window.__API_BASE_URL__ = "https://sua-vps:8080";
   </script>
   ```
4. Faça deploy do HTML no GitHub Pages
5. O bot já está rodando e a API já está disponível!

---

## 🔧 Rodando em Background (VPS)

Para manter rodando mesmo após fechar o terminal:

```bash
nohup python bot.py > bot.log 2>&1 &
```

Para ver os logs:
```bash
tail -f bot.log
```

Para parar:
```bash
pkill -f "python bot.py"
```

---

## ⚠️ Importante

- A API inicia automaticamente na porta **8080**
- Não precisa rodar `uvicorn` separadamente
- Tudo funciona apenas com `python bot.py`
- Os produtos ficam salvos em `bot/data/products.json`
- Os pagamentos ficam em `bot/data/payments.json`

---

## 🎉 Pronto!

Agora é só usar! Adicione produtos pelo Telegram e eles já aparecem no site automaticamente!

