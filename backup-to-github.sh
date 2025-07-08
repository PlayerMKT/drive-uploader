#!/bin/bash

# Script de backup automático para GitHub
# Este script salva todos os arquivos do projeto n8n Google AI

echo "🚀 Iniciando backup automático para GitHub..."

# Configurar git se necessário
git config --global user.email "codespaces@github.com"
git config --global user.name "GitHub Codespaces"

# Verificar e corrigir configuração do remote origin
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ Remote 'origin' não configurado"
    echo "Por favor, configure o remote do GitHub:"
    echo "git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git"
    exit 1
fi

# Verificar se está usando SSH e converter para HTTPS no Codespaces
REMOTE_URL=$(git remote get-url origin)
if [[ $REMOTE_URL == git@github.com:* ]]; then
    echo "🔧 Detectado SSH, convertendo para HTTPS para Codespaces..."
    # Extrair usuario/repo do formato git@github.com:usuario/repo.git
    REPO_PATH=$(echo $REMOTE_URL | sed 's/git@github.com://' | sed 's/.git$//')
    NEW_URL="https://github.com/$REPO_PATH.git"
    git remote set-url origin "$NEW_URL"
    echo "✅ Remote atualizado para: $NEW_URL"
fi

# Adicionar todos os arquivos (incluindo novos)
echo "📁 Adicionando todos os arquivos..."
git add -A

# Criar commit com timestamp ou mensagem personalizada
if [ -n "$1" ]; then
    COMMIT_MESSAGE="$1"
    echo "💾 Criando commit com mensagem personalizada: $COMMIT_MESSAGE"
else
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    COMMIT_MESSAGE="🔄 Backup automático - $TIMESTAMP"
    echo "💾 Criando commit automático: $COMMIT_MESSAGE"
fi
git commit -m "$COMMIT_MESSAGE"

# Push para o repositório
echo "☁️ Enviando para GitHub..."
git push origin main

# Verificar status final
echo "✅ Status final:"
git status --porcelain

if [ $? -eq 0 ]; then
    echo "✅ Backup realizado com sucesso!"
    echo "📊 Resumo dos arquivos salvos:"
    git log --oneline -1
    echo "🌐 Todos os arquivos estão seguros no GitHub!"
else
    echo "❌ Erro durante o backup. Verifique as configurações do Git."
fi
