#!/bin/bash

# Script para carregar variáveis do n8n
# Use: source load-n8n-env.sh

echo "🔧 Carregando variáveis de ambiente do n8n..."

export N8N_HOST=0.0.0.0
export N8N_PORT=5678
export WEBHOOK_URL=https://opulent-waffle-5g95x97v74xxh7ppp-5678.app.github.dev
export N8N_EDITOR_BASE_URL=https://opulent-waffle-5g95x97v74xxh7ppp-5678.app.github.dev
export N8N_BASIC_AUTH_ACTIVE=false
export N8N_DISABLE_PRODUCTION_MAIN_PROCESS=true

echo "✅ Variáveis carregadas:"
echo "   N8N_HOST: $N8N_HOST"
echo "   N8N_PORT: $N8N_PORT"
echo "   WEBHOOK_URL: $WEBHOOK_URL"
echo "   N8N_EDITOR_BASE_URL: $N8N_EDITOR_BASE_URL"
