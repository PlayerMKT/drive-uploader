#!/bin/bash

# Script para criar repositório GitHub automaticamente
# Requer gh CLI ou orientações manuais

echo "🌐 Criação do Repositório GitHub"
echo "================================"

REPO_USER="EngThi"
REPO_NAME="n8n-google-ai-node"
REPO_URL="https://github.com/$REPO_USER/$REPO_NAME.git"

echo "📋 Informações do repositório:"
echo "   Usuário: $REPO_USER"
echo "   Nome: $REPO_NAME"
echo "   URL: $REPO_URL"
echo ""

# Verificar se gh CLI está disponível
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI encontrado! Tentando criar repositório automaticamente..."
    
    # Criar repositório usando gh CLI
    gh repo create "$REPO_NAME" \
        --public \
        --description "n8n custom node for Google AI integration (Gemini)" \
        --add-readme=false \
        --clone=false
    
    if [ $? -eq 0 ]; then
        echo "🎉 Repositório criado com sucesso!"
        echo ""
        echo "🚀 Fazendo primeiro push..."
        git push -u origin main
        
        if [ $? -eq 0 ]; then
            echo "✅ Código enviado para GitHub com sucesso!"
            echo "🌐 Acesse: https://github.com/$REPO_USER/$REPO_NAME"
        else
            echo "⚠️ Repositório criado, mas push falhou. Tente manualmente:"
            echo "   git push -u origin main"
        fi
    else
        echo "❌ Falha ao criar repositório automaticamente"
        echo "📋 Crie manualmente seguindo as instruções abaixo:"
    fi
else
    echo "⚠️ GitHub CLI não encontrado"
    echo "📋 Siga as instruções manuais abaixo:"
fi

echo ""
echo "📋 INSTRUÇÕES MANUAIS (se necessário):"
echo "======================================"
echo ""
echo "1. 🌐 Acesse: https://github.com/new"
echo ""
echo "2. 📝 Preencha os dados:"
echo "   - Repository name: $REPO_NAME"
echo "   - Description: n8n custom node for Google AI integration (Gemini)"
echo "   - Visibility: Public ✅"
echo "   - Initialize repository: NÃO marque nenhuma opção ❌"
echo ""
echo "3. 🚀 Clique em 'Create repository'"
echo ""
echo "4. 💾 Execute este comando para enviar o código:"
echo "   git push -u origin main"
echo ""
echo "5. ✅ Verifique se funcionou:"
echo "   ./backup-to-github.sh 'Repositório configurado!'"
echo ""
echo "🔗 Links úteis:"
echo "   - Criar repo: https://github.com/new"
echo "   - Seu perfil: https://github.com/$REPO_USER"
echo "   - Repositório: https://github.com/$REPO_USER/$REPO_NAME"
