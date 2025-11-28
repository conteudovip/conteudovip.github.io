# ⚠️ Git Não Está Instalado - Solução

## 🚨 Problema
O PowerShell está mostrando:
```
git : O termo 'git' não é reconhecido...
```

Isso significa que o **Git não está instalado** no seu Windows.

---

## ✅ Solução: Instalar o Git

### Passo 1: Baixar o Git

1. Acesse: **https://git-scm.com/download/win**
2. O download iniciará automaticamente
3. Ou clique no botão de download se não iniciar

### Passo 2: Instalar

1. **Execute** o arquivo baixado (ex: `Git-2.xx.xx-64-bit.exe`)
2. Clique **Next** em todas as telas
3. **Mantenha as opções padrão**
4. Clique **Install**
5. Aguarde a instalação terminar
6. Clique **Finish**

### Passo 3: Reiniciar o PowerShell

**IMPORTANTE:** Após instalar, você DEVE:
1. **Fechar** o PowerShell atual
2. **Abrir um novo** PowerShell
3. Ou reiniciar o terminal

Isso é necessário para o PowerShell reconhecer o Git!

---

## 🧪 Testar se Funcionou

Após instalar e abrir um NOVO PowerShell:

```powershell
git --version
```

**Se aparecer:** `git version 2.xx.x` ✅ **Funcionou!**

**Se ainda der erro:** Reinicie o computador ou verifique se instalou corretamente.

---

## 🚀 Depois de Instalar

1. **Abra um NOVO PowerShell**
2. **Navegue até a pasta do projeto:**
   ```powershell
   cd C:\Users\vini\Desktop\site
   ```
3. **Execute o script:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File fazer-commit.ps1
   ```

---

## 📋 Ou Execute os Comandos Manualmente

```powershell
cd C:\Users\vini\Desktop\site
git init
git remote add origin https://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@github.com/conteudovip/conteudovip.github.io.git
git add .
git commit -m "Initial commit - Site Telegram Secrets VIP"
git branch -M main
git push -u origin main
```

---

## 🎯 Resumo Rápido

1. ✅ Baixe Git: https://git-scm.com/download/win
2. ✅ Instale (mantenha padrão)
3. ✅ **FECHE e ABRA NOVO PowerShell** (importante!)
4. ✅ Execute o script ou comandos acima

---

## 💡 Alternativa: GitHub Desktop

Se preferir interface gráfica:

1. Baixe: https://desktop.github.com/
2. Instale e faça login
3. Adicione o repositório local
4. Faça commit e push pela interface

---

## ❓ Ainda Não Funciona?

1. Verifique se instalou o Git corretamente
2. Reinicie o computador
3. Tente instalar novamente
4. Use o GitHub Desktop como alternativa



