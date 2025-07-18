#!/bin/bash

# Backup Automático para Google Drive
# Após a primeira autenticação, funciona 100% automático

echo "🚀 BACKUP AUTOMÁTICO GOOGLE DRIVE"
echo "=================================="

# Verificar se já existe token
if [ -f "access_token.txt" ]; then
    echo "✅ Token encontrado - Backup automático!"
    echo "📦 Iniciando backup..."
    
    # Executar backup automático
    python3 -c "
from google_drive_manual import CodespaceGoogleDriveUploader
uploader = CodespaceGoogleDriveUploader()
uploader.full_backup()
"
else
    echo "🔐 Primeira execução - Autenticação necessária"
    echo "📋 Após esta autenticação, próximas execuções serão automáticas"
    echo ""
    
    # Executar com autenticação
    python3 google-drive-manual.py
fi

echo ""
echo "✅ Processo concluído!"
echo "🎯 Próximas execuções serão 100% automáticas!"
