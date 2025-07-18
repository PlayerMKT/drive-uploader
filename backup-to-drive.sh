#!/bin/bash

# Backup Automático para Google Drive
# Script integrado que faz tudo: captura ambiente + upload para Drive

echo "☁️ SISTEMA DE BACKUP AUTOMÁTICO PARA GOOGLE DRIVE"
echo "=================================================="

# Função para logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Verificar se as dependências estão instaladas
check_dependencies() {
    log "Verificando dependências..."
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        log "❌ Python3 não encontrado!"
        return 1
    fi
    
    # Verificar bibliotecas Google
    python3 -c "import googleapiclient, google.auth, google_auth_oauthlib" 2>/dev/null
    if [ $? -ne 0 ]; then
        log "📦 Instalando bibliotecas Google Drive..."
        pip3 install --user google-api-python-client google-auth-httplib2 google-auth-oauthlib
    fi
    
    log "✅ Dependências verificadas"
    return 0
}

# Verificar credenciais
check_credentials() {
    log "Verificando credenciais..."
    
    if [ ! -f "google-drive-credentials.json" ]; then
        log "❌ Arquivo de credenciais não encontrado!"
        log "📋 Criando template..."
        
        cat > google-drive-credentials.json << 'EOF'
{
  "installed": {
    "client_id": "SEU_CLIENT_ID_AQUI.apps.googleusercontent.com",
    "project_id": "seu-projeto-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "SEU_CLIENT_SECRET_AQUI",
    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
  }
}
EOF
        
        log "📋 Template criado: google-drive-credentials.json"
        log "🔧 Configure suas credenciais e execute novamente"
        
        echo ""
        echo "CONFIGURE O GOOGLE DRIVE:"
        echo "========================"
        echo "1. Acesse: https://console.cloud.google.com/"
        echo "2. Crie projeto e ative Google Drive API"
        echo "3. Crie credenciais OAuth 2.0 Desktop"
        echo "4. Baixe o JSON e substitua google-drive-credentials.json"
        echo "5. Execute novamente: $0"
        
        return 1
    fi
    
    # Verificar se não é template
    if grep -q "SEU_CLIENT_ID_AQUI" google-drive-credentials.json; then
        log "❌ Credenciais não configuradas (ainda é template)"
        log "🔧 Edite google-drive-credentials.json com suas credenciais reais"
        return 1
    fi
    
    log "✅ Credenciais encontradas"
    return 0
}

# Capturar ambiente
capture_environment() {
    log "1️⃣ Capturando ambiente..."
    
    if [ -f "./capture-environment.sh" ]; then
        chmod +x ./capture-environment.sh
        ./capture-environment.sh
        log "✅ Ambiente capturado"
    else
        log "❌ Script capture-environment.sh não encontrado"
        return 1
    fi
}

# Executar upload
execute_upload() {
    log "2️⃣ Executando upload para Google Drive..."
    
    if [ -f "google-drive-uploader.py" ]; then
        python3 -c "
import sys
sys.path.append('.')
from google_drive_uploader import GoogleDriveUploader
uploader = GoogleDriveUploader()
uploader.full_backup_and_upload()
" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            log "✅ Upload concluído com sucesso!"
        else
            log "⚠️ Houve problemas no upload, tentando modo interativo..."
            python3 google-drive-uploader.py
        fi
    else
        log "❌ Script google-drive-uploader.py não encontrado"
        return 1
    fi
}

# Menu interativo
interactive_menu() {
    while true; do
        echo ""
        echo "📋 MENU DE BACKUP GOOGLE DRIVE"
        echo "==============================="
        echo "1. Configurar credenciais"
        echo "2. Fazer backup completo"
        echo "3. Verificar status"
        echo "4. Upload manual"
        echo "5. Ver instruções"
        echo "6. Sair"
        echo ""
        
        read -p "Escolha uma opção: " choice
        
        case $choice in
            1)
                echo "🔧 Abrindo arquivo de credenciais..."
                if command -v code &> /dev/null; then
                    code google-drive-credentials.json
                elif command -v nano &> /dev/null; then
                    nano google-drive-credentials.json
                else
                    echo "📝 Edite o arquivo: google-drive-credentials.json"
                fi
                ;;
            2)
                log "🚀 Iniciando backup completo..."
                if check_dependencies && check_credentials; then
                    capture_environment && execute_upload
                else
                    log "❌ Verifique as dependências e credenciais"
                fi
                ;;
            3)
                echo "📊 STATUS DO SISTEMA:"
                echo "===================="
                check_dependencies
                check_credentials
                
                if [ -f ".codespace-config/system-info.txt" ]; then
                    echo "✅ Último backup: $(stat -c %y .codespace-config/system-info.txt)"
                else
                    echo "❌ Nenhum backup local encontrado"
                fi
                ;;
            4)
                if [ -f "google-drive-uploader.py" ]; then
                    python3 google-drive-uploader.py
                else
                    log "❌ Uploader não encontrado"
                fi
                ;;
            5)
                if [ -f "google-drive-setup-instructions.md" ]; then
                    if command -v code &> /dev/null; then
                        code google-drive-setup-instructions.md
                    else
                        cat google-drive-setup-instructions.md
                    fi
                else
                    log "❌ Instruções não encontradas"
                fi
                ;;
            6)
                log "👋 Saindo..."
                exit 0
                ;;
            *)
                echo "❌ Opção inválida"
                ;;
        esac
        
        echo ""
        read -p "Pressione Enter para continuar..."
    done
}

# Função principal
main() {
    # Se não há argumentos, mostrar menu
    if [ $# -eq 0 ]; then
        interactive_menu
        return
    fi
    
    # Processar argumentos
    case $1 in
        "auto"|"backup")
            log "🚀 Modo automático ativado"
            if check_dependencies && check_credentials; then
                capture_environment && execute_upload
            else
                log "❌ Configure o sistema primeiro"
                exit 1
            fi
            ;;
        "setup")
            ./setup-google-drive.sh
            ;;
        "check")
            check_dependencies
            check_credentials
            ;;
        *)
            echo "Uso: $0 [auto|backup|setup|check]"
            echo "Ou execute sem argumentos para menu interativo"
            ;;
    esac
}

# Executar função principal
main "$@"
