# 🚀 Como Rodar o Script PowerShell

## Método 1: PowerShell Aberto (Recomendado)

### Passo a Passo:

1. **Abra o PowerShell:**
   - Pressione `Win + X`
   - Escolha "Windows PowerShell" ou "Terminal"
   - Ou pressione `Win + R`, digite `powershell` e Enter

2. **Navegue até a pasta do projeto:**
   ```powershell
   cd C:\Users\vini\Desktop\site
   ```

3. **Execute o script:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File fazer-commit.ps1
   ```

---

## Método 2: Direto do Explorador de Arquivos

1. **Abra a pasta do projeto:**
   - Navegue até: `C:\Users\vini\Desktop\site`

2. **No menu superior, clique em "Arquivo" → "Abrir Windows PowerShell"**

3. **Execute o comando:**
   ```powershell
   .\fazer-commit.ps1
   ```

   Se der erro de permissão, execute:
   ```powershell
   powershell -ExecutionPolicy Bypass -File fazer-commit.ps1
   ```

---

## Método 3: Botão Direito no Arquivo

1. **Clique com botão direito** no arquivo `fazer-commit.ps1`

2. **Escolha "Executar com PowerShell"**

   ⚠️ Se der erro de permissão, use o Método 1 ou 2.

---

## 🔧 Se Der Erro de Permissão

O PowerShell pode bloquear scripts por segurança. Solução:

### Opção A: Bypass temporário
```powershell
powershell -ExecutionPolicy Bypass -File fazer-commit.ps1
```

### Opção B: Permitir scripts (mais permanente)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois execute normalmente:
```powershell
.\fazer-commit.ps1
```

---

## ✅ O que o Script Faz

O script vai:
1. ✅ Verificar se o Git está instalado
2. ✅ Inicializar o repositório Git (se necessário)
3. ✅ Configurar o remote do GitHub
4. ✅ Adicionar todos os arquivos
5. ✅ Fazer commit
6. ✅ Fazer push para o GitHub

---

## 📝 Comandos Rápidos (Copy & Paste)

Abra o PowerShell e cole estes comandos:

```powershell
cd C:\Users\vini\Desktop\site
powershell -ExecutionPolicy Bypass -File fazer-commit.ps1
```

---

## ❓ Problemas Comuns

### Erro: "git não é reconhecido"
**Solução:** Instale o Git primeiro
- Baixe: https://git-scm.com/download/win
- Instale e reinicie o PowerShell

### Erro: "Cannot be loaded because running scripts is disabled"
**Solução:** Use o comando com bypass:
```powershell
powershell -ExecutionPolicy Bypass -File fazer-commit.ps1
```

### Erro: "Repository not found" ou "Authentication failed"
**Solução:** Verifique se o token está correto no script

---

## 🎯 Resumo Ultra Rápido

1. Abra PowerShell
2. Digite: `cd C:\Users\vini\Desktop\site`
3. Digite: `powershell -ExecutionPolicy Bypass -File fazer-commit.ps1`
4. Enter! ✅



