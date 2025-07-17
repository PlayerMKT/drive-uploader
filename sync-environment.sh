#!/bin/bash

# Sync Environment Script
# Sincroniza o ambiente atual com as configurações capturadas

set -e

echo "🔄 Sincronizando ambiente..."

# Função para logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Verificar se existe a pasta de configurações
if [ ! -d ".codespace-config" ]; then
    log "Pasta .codespace-config não encontrada, criando captura inicial..."
    ./capture-environment.sh
fi

# Função para comparar versões
compare_versions() {
    local current=$1
    local captured=$2
    local tool=$3
    
    if [ "$current" != "$captured" ]; then
        echo "⚠️ $tool: atual=$current, capturado=$captured"
        return 1
    else
        echo "✅ $tool: $current"
        return 0
    fi
}

# Comparar versões das ferramentas
log "Comparando versões das ferramentas..."

if [ -f ".codespace-config/tool-versions.txt" ]; then
    # Extrair versões capturadas
    node_captured=$(grep "Node.js:" .codespace-config/tool-versions.txt | cut -d' ' -f2 || echo "unknown")
    npm_captured=$(grep "npm:" .codespace-config/tool-versions.txt | cut -d' ' -f2 || echo "unknown")
    
    # Versões atuais
    node_current=$(node --version 2>/dev/null || echo "not installed")
    npm_current=$(npm --version 2>/dev/null || echo "not installed")
    
    echo ""
    echo "=== Comparação de Versões ==="
    compare_versions "$node_current" "$node_captured" "Node.js"
    compare_versions "$npm_current" "$npm_captured" "npm"
fi

# Comparar pacotes globais
log "Comparando pacotes npm globais..."

if [ -f ".codespace-config/npm-global-packages.txt" ]; then
    echo ""
    echo "=== Pacotes Globais ==="
    
    # Obter lista atual
    npm list -g --depth=0 --silent > /tmp/current-globals.txt 2>/dev/null || echo "" > /tmp/current-globals.txt
    
    # Comparar com capturado
    if diff -q .codespace-config/npm-global-packages.txt /tmp/current-globals.txt >/dev/null 2>&1; then
        echo "✅ Pacotes globais estão sincronizados"
    else
        echo "⚠️ Diferenças encontradas nos pacotes globais:"
        echo "--- Capturado ---"
        cat .codespace-config/npm-global-packages.txt
        echo ""
        echo "--- Atual ---"
        cat /tmp/current-globals.txt
        echo ""
        
        read -p "Deseja instalar os pacotes faltantes? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ./.codespace-config/install-environment.sh
        fi
    fi
    
    rm -f /tmp/current-globals.txt
fi

# Verificar dependências do projeto
log "Verificando dependências do projeto..."

if [ -f "package.json" ]; then
    if [ -f "node_modules/.package-lock.json" ] || [ -f "package-lock.json" ]; then
        echo "✅ Dependências do projeto instaladas"
    else
        echo "⚠️ Dependências do projeto não instaladas"
        read -p "Deseja instalar as dependências? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            npm install
        fi
    fi
fi

# Verificar se o projeto pode ser buildado
log "Testando build do projeto..."

if [ -f "package.json" ] && npm run | grep -q "build"; then
    if npm run build --silent; then
        echo "✅ Build executado com sucesso"
    else
        echo "❌ Build falhou"
        read -p "Deseja tentar restaurar o ambiente? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ./restore-environment.sh
        fi
    fi
fi

echo ""
echo "✅ Sincronização concluída!"
echo "📋 Use './capture-environment.sh' para atualizar a captura"
echo "📋 Use './restore-environment.sh' para restaurar completamente"
