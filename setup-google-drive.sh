#!/bin/bash

# Google Drive Setup Script
# Configuração rápida para conexão com Google Drive

echo "☁️ CONFIGURAÇÃO DO GOOGLE DRIVE"
echo "================================"

# Verificar se Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    echo "Instalando Python3..."
    sudo apt-get update && sudo apt-get install -y python3 python3-pip
fi

# Instalar dependências do Google Drive
echo "📦 Instalando dependências do Google Drive..."
pip3 install --user google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Verificar se foi instalado
python3 -c "import googleapiclient; print('✅ Google API Client instalado')" 2>/dev/null || echo "❌ Falha na instalação"

echo ""
echo "🔧 PASSOS PARA CONFIGURAR GOOGLE DRIVE:"
echo "========================================"
echo ""
echo "1️⃣ Acesse: https://console.cloud.google.com/"
echo ""
echo "2️⃣ Crie um novo projeto ou selecione existente"
echo ""
echo "3️⃣ Ative a API do Google Drive:"
echo "   - Vá em 'APIs & Services' > 'Library'"
echo "   - Procure por 'Google Drive API'"
echo "   - Clique em 'Enable'"
echo ""
echo "4️⃣ Crie credenciais OAuth 2.0:"
echo "   - Vá em 'APIs & Services' > 'Credentials'"
echo "   - Clique em 'Create Credentials' > 'OAuth 2.0 Client IDs'"
echo "   - Escolha 'Desktop Application'"
echo "   - Dê um nome (ex: 'Codespace Backup')"
echo "   - Baixe o arquivo JSON"
echo ""
echo "5️⃣ Renomeie o arquivo baixado para: google-drive-credentials.json"
echo ""
echo "6️⃣ Execute o script de upload:"
echo "   python3 google-drive-uploader.py"
echo ""

# Criar arquivo de instruções
cat > google-drive-setup-instructions.md << 'EOF'
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
EOF

echo "📋 Instruções detalhadas salvas em: google-drive-setup-instructions.md"
echo ""
echo "🚀 Próximos passos:"
echo "1. Configure as credenciais seguindo as instruções acima"
echo "2. Execute: python3 google-drive-uploader.py"
echo "3. Escolha a opção 2 para fazer backup completo"
