#!/bin/bash

# Script para instalar o node n8n-nodes-google-ai localmente

echo "🚀 Instalando n8n-nodes-google-ai localmente..."

# Verificar se o n8n está instalado
if ! command -v n8n &> /dev/null
then
    echo "❌ n8n não está instalado. Por favor, instale o n8n primeiro."
    echo "📖 Veja: https://docs.n8n.io/getting-started/installation/"
    exit 1
fi

# Construir o projeto
echo "📦 Construindo o projeto..."
npm run build

# Gerar o pacote
echo "📦 Gerando o pacote..."
npm pack

# Verificar se o arquivo foi criado
PACKAGE_FILE="n8n-nodes-google-ai-1.0.0.tgz"
if [ -f "$PACKAGE_FILE" ]; then
    echo "✅ Pacote criado: $PACKAGE_FILE"
    echo "📍 Caminho completo: $(pwd)/$PACKAGE_FILE"
    echo ""
    echo "🎯 Para instalar no n8n:"
    echo "1. Acesse o n8n em http://localhost:5678"
    echo "2. Vá para Settings → Community Nodes"
    echo "3. Use o caminho: $(pwd)/$PACKAGE_FILE"
    echo ""
    echo "🔑 Não esqueça de configurar as credenciais do Google AI:"
    echo "1. Obtenha uma API Key em: https://ai.google.dev/"
    echo "2. No n8n, vá para Credentials → Add Credential"
    echo "3. Escolha 'Google AI API' e insira sua API Key"
else
    echo "❌ Erro ao criar o pacote."
    exit 1
fi

echo "✅ Instalação preparada com sucesso!"
