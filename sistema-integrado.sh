#!/bin/bash

# Sistema Integrado YouTube Automation + Google Drive
# Integra geração de conteúdo com backup automático

echo "🎬 SISTEMA INTEGRADO YOUTUBE AUTOMATION + GOOGLE DRIVE"
echo "============================================================"

# Verificar se o Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instalando..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
fi

# Verificar dependências
echo "📦 Verificando dependências..."

# Instalar requisitos base
pip3 install --user requests pillow google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Verificar se existe youtube-automation
if [ -d "youtube-automation" ]; then
    echo "📁 Diretório youtube-automation encontrado"
    
    # Instalar dependências específicas do youtube-automation
    if [ -f "youtube-automation/requirements.txt" ]; then
        echo "📋 Instalando dependências do YouTube Automation..."
        pip3 install --user -r youtube-automation/requirements.txt
    fi
else
    echo "⚠️ Diretório youtube-automation não encontrado"
fi

# Verificar se existe google-drive-manual.py
if [ ! -f "google-drive-manual.py" ]; then
    echo "❌ google-drive-manual.py não encontrado"
    echo "Execute primeiro: python3 google-drive-manual.py"
    exit 1
fi

# Verificar credenciais
if [ ! -f "google-drive-credentials.json" ]; then
    echo "❌ Credenciais do Google Drive não encontradas"
    echo "Baixe as credenciais do Google Cloud Console"
    exit 1
fi

# Função para executar automação
run_automation() {
    echo "🚀 Executando automação integrada..."
    python3 youtube-automation-drive.py
}

# Função para executar apenas YouTube automation
run_youtube_only() {
    echo "🎵 Executando apenas YouTube automation..."
    if [ -f "youtube-automation/main.py" ]; then
        cd youtube-automation
        python3 main.py
        cd ..
    else
        echo "❌ youtube-automation/main.py não encontrado"
    fi
}

# Função para executar apenas Google Drive
run_drive_only() {
    echo "☁️ Executando apenas Google Drive..."
    python3 google-drive-manual.py
}

# Função para backup completo
run_backup() {
    echo "💾 Executando backup completo..."
    if [ -f "auto-backup-drive.sh" ]; then
        bash auto-backup-drive.sh
    else
        echo "❌ auto-backup-drive.sh não encontrado"
    fi
}

# Menu interativo
show_menu() {
    echo ""
    echo "📋 OPÇÕES DISPONÍVEIS:"
    echo "1. 🎬 Automação Completa (YouTube + Drive)"
    echo "2. 🎵 Apenas YouTube Automation"
    echo "3. ☁️ Apenas Google Drive"
    echo "4. 💾 Backup Completo do Workspace"
    echo "5. 🔧 Configurar Ambiente"
    echo "6. 📊 Status do Sistema"
    echo "7. 🚪 Sair"
    echo ""
    read -p "Escolha uma opção: " choice
}

# Função para configurar ambiente
configure_environment() {
    echo "🔧 Configurando ambiente..."
    
    # Criar diretórios necessários
    mkdir -p assets/audio assets/images assets/videos
    
    # Verificar token do Google Drive
    if [ -f "drive_token.json" ]; then
        echo "✅ Token do Google Drive encontrado"
    else
        echo "⚠️ Token do Google Drive não encontrado"
        echo "Execute a autenticação manual primeiro"
        python3 google-drive-manual.py
    fi
    
    # Verificar FFmpeg
    if command -v ffmpeg &> /dev/null; then
        echo "✅ FFmpeg encontrado"
    else
        echo "📦 Instalando FFmpeg..."
        sudo apt-get install -y ffmpeg
    fi
    
    echo "✅ Ambiente configurado"
}

# Função para mostrar status
show_status() {
    echo "📊 STATUS DO SISTEMA:"
    echo "===================="
    
    # Python
    if command -v python3 &> /dev/null; then
        echo "✅ Python3: $(python3 --version)"
    else
        echo "❌ Python3: Não encontrado"
    fi
    
    # FFmpeg
    if command -v ffmpeg &> /dev/null; then
        echo "✅ FFmpeg: $(ffmpeg -version | head -1)"
    else
        echo "❌ FFmpeg: Não encontrado"
    fi
    
    # Arquivos principais
    echo ""
    echo "📁 ARQUIVOS PRINCIPAIS:"
    [ -f "google-drive-manual.py" ] && echo "✅ Google Drive Manual" || echo "❌ Google Drive Manual"
    [ -f "youtube-automation-drive.py" ] && echo "✅ YouTube Automation Drive" || echo "❌ YouTube Automation Drive"
    [ -f "google-drive-credentials.json" ] && echo "✅ Credenciais Google Drive" || echo "❌ Credenciais Google Drive"
    [ -f "drive_token.json" ] && echo "✅ Token Google Drive" || echo "❌ Token Google Drive"
    [ -d "youtube-automation" ] && echo "✅ YouTube Automation Dir" || echo "❌ YouTube Automation Dir"
    
    # Espaço em disco
    echo ""
    echo "💾 ESPAÇO EM DISCO:"
    df -h . | tail -1
    
    # Backups recentes
    echo ""
    echo "🗂️ BACKUPS RECENTES:"
    ls -la *.tar.gz 2>/dev/null | tail -3 || echo "Nenhum backup encontrado"
}

# Loop principal
while true; do
    show_menu
    
    case $choice in
        1)
            run_automation
            ;;
        2)
            run_youtube_only
            ;;
        3)
            run_drive_only
            ;;
        4)
            run_backup
            ;;
        5)
            configure_environment
            ;;
        6)
            show_status
            ;;
        7)
            echo "👋 Saindo..."
            break
            ;;
        *)
            echo "❌ Opção inválida. Tente novamente."
            ;;
    esac
    
    echo ""
    read -p "Pressione Enter para continuar..."
done
