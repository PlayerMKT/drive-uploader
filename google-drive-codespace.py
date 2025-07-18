#!/usr/bin/env python3
"""
Google Drive Uploader - Versão específica para Codespaces
Funciona com credenciais web do Google Cloud Console
"""

import os
import json
import pickle
import tarfile
from datetime import datetime
import webbrowser
import urllib.parse

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    print("✅ Bibliotecas Google Drive OK")
except ImportError:
    print("❌ Instalando bibliotecas...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-api-python-client", "google-auth-httplib2", "google-auth-oauthlib"])
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

class CodespaceGoogleDriveUploader:
    def __init__(self):
        self.service = None
        self.creds_file = "google-drive-credentials.json"
        self.token_file = "google-drive-token.pickle"
        
    def setup_credentials(self):
        """Configura credenciais para Codespaces"""
        print("🔐 Configurando credenciais Google Drive...")
        
        # Verificar token existente
        creds = None
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
                    print("📄 Token existente carregado")
            except Exception as e:
                print(f"⚠️ Erro ao carregar token: {e}")
        
        # Verificar se precisa renovar
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Renovando token...")
                try:
                    creds.refresh(Request())
                    print("✅ Token renovado")
                except Exception as e:
                    print(f"❌ Erro ao renovar: {e}")
                    creds = None
            
            if not creds:
                print("🌐 Iniciando nova autenticação...")
                creds = self.authenticate_manual()
                
                if not creds:
                    return False
        
        # Salvar token
        try:
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
            print("💾 Token salvo")
        except Exception as e:
            print(f"⚠️ Erro ao salvar token: {e}")
        
        # Conectar ao serviço
        try:
            self.service = build('drive', 'v3', credentials=creds)
            print("✅ Conexão com Google Drive estabelecida!")
            return True
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            return False
    
    def authenticate_manual(self):
        """Autenticação manual para Codespaces"""
        try:
            # Carregar credenciais
            with open(self.creds_file, 'r') as f:
                creds_data = json.load(f)
            
            # Usar dados web
            if 'web' in creds_data:
                client_config = creds_data['web']
            else:
                print("❌ Credenciais web não encontradas")
                return None
            
            # Criar flow com redirect_uri correto
            flow = Flow.from_client_config(
                {"web": client_config},
                scopes=SCOPES
            )
            
            # Usar redirect_uri específico para Codespaces
            codespace_url = os.getenv('CODESPACE_NAME', 'localhost')
            if codespace_url != 'localhost':
                redirect_uri = f"https://{codespace_url}-8080.app.github.dev/"
            else:
                redirect_uri = "http://localhost:8080/"
            
            flow.redirect_uri = redirect_uri
            
            # Gerar URL de autorização
            auth_url, _ = flow.authorization_url(
                prompt='consent',
                access_type='offline'
            )
            
            print("\n🔗 AUTENTICAÇÃO MANUAL:")
            print("=" * 50)
            print(f"1. Acesse esta URL: {auth_url}")
            print("2. Faça login na sua conta Google")
            print("3. Autorize o aplicativo")
            print("4. Copie o código de autorização")
            print("=" * 50)
            
            # Solicitar código
            auth_code = input("\n📋 Cole o código de autorização aqui: ").strip()
            
            if not auth_code:
                print("❌ Código não fornecido")
                return None
            
            # Trocar código por token
            try:
                flow.fetch_token(code=auth_code)
                print("✅ Token obtido com sucesso!")
                return flow.credentials
            except Exception as e:
                print(f"❌ Erro ao obter token: {e}")
                return None
                
        except Exception as e:
            print(f"❌ Erro na autenticação: {e}")
            return None
    
    def create_backup_folder(self):
        """Cria pasta de backup no Drive"""
        try:
            folder_name = "Codespace-Backups"
            
            # Verificar se existe
            results = self.service.files().list(
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
                spaces='drive'
            ).execute()
            
            items = results.get('files', [])
            
            if items:
                folder_id = items[0]['id']
                print(f"📁 Pasta encontrada: {folder_name}")
            else:
                # Criar pasta
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                
                folder = self.service.files().create(
                    body=folder_metadata,
                    fields='id'
                ).execute()
                
                folder_id = folder.get('id')
                print(f"📁 Pasta criada: {folder_name}")
            
            return folder_id
            
        except Exception as e:
            print(f"❌ Erro ao criar pasta: {e}")
            return None
    
    def upload_file(self, file_path, folder_id=None):
        """Upload de arquivo"""
        try:
            file_name = os.path.basename(file_path)
            
            metadata = {
                'name': file_name,
                'description': f"Backup do codespace - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            }
            
            if folder_id:
                metadata['parents'] = [folder_id]
            
            media = MediaFileUpload(file_path, resumable=True)
            
            print(f"📤 Fazendo upload: {file_name}")
            
            file = self.service.files().create(
                body=metadata,
                media_body=media,
                fields='id,name,size,webViewLink'
            ).execute()
            
            print(f"✅ Upload concluído!")
            print(f"📄 Nome: {file.get('name')}")
            print(f"🔗 Link: {file.get('webViewLink')}")
            
            return file.get('id')
            
        except Exception as e:
            print(f"❌ Erro no upload: {e}")
            return None
    
    def create_backup(self):
        """Cria backup tar.gz"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"codespace-backup-{timestamp}"
        tar_file = f"{backup_name}.tar.gz"
        
        print("📦 Criando backup...")
        
        with tarfile.open(tar_file, "w:gz") as tar:
            # Adicionar arquivos importantes
            files_to_backup = [
                ".codespace-config",
                "package.json",
                "tsconfig.json",
                "nodes",
                "credentials",
                "youtube-automation",
                "*.py",
                "*.sh",
                "*.md"
            ]
            
            for item in files_to_backup:
                if os.path.exists(item):
                    tar.add(item, arcname=f"{backup_name}/{item}")
                    print(f"✅ Adicionado: {item}")
        
        size = os.path.getsize(tar_file) / (1024 * 1024)
        print(f"📦 Backup criado: {tar_file} ({size:.1f} MB)")
        
        return tar_file
    
    def full_backup(self):
        """Backup completo"""
        print("\n🚀 BACKUP COMPLETO PARA GOOGLE DRIVE")
        print("=" * 50)
        
        # 1. Capturar ambiente
        print("1️⃣ Capturando ambiente...")
        os.system("./capture-environment.sh")
        
        # 2. Criar backup
        print("\n2️⃣ Criando backup...")
        backup_file = self.create_backup()
        
        # 3. Conectar ao Drive
        print("\n3️⃣ Conectando ao Google Drive...")
        if not self.setup_credentials():
            print("❌ Falha na autenticação")
            return
        
        # 4. Criar pasta
        print("\n4️⃣ Preparando pasta...")
        folder_id = self.create_backup_folder()
        
        # 5. Upload
        print("\n5️⃣ Fazendo upload...")
        file_id = self.upload_file(backup_file, folder_id)
        
        if file_id:
            print("\n🎉 BACKUP CONCLUÍDO COM SUCESSO!")
            
            # Limpar arquivo local
            cleanup = input("\n🗑️ Remover arquivo local? (s/n): ").lower()
            if cleanup == 's':
                os.remove(backup_file)
                print(f"🗑️ Removido: {backup_file}")
        else:
            print("❌ Falha no upload")

def main():
    print("☁️ GOOGLE DRIVE UPLOADER - CODESPACES")
    print("=" * 40)
    
    uploader = CodespaceGoogleDriveUploader()
    
    print("\n📋 OPÇÕES:")
    print("1. Fazer backup completo")
    print("2. Apenas configurar credenciais")
    print("3. Sair")
    
    choice = input("\nEscolha: ").strip()
    
    if choice == '1':
        uploader.full_backup()
    elif choice == '2':
        uploader.setup_credentials()
    elif choice == '3':
        print("👋 Saindo...")
    else:
        print("❌ Opção inválida")

if __name__ == "__main__":
    main()
