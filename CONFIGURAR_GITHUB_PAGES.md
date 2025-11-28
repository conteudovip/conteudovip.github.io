# 📋 Como Configurar para GitHub Pages (Sem API)

## ✅ Sistema Funcionando 100% via Bot do Telegram!

Agora o sistema funciona **sem precisar de API pública**. Tudo é feito via bot do Telegram!

## 🔧 Configuração

### 1. Configure o username do bot no `index.html`

Após iniciar o bot, ele detectará automaticamente o username. Você precisa adicionar no `index.html`:

```html
<script>
  window.__TELEGRAM_BOT_USERNAME__ = "SEU_BOT_USERNAME_AQUI"; // Ex: "meubot_bot"
  window.__USE_TELEGRAM_BOT__ = true; // Ativa modo bot-only
</script>
```

**Como descobrir o username do bot:**
1. Inicie o bot: `python bot/bot.py`
2. O bot mostrará no log: `Bot username detectado: @seu_bot`
3. Copie o username (sem o @) e cole no `index.html`

### 2. Gere o arquivo `products.json`

Execute sempre que adicionar/remover produtos:

```bash
python gerar-produtos-json.py
```

**OU** o bot gera automaticamente quando você adiciona um produto via `/addproduct`!

### 3. Faça deploy no GitHub Pages

1. Commit todos os arquivos:
   ```bash
   git add .
   git commit -m "Configurado para GitHub Pages"
   git push
   ```

2. No GitHub, vá em Settings > Pages e ative o GitHub Pages

## 🎯 Como Funciona

1. **Cliente acessa o site** no GitHub Pages
2. **Site carrega produtos** do arquivo `products.json` (estático)
3. **Cliente clica em "Gerar Pix"**
4. **Cliente é redirecionado** para o bot do Telegram: `https://t.me/SEU_BOT?start=pix-PRODUTO_ID`
5. **Bot gera o PIX** e envia para o cliente no Telegram
6. **Cliente paga** via PIX
7. **Bot detecta pagamento** e envia o link automaticamente

## ✅ Vantagens

- ✅ **Sem necessidade de API pública** (sem VPS, sem servidor)
- ✅ **Funciona 100% no GitHub Pages** (grátis!)
- ✅ **Bot gerencia tudo** (produtos, pagamentos, links)
- ✅ **Seguro** (comunicação direta com o bot)

## 🔄 Atualizar Produtos

Sempre que adicionar/remover produtos:

1. Use `/addproduct` ou `/delproduct` no bot
2. O bot gera automaticamente o `products.json`
3. Faça commit e push:
   ```bash
   git add products.json
   git commit -m "Atualizado produtos"
   git push
   ```

Pronto! O site será atualizado automaticamente no GitHub Pages.

