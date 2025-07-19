#!/usr/bin/env python3
"""
Google Drive Upload System
Sistema completo para conectar e fazer upload para Google Drive
"""

import os
import json
import pickle
import zipfile
import tarfile
from datetime import datetime
from pathlib import Path

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    print("✅ Bibliotecas do Google Drive encontradas")
except ImportError:
    print("❌ Bibliotecas do Google Drive não encontradas")
    print("🔧 Instalando dependências...")
    import subprocess
    import sys
    
    packages = [
        "google-api-python-client",
        "google-auth-httplib2", 
        "google-auth-oauthlib"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} instalado")
        except Exception as e:
            print(f"❌ Erro ao instalar {package}: {e}")
    
    # Tentar importar novamente
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        print("✅ Importação bem-sucedida após instalação")
    except ImportError as e:
        print(f"❌ Ainda não foi possível importar: {e}")
        print("Execute: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")

# Escopos necessários para Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveUploader:
    def __init__(self):
        self.service = None
        self.creds_file = "google-drive-credentials.json"
        self.token_file = "google-drive-token.pickle"
        
    def setup_credentials(self):
        """Configura as credenciais do Google Drive"""
        print("🔐 Configurando credenciais do Google Drive...")
        
        # Verificar se já existe token
        if os.path.exists(self.token_file):
            print("📄 Token existente encontrado")
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        else:
            creds = None
            
        # Se não há credenciais válidas, autenticar
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Renovando token expirado...")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.creds_file):
                    print("❌ Arquivo de credenciais não encontrado!")
                    self.create_credentials_template()
                    return False
                
                print("🌐 Iniciando autenticação OAuth...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.creds_file, SCOPES)
                # Usar run_local_server na porta 8080, compatível com redirect URI
                creds = flow.run_local_server(host='localhost', port=8080)
            
            # Salvar credenciais para próxima execução
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('drive', 'v3', credentials=creds)
        print("✅ Conexão com Google Drive estabelecida!")
        return True
    
    def create_credentials_template(self):
        """Cria template para arquivo de credenciais"""
        template = {
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
        
        with open(self.creds_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        print(f"📋 Template criado: {self.creds_file}")
        print("\n🔧 PASSOS PARA CONFIGURAR:")
        print("1. Acesse: https://console.cloud.google.com/")
        print("2. Crie um novo projeto ou selecione existente")
        print("3. Ative a API do Google Drive")
        print("4. Crie credenciais OAuth 2.0")
        print("5. Baixe o arquivo JSON e substitua o conteúdo de google-drive-credentials.json")
        print("6. Execute novamente este script")
    
    def create_backup_folder(self, folder_name="Codespace-Backups"):
        """Cria pasta para backups no Google Drive"""
        try:
            # Verificar se pasta já existe
            results = self.service.files().list(
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
                spaces='drive'
            ).execute()
            
            items = results.get('files', [])
            
            if items:
                folder_id = items[0]['id']
                print(f"📁 Pasta existente encontrada: {folder_name}")
            else:
                # Criar nova pasta
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                
                folder = self.service.files().create(
                    body=folder_metadata,
                    fields='id'
                ).execute()
                
                folder_id = folder.get('id')
                print(f"📁 Nova pasta criada: {folder_name}")
            
            return folder_id
            
        except Exception as e:
            print(f"❌ Erro ao criar pasta: {e}")
            return None
    
    def upload_file(self, file_path, folder_id=None, description=""):
        """Faz upload de arquivo para Google Drive"""
        try:
            file_name = os.path.basename(file_path)
            
            # Metadados do arquivo
            file_metadata = {
                'name': file_name,
                'description': description
            }
            
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            # Upload do arquivo
            media = MediaFileUpload(file_path, resumable=True)
            
            print(f"📤 Fazendo upload: {file_name}")
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,size,createdTime,webViewLink'
            ).execute()
            
            print(f"✅ Upload concluído!")
            print(f"📄 Nome: {file.get('name')}")
            print(f"🆔 ID: {file.get('id')}")
            print(f"🔗 Link: {file.get('webViewLink')}")
            
            return file.get('id')
            
        except Exception as e:
            print(f"❌ Erro no upload: {e}")
            return None
    
    def create_compressed_backup(self):
        """Cria backup comprimido do ambiente"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"codespace-backup-{timestamp}"
        
        print("📦 Criando backup comprimido...")
        
        # Criar arquivo tar.gz
        tar_file = f"{backup_name}.tar.gz"
        
        with tarfile.open(tar_file, "w:gz") as tar:
            # Adicionar diretório de configuração
            if os.path.exists(".codespace-config"):
                tar.add(".codespace-config", arcname=f"{backup_name}/.codespace-config")
                print("✅ Adicionado: .codespace-config")
            
            # Adicionar arquivos importantes do projeto
            important_files = [
                "package.json",
                "package-lock.json",
                "tsconfig.json",
                "gulpfile.js",
                ".gitignore",
                "README.md",
                "capture-environment.sh",
                "manage-environment.sh",
                "dependency_manager.py",
                "interactive-requirements.py"
            ]
            
            for file in important_files:
                if os.path.exists(file):
                    tar.add(file, arcname=f"{backup_name}/{file}")
                    print(f"✅ Adicionado: {file}")
            
            # Adicionar diretórios importantes
            important_dirs = [
                "nodes",
                "credentials", 
                "youtube-automation"
            ]
            
            for dir_name in important_dirs:
                if os.path.exists(dir_name):
                    tar.add(dir_name, arcname=f"{backup_name}/{dir_name}")
                    print(f"✅ Adicionado: {dir_name}/")
        
        file_size = os.path.getsize(tar_file) / (1024 * 1024)  # MB
        print(f"📦 Backup criado: {tar_file} ({file_size:.1f} MB)")
        
        return tar_file
    
    def list_backups(self, folder_id):
        """Lista backups existentes no Google Drive"""
        try:
            results = self.service.files().list(
                q=f"'{folder_id}' in parents",
                orderBy='createdTime desc',
                fields='files(id,name,size,createdTime,webViewLink)'
            ).execute()
            
            items = results.get('files', [])
            
            if not items:
                print("📭 Nenhum backup encontrado")
                return
            
            print("\n📋 BACKUPS EXISTENTES:")
            print("-" * 80)
            
            for i, item in enumerate(items, 1):
                name = item.get('name', 'N/A')
                size = int(item.get('size', 0)) / (1024 * 1024) if item.get('size') else 0
                created = item.get('createdTime', 'N/A')
                link = item.get('webViewLink', 'N/A')
                
                print(f"{i}. {name}")
                print(f"   📏 Tamanho: {size:.1f} MB")
                print(f"   📅 Criado: {created}")
                print(f"   🔗 Link: {link}")
                print()
                
        except Exception as e:
            print(f"❌ Erro ao listar backups: {e}")
    
    def full_backup_and_upload(self):
        """Processo completo: captura ambiente + upload"""
        print("\n🚀 INICIANDO BACKUP COMPLETO PARA GOOGLE DRIVE")
        print("=" * 60)
        
        # 1. Capturar ambiente
        print("1️⃣ Capturando ambiente...")
        os.system("./capture-environment.sh")
        
        # 2. Criar backup comprimido  
        print("\n2️⃣ Criando backup comprimido...")
        backup_file = self.create_compressed_backup()
        
        if not backup_file:
            print("❌ Falha ao criar backup")
            return
        
        # 3. Conectar ao Google Drive
        print("\n3️⃣ Conectando ao Google Drive...")
        if not self.setup_credentials():
            print("❌ Falha na autenticação")
            return
        
        # 4. Criar pasta de backups
        print("\n4️⃣ Preparando pasta no Google Drive...")
        folder_id = self.create_backup_folder()
        
        if not folder_id:
            print("❌ Falha ao criar pasta")
            return
        
        # 5. Upload do backup
        print("\n5️⃣ Fazendo upload para Google Drive...")
        description = f"Backup do codespace criado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}"
        
        file_id = self.upload_file(backup_file, folder_id, description)
        
        if file_id:
            print("\n✅ BACKUP CONCLUÍDO COM SUCESSO!")
            print(f"📁 Arquivo local: {backup_file}")
            print(f"☁️ Arquivo no Drive: ID {file_id}")
            
            # Listar todos os backups
            print("\n6️⃣ Listando backups existentes...")
            self.list_backups(folder_id)
            
            # Limpar arquivo local
            cleanup = input("\n🗑️ Deseja remover o arquivo local? (s/n): ").lower()
            if cleanup == 's':
                os.remove(backup_file)
                print(f"🗑️ Arquivo local removido: {backup_file}")
        else:
            print("❌ Falha no upload")

def main():
    """Função principal"""
    print("☁️ GOOGLE DRIVE BACKUP SYSTEM")
    print("=" * 50)
    
    uploader = GoogleDriveUploader()
    
    while True:
        print("\n📋 OPÇÕES:")
        print("1. Configurar credenciais")
        print("2. Fazer backup completo")
        print("3. Listar backups existentes")
        print("4. Apenas upload de arquivo")
        print("5. Sair")
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == '1':
            uploader.setup_credentials()
        elif choice == '2':
            uploader.full_backup_and_upload()
        elif choice == '3':
            if uploader.setup_credentials():
                folder_id = uploader.create_backup_folder()
                if folder_id:
                    uploader.list_backups(folder_id)
        elif choice == '4':
            file_path = input("Caminho do arquivo: ").strip()
            if os.path.exists(file_path):
                if uploader.setup_credentials():
                    folder_id = uploader.create_backup_folder()
                    if folder_id:
                        uploader.upload_file(file_path, folder_id)
            else:
                print("❌ Arquivo não encontrado")
        elif choice == '5':
            print("👋 Saindo...")
            break
        else:
            print("❌ Opção inválida")

if __name__ == "__main__":
    main()
