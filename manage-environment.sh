#!/bin/bash

# Complete Environment Manager
# Gerenciador completo do ambiente - menu interativo

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para logging colorido
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Função para mostrar status do ambiente
show_status() {
    echo -e "${BLUE}=== Status do Ambiente ===${NC}"
    echo ""
    
    # Verificar Node.js
    if command -v node >/dev/null 2>&1; then
        success "Node.js: $(node --version)"
    else
        error "Node.js: Não instalado"
    fi
    
    # Verificar npm
    if command -v npm >/dev/null 2>&1; then
        success "npm: $(npm --version)"
    else
        error "npm: Não instalado"
    fi
    
    # Verificar projeto
    if [ -f "package.json" ]; then
        success "Projeto: package.json encontrado"
        
        # Verificar dependências
        if [ -d "node_modules" ]; then
            success "Dependências: Instaladas"
        else
            warn "Dependências: Não instaladas"
        fi
        
        # Verificar build
        if [ -d "dist" ]; then
            success "Build: Compilado"
        else
            warn "Build: Não compilado"
        fi
    else
        error "Projeto: package.json não encontrado"
    fi
    
    # Verificar configuração capturada
    if [ -d ".codespace-config" ]; then
        success "Configuração: Capturada em .codespace-config/"
    else
        warn "Configuração: Não capturada"
    fi
    
    echo ""
}

# Menu principal
show_menu() {
    echo -e "${BLUE}=== Gerenciador de Ambiente N8N Google AI ===${NC}"
    echo ""
    echo "1. 📊 Mostrar Status do Ambiente"
    echo "2. 📸 Capturar Ambiente Atual"
    echo "3. 🔄 Restaurar Ambiente"
    echo "4. 🔄 Sincronizar Ambiente"
    echo "5. 📦 Exportar Ambiente Completo"
    echo "6. 🛠️ Instalar Dependências do Projeto"
    echo "7. 🏗️ Executar Build"
    echo "8. 🚀 Iniciar Servidor de Desenvolvimento"
    echo "9. 🧹 Limpar Cache e Rebuild"
    echo "0. ❌ Sair"
    echo ""
    echo -n "Escolha uma opção: "
}

# Função para instalar dependências
install_dependencies() {
    log "Instalando dependências do projeto..."
    
    if [ -f "package.json" ]; then
        if npm install; then
            success "Dependências instaladas com sucesso!"
        else
            error "Falha ao instalar dependências"
            return 1
        fi
    else
        error "package.json não encontrado"
        return 1
    fi
}

# Função para executar build
run_build() {
    log "Executando build do projeto..."
    
    if [ -f "package.json" ]; then
        if npm run build; then
            success "Build executado com sucesso!"
        else
            error "Falha no build"
            return 1
        fi
    else
        error "package.json não encontrado"
        return 1
    fi
}

# Função para iniciar desenvolvimento
start_dev() {
    log "Iniciando servidor de desenvolvimento..."
    
    if [ -f "package.json" ]; then
        if npm run | grep -q "dev"; then
            echo "Pressione Ctrl+C para parar o servidor"
            npm run dev
        else
            warn "Script 'dev' não encontrado no package.json"
            echo "Scripts disponíveis:"
            npm run
        fi
    else
        error "package.json não encontrado"
        return 1
    fi
}

# Função para limpar e rebuild
clean_rebuild() {
    log "Limpando cache e executando rebuild..."
    
    # Remover node_modules e package-lock.json
    if [ -d "node_modules" ]; then
        rm -rf node_modules
        success "node_modules removido"
    fi
    
    if [ -d "dist" ]; then
        rm -rf dist
        success "dist removido"
    fi
    
    # Limpar cache do npm
    npm cache clean --force
    success "Cache do npm limpo"
    
    # Reinstalar dependências
    if install_dependencies; then
        # Executar build
        run_build
    fi
}

# Loop principal
while true; do
    clear
    show_menu
    read -r choice
    
    case $choice in
        1)
            clear
            show_status
            echo ""
            read -p "Pressione Enter para continuar..."
            ;;
        2)
            clear
            log "Capturando ambiente..."
            if ./capture-environment.sh; then
                success "Ambiente capturado com sucesso!"
            else
                error "Falha ao capturar ambiente"
            fi
            echo ""
            read -p "Pressione Enter para continuar..."
            ;;
        3)
            clear
            log "Restaurando ambiente..."
            if ./restore-environment.sh; then
                success "Ambiente restaurado com sucesso!"
            else
                error "Falha ao restaurar ambiente"
            fi
            echo ""
            read -p "Pressione Enter para continuar..."
            ;;
        4)
            clear
            log "Sincronizando ambiente..."
            if ./sync-environment.sh; then
                success "Ambiente sincronizado com sucesso!"
            else
                error "Falha ao sincronizar ambiente"
            fi
            echo ""
            read -p "Pressione Enter para continuar..."
            ;;
        5)
            clear
            log "Exportando ambiente..."
            if ./export-environment.sh; then
                success "Ambiente exportado com sucesso!"
            else
                error "Falha ao exportar ambiente"
            fi
            echo ""
            read -p "Pressione Enter para continuar..."
            ;;
        6)
            clear
            install_dependencies
            echo ""
            read -p "Pressione Enter para continuar..."
            ;;
        7)
            clear
            run_build
            echo ""
            read -p "Pressione Enter para continuar..."
            ;;
        8)
            clear
            start_dev
            echo ""
            read -p "Pressione Enter para continuar..."
            ;;
        9)
            clear
            clean_rebuild
            echo ""
            read -p "Pressione Enter para continuar..."
            ;;
        0)
            success "Saindo..."
            break
            ;;
        *)
            error "Opção inválida"
            sleep 1
            ;;
    esac
done
