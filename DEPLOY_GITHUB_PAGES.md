# 🚀 Deploy no GitHub Pages + VPS

## ✅ Sim, funciona no GitHub Pages!

O GitHub Pages serve apenas arquivos estáticos (HTML, CSS, JS), então:
- ✅ **Frontend (site)**: GitHub Pages
- ✅ **Backend (API + Bot)**: VPS

---

## 📋 Passo a Passo Completo

### 1️⃣ Preparar o Frontend para GitHub Pages

#### A. Configurar URL da API

Edite `index.html` e todas as páginas de produto para apontar para sua VPS:

```html
<script>
  // Substitua pela URL da sua VPS
  window.__API_BASE_URL__ = "https://sua-vps.com:8080";
  // OU se usar domínio próprio:
  // window.__API_BASE_URL__ = "https://api.seusite.com";
</script>
```

#### B. Criar arquivo `.nojekyll` (importante!)

Crie um arquivo `.nojekyll` na raiz do projeto:

```bash
# Windows
echo. > .nojekyll

# Linux/Mac
touch .nojekyll
```

Isso garante que o GitHub Pages não processe os arquivos como Jekyll.

---

### 2️⃣ Fazer Deploy no GitHub Pages

#### Opção A: Via GitHub Web Interface

1. Crie um repositório no GitHub (ex: `meu-site-vips`)
2. Faça upload dos arquivos do frontend:
   - `index.html`
   - `produto.html` (template)
   - `produto-*.html` (páginas geradas)
   - `styles.css`
   - `assets/` (pasta completa)
   - `.nojekyll`
3. Vá em **Settings → Pages**
4. Selecione a branch `main` (ou `master`)
5. Salve
6. Seu site estará em: `https://seu-usuario.github.io/meu-site-vips/`

#### Opção B: Via Git (recomendado)

```bash
# 1. Inicialize git (se ainda não fez)
git init
git add .
git commit -m "Deploy inicial"

# 2. Crie repositório no GitHub e conecte
git remote add origin https://github.com/seu-usuario/meu-site-vips.git
git branch -M main
git push -u origin main

# 3. Configure GitHub Pages
# Vá em: Settings → Pages → Source: main branch
```

---

### 3️⃣ Configurar VPS para Bot + API

#### A. Conectar na VPS

```bash
ssh usuario@sua-vps.com
```

#### B. Instalar Python e dependências

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# Criar ambiente virtual
cd ~
mkdir telegram-secrets
cd telegram-secrets
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r bot/requirements.txt
```

#### C. Configurar `.env`

```bash
cd bot
nano .env
```

Conteúdo do `.env`:

```env
# Telegram
TELEGRAM_BOT_TOKEN=seu_token_aqui
TELEGRAM_ADMIN_IDS=123456789

# PushinPay
PUSHINPAY_API_KEY=55678|wHO1Ac5gTxKWLRZHR9QF71gISLLubooh8viZXNe18a290bbe
PUSHINPAY_BASE_URL=https://api.pushinpay.com.br/api

# Web
WEB_BASE_URL=https://seu-usuario.github.io/meu-site-vips
SECRET_ACCESS_URL=https://t.me/+acesso
ADMIN_API_TOKEN=seu_token_secreto_aqui

# CORS - IMPORTANTE: adicione a URL do GitHub Pages
ALLOWED_ORIGINS=https://seu-usuario.github.io
```

#### D. Configurar Firewall

```bash
# Permitir porta 8080
sudo ufw allow 8080/tcp
sudo ufw reload
```

#### E. Rodar Bot + API

**Opção 1: Direto (para teste)**

```bash
cd ~/telegram-secrets
source venv/bin/activate
cd bot
python bot.py
```

**Opção 2: Com systemd (recomendado para produção)**

Crie `/etc/systemd/system/telegram-secrets.service`:

```ini
[Unit]
Description=Telegram Secrets Bot + API
After=network.target

[Service]
Type=simple
User=seu-usuario
WorkingDirectory=/home/seu-usuario/telegram-secrets/bot
Environment="PATH=/home/seu-usuario/telegram-secrets/venv/bin"
ExecStart=/home/seu-usuario/telegram-secrets/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ative o serviço:

```bash
sudo systemctl enable telegram-secrets
sudo systemctl start telegram-secrets
sudo systemctl status telegram-secrets
```

---

### 4️⃣ Configurar Nginx (Opcional mas Recomendado)

Se quiser usar domínio próprio e HTTPS:

```nginx
# /etc/nginx/sites-available/telegram-secrets
server {
    listen 80;
    server_name api.seusite.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Ative:

```bash
sudo ln -s /etc/nginx/sites-available/telegram-secrets /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Configure SSL com Let's Encrypt:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.seusite.com
```

---

### 5️⃣ Atualizar Frontend com URL da VPS

Depois de configurar a VPS, atualize o `index.html`:

```html
<script>
  // URL da sua VPS (com ou sem domínio)
  window.__API_BASE_URL__ = "https://api.seusite.com";
  // OU diretamente:
  // window.__API_BASE_URL__ = "https://sua-vps.com:8080";
</script>
```

Faça commit e push:

```bash
git add index.html
git commit -m "Atualizar URL da API"
git push
```

---

## 🔧 Script Unificado para VPS

Crie `start.sh` na VPS:

```bash
#!/bin/bash
cd ~/telegram-secrets
source venv/bin/activate
cd bot
python bot.py
```

Torne executável:

```bash
chmod +x start.sh
```

Execute:

```bash
./start.sh
```

---

## ✅ Checklist Final

- [ ] Frontend no GitHub Pages funcionando
- [ ] `.nojekyll` criado na raiz
- [ ] `window.__API_BASE_URL__` apontando para VPS
- [ ] VPS com Python e dependências instaladas
- [ ] `.env` configurado na VPS
- [ ] Porta 8080 aberta no firewall
- [ ] Bot + API rodando na VPS
- [ ] CORS configurado para permitir GitHub Pages
- [ ] Testado: site acessa API da VPS

---

## 🧪 Teste

1. Acesse seu site no GitHub Pages
2. Abra o console (F12)
3. Verifique se os produtos aparecem
4. Tente gerar um PIX
5. Verifique os logs na VPS

---

## 🐛 Troubleshooting

### CORS Error
- Verifique se `ALLOWED_ORIGINS` no `.env` inclui a URL do GitHub Pages
- Verifique se a URL está exata (com/sem `https://`, com/sem barra final)

### API não responde
- Verifique se o bot está rodando: `sudo systemctl status telegram-secrets`
- Verifique os logs: `sudo journalctl -u telegram-secrets -f`
- Teste a API diretamente: `curl https://sua-vps.com:8080/health`

### Produtos não aparecem
- Verifique se há produtos: `curl https://sua-vps.com:8080/products`
- Verifique o console do navegador (F12)

---

## 📞 Suporte

Se tiver problemas, verifique:
1. Logs do bot na VPS
2. Console do navegador (F12)
3. Network tab (F12 → Network) para ver requisições
