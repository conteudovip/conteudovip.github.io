# 🔧 Solução: Erro "Failed to fetch" - API não conecta

## ❌ Erro que você está vendo:
```
Erro ao carregar produtos!
Erro ao conectar com a API: Failed to fetch
Verifique se o bot está rodando e acesse: http://localhost:8080/products
```

---

## ✅ Solução Passo a Passo

### 1️⃣ Verifique se o Bot está Rodando

O erro acontece porque a **API não está rodando**. O bot precisa estar ativo!

**Verifique:**
- Você executou `iniciar.bat` ou `python bot.py`?
- O terminal do bot está aberto?
- Apareceu a mensagem "Bot iniciado!" ou "API iniciada"?

### 2️⃣ Inicie o Bot (se não estiver rodando)

**Opção A: Script automático**
```cmd
iniciar.bat
```

**Opção B: Comando direto**
```powershell
cd bot
python bot.py
```

**Aguarde aparecer:**
```
🤖 Bot iniciado! API rodando na porta 8080.
✅ Tudo funcionando! Use /start no Telegram para começar.
```

### 3️⃣ Teste se a API está Respondendo

Abra no navegador:
```
http://localhost:8080/health
```

**Deve aparecer:**
```json
{"status":"ok","time":"2024-..."}
```

**Se aparecer erro:**
- O bot não está rodando
- A porta 8080 está ocupada
- Algo deu errado na inicialização

### 4️⃣ Teste o Endpoint de Produtos

Abra no navegador:
```
http://localhost:8080/products
```

**Deve aparecer:**
```json
[
  {
    "product_id": "...",
    "title": "...",
    ...
  }
]
```

**Se aparecer `[]` (vazio):**
- API está funcionando, mas não há produtos
- Adicione produtos via Telegram: `/addproduct`

### 5️⃣ Recarregue o Site

Depois que a API estiver respondendo:
1. Volte para `http://localhost:3000`
2. Pressione **F5** (ou CTRL+R) para recarregar
3. Os produtos devem aparecer!

---

## 🔍 Verificação Rápida

Execute o script de verificação:
```cmd
verificar-api.bat
```

Ou teste manualmente:
```powershell
# Teste 1: Health check
curl http://localhost:8080/health

# Teste 2: Listar produtos
curl http://localhost:8080/products
```

---

## 🐛 Problemas Comuns

### Problema 1: "Porta 8080 já está em uso"
**Solução:**
- Feche outros programas usando a porta 8080
- Ou mude a porta no `bot/bot.py` (linha 437)

### Problema 2: Bot inicia mas API não funciona
**Solução:**
- Verifique se apareceu "API iniciada em thread separada"
- Aguarde 2-3 segundos após iniciar
- Teste: `http://localhost:8080/health`

### Problema 3: Site não conecta mesmo com API rodando
**Solução:**
- Verifique se o site está em `http://localhost:3000` (não `file://`)
- Use: `python -m http.server 3000` para servir o site
- Verifique o console do navegador (F12) para erros de CORS

---

## ✅ Checklist Final

- [ ] Bot está rodando? (terminal aberto com "Bot iniciado!")
- [ ] API responde? (`http://localhost:8080/health` retorna OK)
- [ ] Produtos existem? (`http://localhost:8080/products` retorna lista)
- [ ] Site está em `http://localhost:3000`? (não `file://`)
- [ ] Recarregou a página? (F5)

---

## 💡 Dica

**Sempre mantenha 2 terminais abertos:**

**Terminal 1:** Bot + API
```cmd
iniciar.bat
```

**Terminal 2:** Site
```cmd
python -m http.server 3000
```

**Navegador:** `http://localhost:3000`

---

Se ainda não funcionar, me mostre:
1. O que aparece no terminal do bot
2. O que aparece em `http://localhost:8080/health`
3. Erros no console do navegador (F12)

