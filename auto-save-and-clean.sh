#!/bin/bash

# Script principal de automação - salva tudo e limpa o codespace
# Uso: ./auto-save-and-clean.sh [mensagem-commit-opcional]

echo "🤖 Automação Completa: Salvar + Limpar Codespace"
echo "================================================="

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_step() {
    echo -e "${BLUE}[ETAPA]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCESSO]${NC} $1"
}

log_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

# ETAPA 1: Verificar se os scripts existem
log_step "1/4 - Verificando scripts necessários..."

if [ ! -f "backup-to-github.sh" ]; then
    echo "❌ Script backup-to-github.sh não encontrado!"
    exit 1
fi

if [ ! -f "cleanup-codespace.sh" ]; then
    echo "❌ Script cleanup-codespace.sh não encontrado!"
    exit 1
fi

# Tornar scripts executáveis
chmod +x backup-to-github.sh
chmod +x cleanup-codespace.sh

log_success "Scripts encontrados e configurados"

# ETAPA 2: Mostrar resumo do que será salvo
log_step "2/4 - Analisando arquivos do projeto..."

echo "📁 Estrutura atual do projeto:"
echo "   - Arquivos principais: $(find . -maxdepth 1 -name "*.ts" -o -name "*.js" -o -name "*.json" -o -name "*.md" | wc -l)"
echo "   - Credenciais: $(find credentials/ -name "*.ts" 2>/dev/null | wc -l || echo "0")"
echo "   - Nodes: $(find nodes/ -name "*.ts" 2>/dev/null | wc -l || echo "0")"
echo "   - Tamanho total: $(du -sh . 2>/dev/null | cut -f1)"

# ETAPA 3: Fazer backup completo
log_step "3/4 - Executando backup para GitHub..."

if [ -n "$1" ]; then
    log_info "Usando mensagem personalizada: '$1'"
    ./backup-to-github.sh "$1"
else
    log_info "Usando mensagem automática"
    ./backup-to-github.sh
fi

if [ $? -eq 0 ]; then
    log_success "Backup realizado com sucesso!"
else
    echo "❌ Erro no backup. Abortando limpeza por segurança."
    exit 1
fi

# ETAPA 4: Limpar codespace
log_step "4/4 - Limpando Codespace..."

# Perguntar se quer mesmo limpar
read -p "🤔 Deseja limpar arquivos temporários? (y/N): " -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ./cleanup-codespace.sh
    log_success "Limpeza concluída!"
else
    log_info "Limpeza cancelada pelo usuário"
fi

echo ""
echo "🎉 AUTOMAÇÃO CONCLUÍDA!"
echo "======================"
echo "✅ Todos os arquivos importantes foram salvos no GitHub"
echo "✅ Codespace otimizado para melhor performance"
echo ""
echo "📋 Para usar novamente:"
echo "   ./auto-save-and-clean.sh"
echo "   ./auto-save-and-clean.sh \"minha mensagem de commit\""
echo ""
echo "🔗 Links úteis:"
echo "   - Ver repositório: git remote get-url origin"
echo "   - Verificar status: git status"
echo "   - Instalar dependências: npm install"
