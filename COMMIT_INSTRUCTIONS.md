# 📤 Instruções para Fazer Commit no GitHub

## ⚠️ Importante
O Git não está instalado no seu sistema ou não está no PATH. Você precisa instalar o Git primeiro.

## 🚀 Passo a Passo

### 1. Instale o Git (se ainda não tiver)
- Baixe em: https://git-scm.com/download/win
- Instale com as opções padrão

### 2. Configure o Git (primeira vez)
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@example.com"
```

### 3. Inicialize o repositório
```bash
cd C:\Users\vini\Desktop\site
git init
```

### 4. Adicione o remote do GitHub
```bash
git remote add origin git@github.com:conteudovip/conteudovip.github.io.git
```

### 5. Adicione todos os arquivos
```bash
git add .
```

### 6. Faça o commit
```bash
git commit -m "Initial commit - Site Telegram Secrets VIP"
```

### 7. Configure a branch main (se necessário)
```bash
git branch -M main
```

### 8. Faça o push usando o token
```bash
git push -u origin main
```

Quando pedir senha, use o token:
```
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
```

---

## 🔐 Alternativa: Usar HTTPS com Token

Se SSH não funcionar, use HTTPS:

### 1. Adicione o remote HTTPS
```bash
git remote set-url origin https://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@github.com/conteudovip/conteudovip.github.io.git
```

### 2. Faça o push
```bash
git push -u origin main
```

---

## 📝 Script Automático (Windows PowerShell)

Crie um arquivo `fazer-commit.ps1` com este conteúdo:

```powershell
# Inicializar repositório
git init
git remote add origin https://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@github.com/conteudovip/conteudovip.github.io.git

# Adicionar arquivos
git add .

# Commit
git commit -m "Initial commit - Site Telegram Secrets VIP"

# Push
git branch -M main
git push -u origin main
```

Execute com:
```powershell
powershell -ExecutionPolicy Bypass -File fazer-commit.ps1
```

---

## ⚠️ Segurança

**NUNCA faça commit do arquivo `bot/.env`** (já está no .gitignore)

O token de acesso está visível neste arquivo. Após fazer o commit, considere:
1. Revogar este token no GitHub
2. Criar um novo token
3. Usar variáveis de ambiente para tokens

---

## ✅ Verificar se funcionou

Após o push, acesse:
```
https://github.com/conteudovip/conteudovip.github.io
```

Você deve ver todos os arquivos lá!

