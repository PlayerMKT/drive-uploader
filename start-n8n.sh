#!/bin/bash

# Script para configurar e iniciar o n8n no GitHub Codespaces
# Autor: GitHub Copilot
# Data: $(date)

echo "🚀 Configurando n8n para GitHub Codespaces..."

# Carrega as variáveis do arquivo .env
if [ -f .env ]; then
    export $(cat .env | xargs)
    echo "✅ Variáveis carregadas do arquivo .env"
else
    echo "❌ Arquivo .env não encontrado!"
    exit 1
fi

# Exibe as configurações
echo ""
echo "📋 Configurações aplicadas:"
echo "   N8N_HOST: $N8N_HOST"
echo "   N8N_PORT: $N8N_PORT"
echo "   WEBHOOK_URL: $WEBHOOK_URL"
echo "   N8N_EDITOR_BASE_URL: $N8N_EDITOR_BASE_URL"
echo ""

# Verifica se o n8n está instalado
if ! command -v n8n &> /dev/null; then
    echo "❌ n8n não está instalado. Instalando..."
    npm install -g n8n
fi

# Para qualquer instância do n8n que esteja rodando
echo "🔄 Parando instâncias anteriores do n8n..."
pkill -f n8n || true

# Aguarda um momento
sleep 2

# Inicia o n8n com as configurações
echo "🌟 Iniciando n8n..."
n8n start &

# Aguarda o n8n inicializar
sleep 5

# Verifica se está rodando
if curl -s http://localhost:$N8N_PORT > /dev/null; then
    echo "✅ n8n iniciado com sucesso!"
    echo "🌐 Acesse: $N8N_EDITOR_BASE_URL"
else
    echo "❌ Erro ao iniciar o n8n"
    exit 1
fi
