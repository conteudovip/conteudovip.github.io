# 📥 Como Instalar o Git no Windows

## Opção 1: Download Direto

1. **Acesse:** https://git-scm.com/download/win
2. **Baixe** o instalador (Git-2.x.x-64-bit.exe)
3. **Execute** o instalador
4. **Mantenha todas as opções padrão** (Next, Next, Install)
5. **Após instalar**, reinicie o PowerShell

## Opção 2: Com Chocolatey (se tiver instalado)

```powershell
choco install git
```

---

## ✅ Verificar se Instalou

Abra o PowerShell e digite:

```powershell
git --version
```

Se aparecer algo como `git version 2.x.x`, está instalado! ✅

---

## 🚀 Depois de Instalar

Execute o script novamente:

```powershell
powershell -ExecutionPolicy Bypass -File fazer-commit.ps1
```

---

## 📝 Alternativa: Usar GitHub Desktop

Se preferir uma interface gráfica:

1. Baixe: https://desktop.github.com/
2. Faça login com sua conta GitHub
3. Adicione o repositório local
4. Faça commit e push pela interface



