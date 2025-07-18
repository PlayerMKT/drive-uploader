#!/bin/bash

# Auto-generated installation script
# Execute este script para replicar o ambiente

set -e

echo "🚀 Instalando ambiente capturado..."

# Função para logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Instalar Node.js via nvm se não estiver instalado
if ! command -v node >/dev/null 2>&1; then
    log "Instalando Node.js..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    source ~/.bashrc
    nvm install node
    nvm use node
fi

# Instalar dependências do projeto
if [ -f package.json ]; then
    log "Instalando dependências do projeto..."
    npm install
fi

# Restaurar package-lock.json se existir
if [ -f .codespace-config/package-lock.json ]; then
    log "Restaurando package-lock.json..."
    cp .codespace-config/package-lock.json ./
fi

# Instalar pacotes globais npm
if [ -f .codespace-config/npm-global-packages.json ]; then
    log "Instalando pacotes npm globais..."
    
    # Extrair e instalar pacotes globais
    if command -v jq >/dev/null 2>&1; then
        jq -r '.dependencies | keys[]' .codespace-config/npm-global-packages.json | while read package; do
            if [ "$package" != "npm" ] && [ "$package" != "corepack" ]; then
                npm install -g "$package" || log "Falha ao instalar $package"
            fi
        done
    else
        # Fallback sem jq
        grep -o '"[^"]*":' .codespace-config/npm-global-packages.json | tr -d '":' | while read package; do
            if [ "$package" != "dependencies" ] && [ "$package" != "npm" ] && [ "$package" != "corepack" ]; then
                npm install -g "$package" || log "Falha ao instalar $package"
            fi
        done
    fi
fi

# Instalar extensões do VS Code se disponível
if [ -f .codespace-config/vscode-extensions.txt ] && command -v code >/dev/null 2>&1; then
    log "Instalando extensões do VS Code..."
    while read extension; do
        if [ -n "$extension" ]; then
            code --install-extension "$extension" || log "Falha ao instalar extensão $extension"
        fi
    done < .codespace-config/vscode-extensions.txt
fi

# Instalar pacotes Python se disponível
if [ -f .codespace-config/requirements-consolidated.txt ] && command -v pip3 >/dev/null 2>&1; then
    log "Instalando pacotes Python consolidados..."
    pip3 install -r .codespace-config/requirements-consolidated.txt || log "Falha ao instalar alguns pacotes Python"
elif [ -f .codespace-config/python-requirements.txt ] && command -v pip3 >/dev/null 2>&1; then
    log "Instalando pacotes Python..."
    pip3 install -r .codespace-config/python-requirements.txt || log "Falha ao instalar alguns pacotes Python"
fi

# Instalar requirements específicos dos subprojetos
log "Verificando requirements de subprojetos..."
find .codespace-config -name "requirements_*.txt" -type f | while read req_file; do
    if [ -f "$req_file" ]; then
        log "Instalando dependências de $req_file..."
        pip3 install -r "$req_file" || log "Falha em $req_file"
    fi
done

# Executar build se necessário
if [ -f package.json ] && npm run | grep -q "build"; then
    log "Executando build do projeto..."
    npm run build || log "Build falhou, mas continuando..."
fi

log "✅ Instalação concluída!"
log "📋 Verifique o arquivo .codespace-config/system-info.txt para detalhes do ambiente original"
log "🔧 Execute 'npm run dev' ou outros comandos conforme necessário"

