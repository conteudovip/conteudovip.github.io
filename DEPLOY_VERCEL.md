# 🚀 Deploy no Vercel + VPS

## ✅ Arquitetura

- **Frontend**: Vercel (hospedagem gratuita, CDN global)
- **Backend**: VPS (Bot Telegram + API FastAPI)

---

## 📋 Passo a Passo Completo

### 1️⃣ Preparar o Frontend

#### A. Configurar URL da API da VPS

Edite `index.html` e configure a URL da sua VPS:

```html
<script>
  // No código, procure por:
  window.__API_BASE_URL__ = "https://sua-vps.com:8080";
  // OU se usar domínio próprio:
  // window.__API_BASE_URL__ = "https://api.seusite.com";
</script>
```

**O código já detecta automaticamente se está no Vercel e usa a API da VPS!**

#### B. Criar arquivos de configuração do Vercel

Os arquivos `vercel.json` e `package.json` já foram criados. Eles configuram:
- ✅ Deploy estático (HTML, CSS, JS)
- ✅ Headers CORS corretos
- ✅ Rotas para SPA

---

### 2️⃣ Deploy no Vercel

#### Opção A: Via Vercel CLI (Recomendado)

```bash
# 1. Instale o Vercel CLI
npm i -g vercel

# 2. Faça login
vercel login

# 3. Deploy
vercel

# 4. Para produção
vercel --prod
```

#### Opção B: Via GitHub (Recomendado para CI/CD)

1. **Conecte seu repositório no Vercel:**
   - Acesse: https://vercel.com
   - Clique em "New Project"
   - Conecte seu repositório do GitHub
   - Selecione o repositório

2. **Configure o projeto:**
   - Framework Preset: **Other**
   - Build Command: (deixe vazio ou `echo 'No build'`)
   - Output Directory: `.` (raiz)
   - Install Command: (deixe vazio)

3. **Deploy:**
   - Clique em "Deploy"
   - Aguarde o deploy (alguns segundos)
   - Seu site estará em: `https://seu-projeto.vercel.app`

4. **Configurar domínio customizado (opcional):**
   - Vá em Settings → Domains
   - Adicione seu domínio
   - Configure DNS conforme instruções

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

# Clonar ou fazer upload do código
# (faça upload da pasta bot/)
cd bot
pip install -r requirements.txt
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
TELEGRAM_BOT_USERNAME=seu_bot

# PushinPay
PUSHINPAY_API_KEY=sua_chave_aqui
PUSHINPAY_BASE_URL=https://api.pushinpay.com.br/api

# Web
WEB_BASE_URL=https://seu-projeto.vercel.app
SECRET_ACCESS_URL=https://t.me/+acesso
ADMIN_API_TOKEN=seu_token_secreto_aqui

# CORS - IMPORTANTE: adicione a URL do Vercel
ALLOWED_ORIGINS=https://seu-projeto.vercel.app,https://seu-dominio.com
```

**⚠️ IMPORTANTE:** Adicione a URL do Vercel em `ALLOWED_ORIGINS`!

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

### 4️⃣ Configurar Nginx com SSL (Recomendado)

Para usar HTTPS e domínio próprio:

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

Depois, atualize o `index.html` para usar `https://api.seusite.com`.

---

### 5️⃣ Atualizar Frontend com URL da VPS

Edite `index.html` e configure a URL da sua VPS:

```html
<script>
  // Se usar domínio próprio:
  window.__API_BASE_URL__ = "https://api.seusite.com";
  // OU diretamente:
  // window.__API_BASE_URL__ = "https://sua-vps.com:8080";
</script>
```

**O código já detecta automaticamente se está no Vercel!** Mas você precisa configurar a URL da VPS.

Faça commit e push:

```bash
git add index.html
git commit -m "Configurar URL da API da VPS"
git push
```

O Vercel fará deploy automaticamente!

---

## ✅ Checklist Final

- [ ] Frontend no Vercel funcionando
- [ ] `vercel.json` e `package.json` criados
- [ ] `window.__API_BASE_URL__` configurado no `index.html`
- [ ] VPS com Python e dependências instaladas
- [ ] `.env` configurado na VPS com `ALLOWED_ORIGINS` incluindo URL do Vercel
- [ ] Porta 8080 aberta no firewall
- [ ] Bot + API rodando na VPS
- [ ] CORS configurado para permitir Vercel
- [ ] Testado: site no Vercel acessa API da VPS

---

## 🧪 Teste

1. Acesse seu site no Vercel
2. Abra o console (F12)
3. Verifique se os produtos aparecem
4. Tente gerar um PIX
5. Verifique os logs na VPS

---

## 🐛 Troubleshooting

### CORS Error

- Verifique se `ALLOWED_ORIGINS` no `.env` da VPS inclui a URL do Vercel
- Verifique se a URL está correta (com/sem `https://`)
- Verifique se não há espaços extras na lista

### API não responde

- Verifique se o bot está rodando na VPS: `sudo systemctl status telegram-secrets`
- Verifique se a porta 8080 está aberta: `sudo ufw status`
- Teste a API diretamente: `curl http://sua-vps.com:8080/health`

### Frontend não carrega produtos

- Abra o console (F12) e veja os erros
- Verifique se `window.__API_BASE_URL__` está configurado corretamente
- Verifique se a URL da API está acessível

---

## 🔄 Atualizar Frontend

Sempre que fizer alterações:

```bash
git add .
git commit -m "Atualização"
git push
```

O Vercel fará deploy automaticamente!

---

## 📊 Vantagens do Vercel

- ✅ **CDN Global**: Site rápido em qualquer lugar
- ✅ **HTTPS Automático**: SSL gratuito
- ✅ **Deploy Automático**: Push no Git = deploy
- ✅ **Gratuito**: Plano free generoso
- ✅ **Domínio Customizado**: Fácil de configurar

