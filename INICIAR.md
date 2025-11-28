# 🚀 Como Iniciar Bot + API com Um Comando

## ✅ Solução Rápida (Recomendado)

### Opção 1: Clique Duas Vezes
1. Clique duas vezes no arquivo **`iniciar.bat`**
2. Pronto! Bot e API iniciados automaticamente

### Opção 2: Linha de Comando
```cmd
iniciar.bat
```

---

## 🔧 Se o PowerShell Bloquear (Erro de Política)

Se você tentar usar `iniciar.ps1` e receber erro de política de execução, use uma destas opções:

### Solução A: Usar o .bat (Mais Fácil)
```cmd
iniciar.bat
```
O arquivo `.bat` não precisa de permissões especiais!

### Solução B: Habilitar Scripts PowerShell (Uma Vez)
Abra o PowerShell **como Administrador** e execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Depois pode usar:
```powershell
.\iniciar.ps1
```

### Solução C: Comando Direto (Sempre Funciona)
```powershell
cd bot
python bot.py
```
Isso já inicia bot + API automaticamente!

---

## 📋 O Que Acontece Quando Inicia

Quando você executa qualquer uma das opções acima:

✅ **Bot do Telegram** - Fica ativo e responde comandos
✅ **API HTTP** - Inicia na porta 8080
✅ **Monitoramento** - Verifica pagamentos automaticamente

---

## 🧪 Testar o Site

Depois que o bot estiver rodando:

1. **Abra outro terminal** (deixe o bot rodando)
2. Execute:
   ```powershell
   python -m http.server 3000
   ```
3. Acesse no navegador:
   ```
   http://localhost:3000
   ```

---

## 🛑 Para Parar

No terminal onde o bot está rodando, pressione:
```
CTRL + C
```

---

## 💡 Dica

O arquivo **`iniciar.bat`** é a forma mais simples e sempre funciona, sem precisar configurar nada!

