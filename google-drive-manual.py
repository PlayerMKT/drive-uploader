#!/usr/bin/env python3
"""
Google Drive Uploader - Versão Manual para Codespaces
Funciona sem localhost usando autenticação manual
"""

import os
import json
import requests
import tarfile
from datetime import datetime

class CodespaceGoogleDriveUploader:
    def __init__(self):
        self.access_token = None
        self.creds_file = "google-drive-credentials.json"
        self.token_file = "access_token.txt"
        
    def get_client_info(self):
        """Extrai informações do cliente das credenciais"""
        try:
            with open(self.creds_file, 'r') as f:
                creds = json.load(f)
                
            client_id = creds['installed']['client_id']
            client_secret = creds['installed']['client_secret']
            return client_id, client_secret
                
        except Exception as e:
            print(f"❌ Erro ao ler credenciais: {e}")
            return None, None
    
    def authenticate_manual(self):
        """Autenticação manual sem localhost"""
        client_id, client_secret = self.get_client_info()
        
        if not client_id or not client_secret:
            return False
        
        # URL de autorização usando urn:ietf:wg:oauth:2.0:oob (out-of-band)
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri=urn:ietf:wg:oauth:2.0:oob&"
            f"scope=https://www.googleapis.com/auth/drive.file&"
            f"response_type=code&"
            f"access_type=offline&"
            f"prompt=consent"
        )
        
        print("\n🔗 AUTENTICAÇÃO GOOGLE DRIVE - MÉTODO MANUAL")
        print("=" * 60)
        print("🌐 PASSO 1: Acesse a URL abaixo em uma nova aba:")
        print(f"   {auth_url}")
        print("\n📝 PASSO 2: Faça login na sua conta Google")
        print("📝 PASSO 3: Autorize o aplicativo")
        print("📝 PASSO 4: Copie o CÓDIGO que aparece na tela")
        print("=" * 60)
        
        auth_code = input("\n📋 Cole o código de autorização aqui: ").strip()
        
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
            print("🔄 Obtendo token de acesso...")
            response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
            
            if response.status_code == 200:
                token_info = response.json()
                self.access_token = token_info.get('access_token')
                refresh_token = token_info.get('refresh_token')
                
                if self.access_token:
                    print("✅ Token obtido com sucesso!")
                    
                    # Salvar tokens
                    token_data = {
                        'access_token': self.access_token,
                        'refresh_token': refresh_token,
                        'client_id': client_id,
                        'client_secret': client_secret
                    }
                    
                    with open(self.token_file, 'w') as f:
                        json.dump(token_data, f)
                    
                    print("💾 Token salvo para uso futuro")
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
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as f:
                    token_data = json.load(f)
                    
                self.access_token = token_data.get('access_token')
                    
                # Testar token
                headers = {'Authorization': f'Bearer {self.access_token}'}
                response = requests.get('https://www.googleapis.com/drive/v3/about?fields=user', headers=headers)
                
                if response.status_code == 200:
                    user_info = response.json()
                    email = user_info.get('user', {}).get('emailAddress', 'N/A')
                    print(f"✅ Token válido - Usuário: {email}")
                    return True
                else:
                    print("⚠️ Token expirado, tentando renovar...")
                    return self.refresh_token(token_data)
                    
            except Exception as e:
                print(f"❌ Erro ao carregar token: {e}")
                return False
        else:
            return False
    
    def refresh_token(self, token_data):
        """Renova token expirado"""
        refresh_token = token_data.get('refresh_token')
        client_id = token_data.get('client_id')
        client_secret = token_data.get('client_secret')
        
        if not refresh_token:
            print("❌ Refresh token não disponível")
            return False
        
        try:
            refresh_data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token'
            }
            
            response = requests.post('https://oauth2.googleapis.com/token', data=refresh_data)
            
            if response.status_code == 200:
                new_token_info = response.json()
                self.access_token = new_token_info.get('access_token')
                
                # Atualizar arquivo
                token_data['access_token'] = self.access_token
                with open(self.token_file, 'w') as f:
                    json.dump(token_data, f)
                
                print("✅ Token renovado com sucesso")
                return True
            else:
                print("❌ Falha ao renovar token")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao renovar token: {e}")
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
        """Upload de arquivo usando requests"""
        if not self.access_token:
            print("❌ Token não disponível")
            return None
        
        if not os.path.exists(file_path):
            print(f"❌ Arquivo não encontrado: {file_path}")
            return None
        
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        
        print(f"📤 Fazendo upload: {file_name} ({file_size:.1f} MB)")
        
        # Metadados do arquivo
        metadata = {
            'name': file_name,
            'description': f"Backup do codespace - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        }
        
        if folder_id:
            metadata['parents'] = [folder_id]
        
        try:
            # Upload simples para arquivos pequenos (até 5MB)
            # Para arquivos maiores, usar upload resumável
            
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            # Upload multipart
            files = {
                'metadata': (None, json.dumps(metadata), 'application/json'),
                'file': (file_name, open(file_path, 'rb'), 'application/octet-stream')
            }
            
            upload_url = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart'
            
            print("⏳ Enviando arquivo...")
            response = requests.post(upload_url, headers=headers, files=files)
            
            # Fechar arquivo
            files['file'][1].close()
            
            if response.status_code == 200:
                file_info = response.json()
                file_id = file_info.get('id')
                
                print(f"✅ Upload concluído!")
                print(f"📄 ID: {file_id}")
                print(f"🔗 Link: https://drive.google.com/file/d/{file_id}/view")
                return file_id
            else:
                print(f"❌ Erro no upload: {response.status_code}")
                print(f"Resposta: {response.text}")
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
                
                # Adicionar scripts importantes
                script_files = [
                    "capture-environment.sh",
                    "manage-environment.sh", 
                    "backup-to-drive.sh",
                    "dependency_manager.py",
                    "interactive-requirements.py",
                    "google-drive-simple.py"
                ]
                
                for script in script_files:
                    if os.path.exists(script):
                        tar.add(script, arcname=f"{backup_name}/{script}")
                        print(f"✅ Adicionado: {script}")
            
            size = os.path.getsize(tar_file) / (1024 * 1024)
            print(f"📦 Backup criado: {tar_file} ({size:.1f} MB)")
            
            return tar_file
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return None
    
    def list_backups(self, folder_id):
        """Lista backups na pasta do Google Drive"""
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            url = f"https://www.googleapis.com/drive/v3/files?q='{folder_id}' in parents&orderBy=createdTime desc"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                files = response.json().get('files', [])
                
                if not files:
                    print("📭 Nenhum backup encontrado na pasta")
                    return
                
                print("\n📋 BACKUPS EXISTENTES:")
                print("-" * 60)
                
                for i, file in enumerate(files, 1):
                    name = file.get('name', 'N/A')
                    file_id = file.get('id')
                    
                    print(f"{i}. {name}")
                    print(f"   🔗 https://drive.google.com/file/d/{file_id}/view")
                    print()
            else:
                print(f"❌ Erro ao listar arquivos: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def full_backup(self):
        """Backup completo"""
        print("\n🚀 BACKUP COMPLETO PARA GOOGLE DRIVE")
        print("=" * 50)
        
        # 1. Autenticar
        print("1️⃣ Verificando autenticação...")
        if not self.load_existing_token():
            print("🔐 Nova autenticação necessária...")
            if not self.authenticate_manual():
                print("❌ Falha na autenticação")
                return
        
        # 2. Capturar ambiente
        print("\n2️⃣ Capturando ambiente...")
        if os.path.exists("./capture-environment.sh"):
            os.system("./capture-environment.sh")
        
        # 3. Criar backup
        print("\n3️⃣ Criando backup...")
        backup_file = self.create_backup()
        
        if not backup_file:
            print("❌ Falha ao criar backup")
            return
        
        # 4. Criar pasta no Drive
        print("\n4️⃣ Preparando pasta no Google Drive...")
        folder_id = self.create_folder()
        
        if not folder_id:
            print("❌ Falha ao criar pasta")
            return
        
        # 5. Upload
        print("\n5️⃣ Fazendo upload...")
        file_id = self.upload_file(backup_file, folder_id)
        
        if file_id:
            print("\n🎉 BACKUP CONCLUÍDO COM SUCESSO!")
            
            # Listar backups
            print("\n6️⃣ Listando backups existentes...")
            self.list_backups(folder_id)
            
            # Limpar arquivo local
            cleanup = input("\n🗑️ Remover arquivo local? (s/n): ").lower()
            if cleanup == 's':
                os.remove(backup_file)
                print(f"🗑️ Removido: {backup_file}")
        else:
            print("❌ Falha no upload")

def main():
    print("☁️ GOOGLE DRIVE UPLOADER - AUTENTICAÇÃO MANUAL")
    print("=" * 50)
    
    uploader = CodespaceGoogleDriveUploader()
    
    print("\n📋 OPÇÕES:")
    print("1. Fazer backup completo")
    print("2. Apenas autenticar")
    print("3. Upload do backup existente")
    print("4. Listar backups no Drive")
    print("5. Sair")
    
    choice = input("\nEscolha: ").strip()
    
    if choice == '1':
        uploader.full_backup()
    elif choice == '2':
        if not uploader.load_existing_token():
            uploader.authenticate_manual()
    elif choice == '3':
        # Procurar backup existente
        backup_files = [f for f in os.listdir('.') if f.startswith('codespace-backup-') and f.endswith('.tar.gz')]
        if backup_files:
            print("\n📦 Backups locais encontrados:")
            for i, backup in enumerate(backup_files, 1):
                size = os.path.getsize(backup) / (1024 * 1024)
                print(f"{i}. {backup} ({size:.1f} MB)")
            
            try:
                idx = int(input("\nEscolha o backup (número): ")) - 1
                if 0 <= idx < len(backup_files):
                    selected_backup = backup_files[idx]
                    
                    if not uploader.load_existing_token():
                        if uploader.authenticate_manual():
                            folder_id = uploader.create_folder()
                            if folder_id:
                                uploader.upload_file(selected_backup, folder_id)
                    else:
                        folder_id = uploader.create_folder()
                        if folder_id:
                            uploader.upload_file(selected_backup, folder_id)
                else:
                    print("❌ Número inválido")
            except ValueError:
                print("❌ Entrada inválida")
        else:
            print("❌ Nenhum backup local encontrado")
    elif choice == '4':
        if not uploader.load_existing_token():
            if uploader.authenticate_manual():
                folder_id = uploader.create_folder()
                if folder_id:
                    uploader.list_backups(folder_id)
        else:
            folder_id = uploader.create_folder()
            if folder_id:
                uploader.list_backups(folder_id)
    elif choice == '5':
        print("👋 Saindo...")
    else:
        print("❌ Opção inválida")

if __name__ == "__main__":
    main()
