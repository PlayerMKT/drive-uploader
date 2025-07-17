#!/bin/bash

# Restore Environment Script
# Restaura o ambiente a partir das configurações capturadas

set -e

echo "🔄 Restaurando ambiente a partir das configurações capturadas..."

# Verificar se existe a pasta de configurações
if [ ! -d ".codespace-config" ]; then
    echo "❌ Pasta .codespace-config não encontrada!"
    echo "Execute primeiro: ./capture-environment.sh"
    exit 1
fi

# Função para logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Verificar se o script de instalação existe
if [ -f ".codespace-config/install-environment.sh" ]; then
    log "Executando script de instalação..."
    chmod +x .codespace-config/install-environment.sh
    ./.codespace-config/install-environment.sh
else
    echo "❌ Script de instalação não encontrado!"
    exit 1
fi

# Verificar instalação
log "Verificando instalação..."

echo ""
echo "=== Verificação do Ambiente ==="
echo "Node.js: $(node --version 2>/dev/null || echo 'Não instalado')"
echo "npm: $(npm --version 2>/dev/null || echo 'Não instalado')"
echo "Projeto: $(if [ -f package.json ]; then echo 'Encontrado'; else echo 'Não encontrado'; fi)"

if [ -f package.json ]; then
    echo ""
    echo "=== Testando Build ==="
    if npm run build; then
        echo "✅ Build executado com sucesso!"
    else
        echo "⚠️ Build falhou, mas o ambiente foi restaurado"
    fi
fi

echo ""
echo "✅ Restauração concluída!"
echo "📋 Consulte .codespace-config/README.md para mais detalhes"
