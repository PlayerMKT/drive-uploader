#!/bin/bash

# Capture Environment Script
# Captura todas as dependências e configurações do codespace

set -e

echo "🔍 Capturando configurações do ambiente..."

# Criar diretório para armazenar as configurações
mkdir -p .codespace-config

# Função para logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Capturar informações do sistema
log "Capturando informações do sistema..."
cat > .codespace-config/system-info.txt << EOF
# System Information
Date: $(date)
OS: $(uname -a)
User: $(whoami)
Shell: $SHELL
EOF

# Capturar versões das ferramentas
log "Capturando versões das ferramentas..."
cat > .codespace-config/tool-versions.txt << EOF
# Tool Versions
Node.js: $(node --version 2>/dev/null || echo "Not installed")
npm: $(npm --version 2>/dev/null || echo "Not installed")
nvm: $(nvm --version 2>/dev/null || echo "Not installed")
git: $(git --version 2>/dev/null || echo "Not installed")
Python: $(python3 --version 2>/dev/null || echo "Not installed")
pip: $(pip3 --version 2>/dev/null || echo "Not installed")
EOF

# Capturar pacotes npm globais
log "Capturando pacotes npm globais..."
npm list -g --depth=0 --json > .codespace-config/npm-global-packages.json 2>/dev/null || echo "{}" > .codespace-config/npm-global-packages.json

# Capturar lista de pacotes npm globais em formato legível
npm list -g --depth=0 > .codespace-config/npm-global-packages.txt 2>/dev/null || echo "No global packages" > .codespace-config/npm-global-packages.txt

# Capturar package-lock.json se existir
if [ -f package-lock.json ]; then
    log "Copiando package-lock.json..."
    cp package-lock.json .codespace-config/
fi

# Capturar configurações do Node.js
log "Capturando configurações do Node.js..."
cat > .codespace-config/node-config.txt << EOF
# Node.js Configuration
Node Path: $(which node 2>/dev/null || echo "Not found")
npm Path: $(which npm 2>/dev/null || echo "Not found")
Node Version: $(node --version 2>/dev/null || echo "Not installed")
npm Version: $(npm --version 2>/dev/null || echo "Not installed")
npm Config: 
$(npm config list 2>/dev/null || echo "No npm config")
EOF

# Capturar variáveis de ambiente importantes
log "Capturando variáveis de ambiente..."
cat > .codespace-config/environment-variables.txt << EOF
# Environment Variables
PATH=$PATH
NODE_PATH=$NODE_PATH
NVM_DIR=$NVM_DIR
HOME=$HOME
USER=$USER
SHELL=$SHELL
PWD=$PWD
EOF

# Capturar configurações do bash
log "Capturando configurações do bash..."
if [ -f ~/.bashrc ]; then
    cp ~/.bashrc .codespace-config/bashrc-backup
fi

if [ -f ~/.bash_profile ]; then
    cp ~/.bash_profile .codespace-config/bash_profile-backup
fi

if [ -f ~/.profile ]; then
    cp ~/.profile .codespace-config/profile-backup
fi

# Capturar arquivos de configuração do projeto
log "Capturando arquivos de configuração do projeto..."
for file in tsconfig.json gulpfile.js .gitignore .eslintrc* .prettierrc*; do
    if [ -f "$file" ]; then
        cp "$file" .codespace-config/
    fi
done

# Capturar lista de extensões do VS Code se disponível
if command -v code >/dev/null 2>&1; then
    log "Capturando extensões do VS Code..."
    code --list-extensions > .codespace-config/vscode-extensions.txt 2>/dev/null || echo "No extensions found" > .codespace-config/vscode-extensions.txt
fi

# Capturar pacotes Python se disponível
if command -v pip3 >/dev/null 2>&1; then
    log "Capturando pacotes Python..."
    pip3 list --format=freeze > .codespace-config/python-requirements.txt 2>/dev/null || echo "# No Python packages" > .codespace-config/python-requirements.txt
fi

# Capturar todos os arquivos requirements.txt do projeto
log "Capturando arquivos requirements.txt..."
find . -name "requirements*.txt" -type f | while read req_file; do
    if [ -f "$req_file" ]; then
        rel_path=$(echo "$req_file" | sed 's|^\./||')
        safe_name=$(echo "$rel_path" | sed 's|/|_|g')
        log "Copiando $req_file para requirements_$safe_name"
        cp "$req_file" ".codespace-config/requirements_$safe_name" 2>/dev/null || true
    fi
done

# Criar consolidador de requirements
log "Criando consolidador de requirements..."
cat > .codespace-config/consolidate-requirements.py << 'CONSOLIDATE_EOF'
#!/usr/bin/env python3
"""
Consolidador de arquivos requirements.txt
"""
import os
import glob

def consolidate_requirements():
    """Consolida todos os arquivos requirements encontrados"""
    print("🔍 Consolidando arquivos requirements...")
    
    # Encontrar todos os arquivos requirements
    req_files = glob.glob('.codespace-config/requirements_*.txt')
    req_files.extend(glob.glob('requirements*.txt'))
    
    all_packages = set()
    
    for req_file in req_files:
        if os.path.exists(req_file):
            print(f"📄 Processando: {req_file}")
            try:
                with open(req_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            all_packages.add(line)
            except Exception as e:
                print(f"⚠️ Erro ao processar {req_file}: {e}")
    
    # Criar arquivo consolidado
    consolidated_file = '.codespace-config/requirements-consolidated.txt'
    with open(consolidated_file, 'w') as f:
        f.write("# Arquivo consolidado de requirements\n")
        f.write("# Gerado automaticamente\n\n")
        
        for package in sorted(all_packages):
            f.write(f"{package}\n")
    
    print(f"✅ Arquivo consolidado criado: {consolidated_file}")
    print(f"📊 Total de pacotes únicos: {len(all_packages)}")
    
    return consolidated_file

if __name__ == "__main__":
    consolidate_requirements()
CONSOLIDATE_EOF

chmod +x .codespace-config/consolidate-requirements.py

# Executar o consolidador
python3 .codespace-config/consolidate-requirements.py 2>/dev/null || log "Falha ao executar consolidador"

# Capturar histórico de comandos recentes
log "Capturando histórico de comandos..."
tail -100 ~/.bash_history > .codespace-config/recent-commands.txt 2>/dev/null || echo "No command history" > .codespace-config/recent-commands.txt

# Criar script de instalação
log "Criando script de instalação..."
cat > .codespace-config/install-environment.sh << 'INSTALL_EOF'
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

INSTALL_EOF

chmod +x .codespace-config/install-environment.sh

# Criar README para a configuração
cat > .codespace-config/README.md << 'README_EOF'
# Configuração do Ambiente Capturada

Este diretório contém todas as configurações e dependências capturadas do ambiente original.

## Arquivos Capturados

- `system-info.txt` - Informações do sistema operacional
- `tool-versions.txt` - Versões das ferramentas instaladas
- `npm-global-packages.json` - Pacotes npm globais (formato JSON)
- `npm-global-packages.txt` - Pacotes npm globais (formato texto)
- `node-config.txt` - Configuração do Node.js
- `environment-variables.txt` - Variáveis de ambiente importantes
- `vscode-extensions.txt` - Extensões do VS Code instaladas
- `python-requirements.txt` - Pacotes Python instalados
- `recent-commands.txt` - Comandos recentes do terminal
- `install-environment.sh` - Script de instalação automática

## Como Usar

1. Clone este repositório
2. Execute o script de instalação:
   ```bash
   chmod +x .codespace-config/install-environment.sh
   ./.codespace-config/install-environment.sh
   ```

3. Verifique se tudo foi instalado corretamente:
   ```bash
   node --version
   npm --version
   npm run build
   ```

## Restauração Manual

Se o script automático falhar, você pode instalar manualmente:

### Node.js e npm
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install node
```

### Dependências do Projeto
```bash
npm install
```

### Pacotes Globais
Consulte `npm-global-packages.txt` para a lista completa.

### Extensões VS Code
Consulte `vscode-extensions.txt` para a lista completa.

README_EOF

log "✅ Captura concluída!"
log "📁 Configurações salvas em: .codespace-config/"
log "📋 Para replicar o ambiente, execute: ./.codespace-config/install-environment.sh"
log "📖 Consulte .codespace-config/README.md para mais detalhes"

echo ""
echo "Resumo dos arquivos capturados:"
ls -la .codespace-config/
