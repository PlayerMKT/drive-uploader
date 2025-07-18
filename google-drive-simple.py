#!/usr/bin/env python3
"""
Google Drive Uploader Simples - Versão Manual
Funciona com credenciais web através de autenticação manual
"""

import os
import json
import requests
import tarfile
from datetime import datetime
import base64

class SimpleGoogleDriveUploader:
    def __init__(self):
        self.access_token = None
        self.creds_file = "google-drive-credentials.json"
        
    def get_client_info(self):
        """Extrai informações do cliente das credenciais"""
        try:
            with open(self.creds_file, 'r') as f:
                creds = json.load(f)
                
            if 'web' in creds:
                client_id = creds['web']['client_id']
                client_secret = creds['web']['client_secret']
                return client_id, client_secret
            else:
                print("❌ Credenciais web não encontradas")
                return None, None
                
        except Exception as e:
            print(f"❌ Erro ao ler credenciais: {e}")
            return None, None
    
    def authenticate_manual(self):
        """Autenticação manual simplificada"""
        client_id, client_secret = self.get_client_info()
        
        if not client_id or not client_secret:
            return False
        
        # URL de autorização
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri=urn:ietf:wg:oauth:2.0:oob&"
            f"scope=https://www.googleapis.com/auth/drive.file&"
            f"response_type=code&"
            f"access_type=offline&"
            f"prompt=consent"
        )
        
        print("\n🔗 AUTENTICAÇÃO GOOGLE DRIVE")
        print("=" * 50)
        print(f"1. Acesse esta URL:")
        print(f"   {auth_url}")
        print("\n2. Faça login e autorize o aplicativo")
        print("3. Copie o código de autorização mostrado")
        print("=" * 50)
        
        auth_code = input("\n📋 Cole o código aqui: ").strip()
        
        if not auth_code:
            print("❌ Código não fornecido")
            return False
        
        # Trocar código por token
        token_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'
        }
        
        try:
            response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
            
            if response.status_code == 200:
                token_info = response.json()
                self.access_token = token_info.get('access_token')
                
                if self.access_token:
                    print("✅ Token obtido com sucesso!")
                    
                    # Salvar token
                    with open('access_token.txt', 'w') as f:
                        f.write(self.access_token)
                    
                    return True
                else:
                    print("❌ Token não encontrado na resposta")
                    return False
            else:
                print(f"❌ Erro na obtenção do token: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return False
    
    def load_existing_token(self):
        """Carrega token existente"""
        if os.path.exists('access_token.txt'):
            try:
                with open('access_token.txt', 'r') as f:
                    self.access_token = f.read().strip()
                    
                # Testar token
                headers = {'Authorization': f'Bearer {self.access_token}'}
                response = requests.get('https://www.googleapis.com/drive/v3/about?fields=user', headers=headers)
                
                if response.status_code == 200:
                    user_info = response.json()
                    print(f"✅ Token válido - Usuário: {user_info.get('user', {}).get('emailAddress', 'N/A')}")
                    return True
                else:
                    print("⚠️ Token expirado, nova autenticação necessária")
                    return False
                    
            except Exception as e:
                print(f"❌ Erro ao carregar token: {e}")
                return False
        else:
            return False
    
    def create_folder(self, folder_name="Codespace-Backups"):
        """Cria pasta no Google Drive"""
        if not self.access_token:
            print("❌ Token não disponível")
            return None
        
        # Verificar se pasta existe
        headers = {'Authorization': f'Bearer {self.access_token}'}
        search_url = f"https://www.googleapis.com/drive/v3/files?q=name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        
        try:
            response = requests.get(search_url, headers=headers)
            
            if response.status_code == 200:
                files = response.json().get('files', [])
                
                if files:
                    folder_id = files[0]['id']
                    print(f"📁 Pasta encontrada: {folder_name}")
                    return folder_id
                else:
                    # Criar pasta
                    folder_data = {
                        'name': folder_name,
                        'mimeType': 'application/vnd.google-apps.folder'
                    }
                    
                    create_response = requests.post(
                        'https://www.googleapis.com/drive/v3/files',
                        headers={
                            'Authorization': f'Bearer {self.access_token}',
                            'Content-Type': 'application/json'
                        },
                        json=folder_data
                    )
                    
                    if create_response.status_code == 200:
                        folder_info = create_response.json()
                        folder_id = folder_info['id']
                        print(f"📁 Pasta criada: {folder_name}")
                        return folder_id
                    else:
                        print(f"❌ Erro ao criar pasta: {create_response.text}")
                        return None
            else:
                print(f"❌ Erro na busca: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def upload_file(self, file_path, folder_id=None):
        """Upload de arquivo"""
        if not self.access_token:
            print("❌ Token não disponível")
            return None
        
        if not os.path.exists(file_path):
            print(f"❌ Arquivo não encontrado: {file_path}")
            return None
        
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        print(f"📤 Fazendo upload: {file_name} ({file_size/1024/1024:.1f} MB)")
        
        # Metadados do arquivo
        metadata = {
            'name': file_name,
            'description': f"Backup do codespace - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        }
        
        if folder_id:
            metadata['parents'] = [folder_id]
        
        try:
            # Upload usando resumable upload
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            # Iniciar upload
            upload_url = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable'
            
            response = requests.post(upload_url, headers=headers, json=metadata)
            
            if response.status_code == 200:
                session_url = response.headers.get('Location')
                
                # Upload do arquivo
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                
                upload_headers = {
                    'Content-Type': 'application/gzip'
                }
                
                upload_response = requests.put(session_url, headers=upload_headers, data=file_data)
                
                if upload_response.status_code == 200:
                    file_info = upload_response.json()
                    print(f"✅ Upload concluído!")
                    print(f"📄 ID: {file_info.get('id')}")
                    print(f"🔗 Link: https://drive.google.com/file/d/{file_info.get('id')}/view")
                    return file_info.get('id')
                else:
                    print(f"❌ Erro no upload: {upload_response.text}")
                    return None
            else:
                print(f"❌ Erro ao iniciar upload: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Erro no upload: {e}")
            return None
    
    def create_backup(self):
        """Cria backup tar.gz"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"codespace-backup-{timestamp}"
        tar_file = f"{backup_name}.tar.gz"
        
        print("📦 Criando backup...")
        
        try:
            with tarfile.open(tar_file, "w:gz") as tar:
                # Adicionar arquivos e diretórios importantes
                items_to_backup = [
                    ".codespace-config",
                    "package.json",
                    "package-lock.json",
                    "tsconfig.json",
                    "gulpfile.js",
                    ".gitignore",
                    "README.md",
                    "nodes",
                    "credentials",
                    "youtube-automation"
                ]
                
                for item in items_to_backup:
                    if os.path.exists(item):
                        tar.add(item, arcname=f"{backup_name}/{item}")
                        print(f"✅ Adicionado: {item}")
                
                # Adicionar scripts Python e shell
                for ext in ['.py', '.sh']:
                    for file in os.listdir('.'):
                        if file.endswith(ext) and os.path.isfile(file):
                            tar.add(file, arcname=f"{backup_name}/{file}")
                            print(f"✅ Adicionado: {file}")
            
            size = os.path.getsize(tar_file) / (1024 * 1024)
            print(f"📦 Backup criado: {tar_file} ({size:.1f} MB)")
            
            return tar_file
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return None
    
    def full_backup(self):
        """Backup completo"""
        print("\n🚀 BACKUP COMPLETO PARA GOOGLE DRIVE")
        print("=" * 50)
        
        # 1. Capturar ambiente
        print("1️⃣ Capturando ambiente...")
        if os.path.exists("./capture-environment.sh"):
            os.system("./capture-environment.sh")
        
        # 2. Autenticar
        print("\n2️⃣ Autenticando...")
        if not self.load_existing_token():
            if not self.authenticate_manual():
                print("❌ Falha na autenticação")
                return
        
        # 3. Criar backup
        print("\n3️⃣ Criando backup...")
        backup_file = self.create_backup()
        
        if not backup_file:
            print("❌ Falha ao criar backup")
            return
        
        # 4. Criar pasta
        print("\n4️⃣ Preparando pasta no Drive...")
        folder_id = self.create_folder()
        
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
    print("☁️ GOOGLE DRIVE UPLOADER SIMPLES")
    print("=" * 40)
    
    uploader = SimpleGoogleDriveUploader()
    
    print("\n📋 OPÇÕES:")
    print("1. Fazer backup completo")
    print("2. Apenas autenticar")
    print("3. Upload de arquivo específico")
    print("4. Sair")
    
    choice = input("\nEscolha: ").strip()
    
    if choice == '1':
        uploader.full_backup()
    elif choice == '2':
        if not uploader.load_existing_token():
            uploader.authenticate_manual()
    elif choice == '3':
        file_path = input("Caminho do arquivo: ").strip()
        if os.path.exists(file_path):
            if not uploader.load_existing_token():
                if uploader.authenticate_manual():
                    folder_id = uploader.create_folder()
                    uploader.upload_file(file_path, folder_id)
            else:
                folder_id = uploader.create_folder()
                uploader.upload_file(file_path, folder_id)
        else:
            print("❌ Arquivo não encontrado")
    elif choice == '4':
        print("👋 Saindo...")
    else:
        print("❌ Opção inválida")

if __name__ == "__main__":
    main()
