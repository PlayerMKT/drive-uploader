#!/bin/bash

# Script de limpeza para otimizar o Codespace
# Remove arquivos temporários e desnecessários

echo "🧹 Iniciando limpeza do Codespace..."

# Fazer backup antes da limpeza
echo "📦 Fazendo backup antes da limpeza..."
./backup-to-github.sh

echo "🗑️ Removendo arquivos temporários e duplicados..."

# Remover arquivos ZIP (já estão no Git)
rm -f *.zip *.tgz

# Remover node_modules se existir (pode ser reinstalado)
if [ -d "node_modules" ]; then
    echo "📦 Removendo node_modules (será reinstalado quando necessário)..."
    rm -rf node_modules
fi

# Remover logs
rm -f *.log
rm -rf logs/

# Remover cache do npm
if command -v npm &> /dev/null; then
    echo "🧹 Limpando cache do npm..."
    npm cache clean --force
fi

# Remover pasta upload-files (duplicada)
if [ -d "upload-files" ]; then
    echo "📁 Removendo pasta upload-files (duplicada)..."
    rm -rf upload-files
fi

# Limpar cache do sistema
echo "💾 Limpando cache do sistema..."
sudo apt-get clean 2>/dev/null || true

echo "✅ Limpeza concluída!"
echo "💾 Espaço livre:"
df -h | grep -E "(Filesystem|/dev/root)"

echo "📊 Arquivos principais mantidos:"
ls -la | grep -E "\.(ts|js|json|md)$"
