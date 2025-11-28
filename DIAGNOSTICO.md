# 🔍 Diagnóstico - Produtos Não Aparecem

## ⚡ Teste Rápido em 3 Passos

### Passo 1: Verifique se o bot está rodando

No terminal, você deve ter rodado:
```bash
cd bot
python bot.py
```

Você deve ver estas mensagens:
```
INFO - Iniciando API na porta 8080...
INFO - API iniciada em thread separada. Aguardando inicialização...
INFO - 🤖 Bot iniciado! API rodando na porta 8080.
```

**Se não estiver rodando:**
- Execute `python bot.py` na pasta `bot/`

---

### Passo 2: Teste a API diretamente

Abra no navegador:
```
http://localhost:8080/products
```

**Resultado esperado:**
- ✅ Você deve ver um JSON com produtos: `[{...}, {...}]`
- ✅ Ou um array vazio: `[]` (se não houver produtos)

**Se der erro:**
- ❌ "Connection refused" → O bot não está rodando
- ❌ Página não carrega → A API não iniciou

---

### Passo 3: Teste com a página de diagnóstico

1. Abra o arquivo `test-api.html` no navegador
   - **IMPORTANTE:** Use um servidor HTTP, não abra direto (file://)
   
2. Para usar servidor HTTP:
   ```bash
   python -m http.server 3000
   ```
   Depois acesse: `http://localhost:3000/test-api.html`

3. Clique no botão "Testar API Agora"

**Você verá:**
- ✅ Sucesso e lista de produtos
- ❌ Erro com detalhes do problema

---

## 🐛 Problemas Comuns e Soluções

### Problema 1: "Connection refused" ou página não carrega

**Causa:** A API não está rodando

**Solução:**
1. Certifique-se de que o bot está rodando
2. Verifique se a porta 8080 está livre
3. Reinicie o bot: `python bot.py`

---

### Problema 2: API retorna `[]` (vazio)

**Causa:** Não há produtos cadastrados

**Solução:**
1. No Telegram, envie: `/produtos`
   - Se aparecer lista → Produtos existem
   - Se não aparecer nada → Não há produtos

2. Adicione um produto:
   ```
   /addproduct
   ```
   - Envie a imagem
   - Envie: `Título|Preço|Descrição|LinkSecreto`

---

### Problema 3: Site não carrega produtos (mas API funciona)

**Causa 1:** Abrindo HTML direto (file://)
- ❌ Não funciona: Clicar duplo no `index.html`
- ✅ Funciona: Usar servidor HTTP

**Solução:**
```bash
python -m http.server 3000
# Depois acesse: http://localhost:3000
```

**Causa 2:** URL da API errada

**Verifique no `index.html` (linha 19):**
```html
<script>
  window.__API_BASE_URL__ = "http://localhost:8080";
</script>
```

---

### Problema 4: Erro de CORS

**Causa:** Navegador bloqueando requisições

**Solução:**
- A API já está configurada para aceitar qualquer origem
- Se ainda der erro, verifique se o bot está rodando
- Use o servidor HTTP (não file://)

---

## ✅ Checklist Rápido

- [ ] Bot está rodando? (`python bot.py`)
- [ ] API responde? (http://localhost:8080/products)
- [ ] Há produtos cadastrados? (`/produtos` no Telegram)
- [ ] Está usando servidor HTTP? (não file://)
- [ ] URL da API está correta? (`http://localhost:8080`)

---

## 🚀 Teste Completo

1. **Inicie o bot:**
   ```bash
   cd bot
   python bot.py
   ```

2. **Teste a API:**
   - Acesse: http://localhost:8080/products
   - Deve mostrar JSON com produtos

3. **Inicie servidor HTTP:**
   ```bash
   python -m http.server 3000
   ```

4. **Acesse o site:**
   - http://localhost:3000 (ou http://localhost:3000/index.html)
   - Produtos devem aparecer!

5. **Se não aparecer:**
   - Abra o console (F12)
   - Veja as mensagens de erro
   - Teste com: http://localhost:3000/test-api.html

---

## 📞 Ainda Não Funciona?

Execute estes comandos e envie o resultado:

```bash
# 1. Verificar se há produtos no JSON
cat bot/data/products.json

# 2. Testar API com curl (se tiver)
curl http://localhost:8080/products

# 3. Verificar se o bot está rodando
# No terminal onde rodou python bot.py, veja as mensagens
```

**No navegador (F12 → Console):**
```javascript
fetch('http://localhost:8080/products')
  .then(r => r.json())
  .then(d => console.log('Produtos:', d))
  .catch(e => console.error('Erro:', e))
```

