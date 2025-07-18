# Configuração Google Drive - Instruções Detalhadas

## Passo a Passo Completo

### 1. Acessar Google Cloud Console
- Vá para: https://console.cloud.google.com/
- Faça login com sua conta Google

### 2. Criar/Selecionar Projeto
- Clique em "Select a project" no topo
- Clique em "NEW PROJECT"
- Nome: "Codespace Backup" (ou qualquer nome)
- Clique em "CREATE"

### 3. Ativar Google Drive API
- No menu lateral, vá em "APIs & Services" > "Library"
- Procure por "Google Drive API"
- Clique no resultado
- Clique em "ENABLE"

### 4. Configurar OAuth Consent Screen
- Vá em "APIs & Services" > "OAuth consent screen"
- Escolha "External" se for conta pessoal
- Preencha:
  - App name: "Codespace Backup"
  - User support email: seu email
  - Developer contact: seu email
- Clique em "SAVE AND CONTINUE"
- Em Scopes, clique em "SAVE AND CONTINUE"
- Em Test users, adicione seu email
- Clique em "SAVE AND CONTINUE"

### 5. Criar Credenciais
- Vá em "APIs & Services" > "Credentials"
- Clique em "CREATE CREDENTIALS" > "OAuth 2.0 Client IDs"
- Application type: "Desktop application"
- Name: "Codespace Backup Client"
- Clique em "CREATE"

### 6. Baixar Credenciais
- Clique no ícone de download na credencial criada
- Salve o arquivo como `google-drive-credentials.json`
- Copie o arquivo para o diretório do projeto

### 7. Executar Upload
```bash
python3 google-drive-uploader.py
```

## Estrutura do Arquivo de Credenciais

O arquivo `google-drive-credentials.json` deve ter esta estrutura:

```json
{
  "installed": {
    "client_id": "xxxxx.apps.googleusercontent.com",
    "project_id": "seu-projeto-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "xxxxx",
    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
  }
}
```

## Uso do Sistema

### Upload Automático
```bash
# Fazer backup completo para Google Drive
python3 google-drive-uploader.py
# Escolha opção 2
```

### Comandos Úteis
```bash
# Verificar conexão
python3 -c "import googleapiclient; print('OK')"

# Listar backups
python3 google-drive-uploader.py
# Escolha opção 3
```

## Resolução de Problemas

### Erro: "google-api-python-client not found"
```bash
pip3 install --user google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Erro: "credentials not found"
- Verifique se o arquivo `google-drive-credentials.json` está no diretório correto
- Verifique se o formato JSON está correto

### Erro de autenticação
- Delete o arquivo `google-drive-token.pickle`
- Execute novamente o script
- Refaça a autenticação no navegador
