#!/bin/bash

# Script de backup automático para GitHub
# Este script salva todos os arquivos do projeto n8n Google AI

echo "🚀 Iniciando backup automático para GitHub..."

# Configurar git se necessário
git config --global user.email "codespaces@github.com"
git config --global user.name "GitHub Codespaces"

# Adicionar todos os arquivos (incluindo novos)
echo "📁 Adicionando todos os arquivos..."
git add -A

# Criar commit com timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
COMMIT_MESSAGE="🔄 Backup automático - $TIMESTAMP"

echo "💾 Criando commit: $COMMIT_MESSAGE"
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
