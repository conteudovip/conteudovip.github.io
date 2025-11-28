# 🔍 Diagnóstico Rápido - API Não Conecta

## ✅ Você já tem:
- ✅ Produtos cadastrados
- ✅ 2 terminais rodando (bot + site)

## 🧪 Teste Rápido em 3 Passos

### 1️⃣ Teste a API Diretamente no Navegador

Abra estes links e veja o que aparece:

**Teste 1: Health Check**
```
http://localhost:8080/health
```
**Deve aparecer:** `{"status":"ok","time":"..."}`

**Teste 2: Produtos**
```
http://localhost:8080/products
```
**Deve aparecer:** Lista de produtos em JSON

---

### 2️⃣ Use a Página de Teste

1. Acesse: `http://localhost:3000/test-api.html`
2. Clique no botão "🔍 Testar API Agora"
3. Veja o resultado

**Se aparecer erro:**
- A API não está respondendo
- Verifique o terminal do bot

**Se aparecer sucesso:**
- A API está OK
- O problema pode ser no `index.html`

---

### 3️⃣ Verifique o Console do Navegador

1. Abra `http://localhost:3000`
2. Pressione **F12** (abre o console)
3. Vá na aba **Console**
4. Veja se há erros em vermelho

**Erros comuns:**
- `Failed to fetch` → API não está acessível
- `CORS error` → Problema de permissão
- `Network error` → API não está rodando

---

## 🔧 Soluções Rápidas

### Solução 1: Verificar se a API Iniciou

No terminal do bot, você deve ver:
```
INFO - Iniciando API na porta 8080...
INFO - API iniciada em thread separada. Aguardando inicialização...
INFO - 🤖 Bot iniciado! API rodando na porta 8080.
```

**Se não aparecer:**
- Reinicie o bot: `CTRL+C` e depois `python bot.py` novamente
- Aguarde 2-3 segundos após iniciar

### Solução 2: Verificar Porta 8080

A porta 8080 pode estar ocupada. Teste:

```powershell
netstat -ano | findstr :8080
```

**Se aparecer algo:**
- A porta está em uso
- Pode ser o bot (OK) ou outro programa (problema)

### Solução 3: Testar com curl (se tiver)

```powershell
curl http://localhost:8080/health
```

**Se funcionar:**
- API está OK
- Problema pode ser no navegador/CORS

**Se não funcionar:**
- API não está rodando
- Reinicie o bot

---

## 🐛 Problemas Específicos

### Problema: API responde no navegador, mas site não carrega

**Causa:** Problema no JavaScript do site

**Solução:**
1. Abra o console (F12)
2. Veja erros específicos
3. Verifique se `window.__API_BASE_URL__` está correto

### Problema: "Failed to fetch" mesmo com API rodando

**Causa:** Firewall/Antivírus bloqueando

**Solução:**
1. Desative temporariamente o firewall
2. Ou adicione exceção para porta 8080

### Problema: API funciona em `test-api.html` mas não no `index.html`

**Causa:** Problema no código JavaScript

**Solução:**
1. Compare os dois arquivos
2. Verifique se ambos usam a mesma URL da API
3. Verifique erros no console

---

## ✅ Checklist Final

- [ ] API responde em `http://localhost:8080/health`?
- [ ] API retorna produtos em `http://localhost:8080/products`?
- [ ] `test-api.html` funciona?
- [ ] Console do navegador mostra erros?
- [ ] Bot está rodando e mostra "API rodando na porta 8080"?
- [ ] Site está em `http://localhost:3000` (não `file://`)?

---

## 💡 Próximos Passos

**Se a API não responde:**
1. Reinicie o bot
2. Aguarde aparecer "API rodando"
3. Teste novamente

**Se a API responde mas o site não carrega:**
1. Abra o console (F12)
2. Me mostre os erros
3. Verifique se está usando servidor HTTP (não file://)

---

**Me diga:**
1. O que aparece em `http://localhost:8080/health`?
2. O que aparece em `http://localhost:8080/products`?
3. O que aparece no console do navegador (F12)?

Com essas informações, consigo ajudar melhor! 🚀

