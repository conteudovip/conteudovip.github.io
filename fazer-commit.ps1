# Script para fazer commit e push no GitHub
Write-Host "Iniciando commit no GitHub..." -ForegroundColor Green

# Token do GitHub
$token = "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"
$repo = "conteudovip/conteudovip.github.io.git"
$remote = "https://${token}@github.com/${repo}"

# Verificar se git esta instalado
try {
    $gitVersion = git --version
    Write-Host "Git encontrado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERRO: Git nao encontrado! Instale o Git primeiro:" -ForegroundColor Red
    Write-Host "   https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Verificar se ja e um repositorio git
if (Test-Path .git) {
    Write-Host "Repositorio Git ja inicializado" -ForegroundColor Green
} else {
    Write-Host "Inicializando repositorio Git..." -ForegroundColor Yellow
    git init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Erro ao inicializar repositorio" -ForegroundColor Red
        exit 1
    }
}

# Verificar remote
$currentRemote = git remote get-url origin 2>$null
if ($currentRemote) {
    Write-Host "Remote ja configurado, atualizando..." -ForegroundColor Green
    git remote set-url origin $remote
} else {
    Write-Host "Configurando remote..." -ForegroundColor Yellow
    git remote add origin $remote
}

# Adicionar arquivos
Write-Host "Adicionando arquivos..." -ForegroundColor Yellow
git add .

# Verificar se ha mudancas
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "Nenhuma mudanca para commitar" -ForegroundColor Yellow
    
    # Verificar se ja tem commits
    $hasCommits = git log --oneline -n 1 2>$null
    if ([string]::IsNullOrWhiteSpace($hasCommits)) {
        Write-Host "Fazendo commit inicial..." -ForegroundColor Yellow
        git commit -m "Initial commit - Site Telegram Secrets VIP"
    } else {
        Write-Host "Tudo ja esta commitado" -ForegroundColor Green
    }
} else {
    Write-Host "Fazendo commit..." -ForegroundColor Yellow
    $date = Get-Date -Format "yyyy-MM-dd HH:mm"
    $commitMessage = "Update: Site Telegram Secrets VIP - $date"
    git commit -m $commitMessage
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Erro ao fazer commit" -ForegroundColor Red
        exit 1
    }
}

# Configurar branch main
Write-Host "Configurando branch main..." -ForegroundColor Yellow
git branch -M main

# Push
Write-Host "Fazendo push para o GitHub..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCESSO! Codigo enviado para o GitHub!" -ForegroundColor Green
    Write-Host "Veja em: https://github.com/conteudovip/conteudovip.github.io" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "ERRO ao fazer push" -ForegroundColor Red
    Write-Host "Verifique se o token esta correto e tem permissoes" -ForegroundColor Yellow
    exit 1
}
