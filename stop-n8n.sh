#!/bin/bash

# Script para parar o n8n
# Autor: GitHub Copilot

echo "🛑 Parando n8n..."

# Método 1: Parar pelo nome do processo
echo "   Procurando processos n8n..."
N8N_PIDS=$(pgrep -f "n8n")

if [ -n "$N8N_PIDS" ]; then
    echo "   Encontrados processos: $N8N_PIDS"
    
    # Tenta parar graciosamente primeiro
    echo "   Enviando SIGTERM..."
    pkill -TERM -f "n8n"
    
    # Aguarda 5 segundos
    sleep 5
    
    # Verifica se ainda está rodando
    N8N_PIDS=$(pgrep -f "n8n")
    if [ -n "$N8N_PIDS" ]; then
        echo "   Forçando parada com SIGKILL..."
        pkill -KILL -f "n8n"
        sleep 2
    fi
    
    # Verificação final
    N8N_PIDS=$(pgrep -f "n8n")
    if [ -z "$N8N_PIDS" ]; then
        echo "✅ n8n parado com sucesso!"
    else
        echo "❌ Erro ao parar n8n. PIDs ainda ativos: $N8N_PIDS"
        exit 1
    fi
else
    echo "ℹ️  Nenhum processo n8n encontrado"
fi

# Método 2: Verificar porta 5678
if netstat -tlnp 2>/dev/null | grep -q ":5678 "; then
    echo "⚠️  Porta 5678 ainda está em uso"
    echo "   Processos usando a porta:"
    lsof -i :5678 2>/dev/null || netstat -tlnp 2>/dev/null | grep ":5678 "
else
    echo "✅ Porta 5678 liberada"
fi
