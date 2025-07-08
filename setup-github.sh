#!/bin/bash

# Script para configurar o repositório GitHub
# Uso: ./setup-github.sh [usuario] [nome-do-repo]

echo "🔧 Configuração do Repositório GitHub"
echo "====================================="

# Verificar configuração atual
echo "📋 Configuração atual:"
echo "   Remote atual: $(git remote get-url origin 2>/dev/null || echo "Não configurado")"
echo "   Branch atual: $(git branch --show-current)"
echo ""

# Se parâmetros foram fornecidos, configurar automaticamente
if [ -n "$1" ] && [ -n "$2" ]; then
    USUARIO="$1"
    REPO="$2"
    NEW_URL="https://github.com/$USUARIO/$REPO.git"
    
    echo "🚀 Configurando repositório:"
    echo "   Usuário: $USUARIO"
    echo "   Repositório: $REPO"
    echo "   URL: $NEW_URL"
    
    git remote set-url origin "$NEW_URL" 2>/dev/null || git remote add origin "$NEW_URL"
    
    echo "✅ Repositório configurado!"
    echo ""
    echo "📝 Próximos passos:"
    echo "   1. Crie o repositório no GitHub: https://github.com/new"
    echo "   2. Nome do repositório: $REPO"
    echo "   3. Execute: ./backup-to-github.sh"
    
else
    echo "💡 Uso:"
    echo "   ./setup-github.sh SEU_USUARIO NOME_DO_REPO"
    echo ""
    echo "📝 Exemplo:"
    echo "   ./setup-github.sh EngThi n8n-google-ai-node"
    echo ""
    echo "🔧 Ou configure manualmente:"
    echo "   git remote set-url origin https://github.com/SEU_USUARIO/SEU_REPO.git"
fi

echo ""
echo "🌐 Para criar o repositório no GitHub:"
echo "   https://github.com/new"
