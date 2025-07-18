#!/usr/bin/env python3
"""
Backup Automático Silencioso
Executa backup sem perguntar nada (após primeira autenticação)
"""

import os
import sys
from google_drive_manual import CodespaceGoogleDriveUploader

def silent_backup():
    """Backup completamente automático"""
    uploader = CodespaceGoogleDriveUploader()
    
    # Verificar se já tem token
    if not uploader.load_existing_token():
        print("❌ Token não encontrado. Execute primeiro:")
        print("   python3 google-drive-manual.py")
        print("   Escolha opção 2 para autenticar")
        return False
    
    print("🚀 BACKUP AUTOMÁTICO INICIADO")
    print("=" * 40)
    
    # Capturar ambiente
    print("1️⃣ Capturando ambiente...")
    if os.path.exists("./capture-environment.sh"):
        os.system("./capture-environment.sh > /dev/null 2>&1")
    
    # Criar backup
    print("2️⃣ Criando backup...")
    backup_file = uploader.create_backup()
    
    if not backup_file:
        print("❌ Falha ao criar backup")
        return False
    
    # Criar pasta no Drive
    print("3️⃣ Conectando ao Google Drive...")
    folder_id = uploader.create_folder()
    
    if not folder_id:
        print("❌ Falha ao conectar")
        return False
    
    # Upload
    print("4️⃣ Fazendo upload...")
    file_id = uploader.upload_file(backup_file, folder_id)
    
    if file_id:
        print("\n🎉 BACKUP CONCLUÍDO!")
        print(f"📁 Arquivo: {backup_file}")
        print(f"🔗 Link: https://drive.google.com/file/d/{file_id}/view")
        
        # Remover arquivo local automaticamente
        os.remove(backup_file)
        print(f"🗑️ Arquivo local removido")
        
        return True
    else:
        print("❌ Falha no upload")
        return False

if __name__ == "__main__":
    success = silent_backup()
    sys.exit(0 if success else 1)
