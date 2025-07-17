#!/bin/bash

# Export Environment Script
# Exporta o ambiente para um arquivo compactado

set -e

echo "📦 Exportando ambiente para arquivo compactado..."

# Função para logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Capturar ambiente primeiro
log "Capturando ambiente atual..."
./capture-environment.sh

# Criar nome do arquivo com timestamp
timestamp=$(date +"%Y%m%d_%H%M%S")
export_file="n8n-google-ai-environment-${timestamp}.tar.gz"

# Preparar arquivos para exportação
log "Preparando arquivos para exportação..."

# Criar lista de arquivos importantes
files_to_export=(
    "package.json"
    "package-lock.json"
    "tsconfig.json"
    "gulpfile.js"
    ".gitignore"
    "README.md"
    "LICENSE"
    "nodes/"
    "credentials/"
    ".codespace-config/"
    "*.sh"
    "*.md"
    "*.json"
)

# Criar arquivo temporário com lista de arquivos
temp_list=$(mktemp)

# Verificar quais arquivos existem
for pattern in "${files_to_export[@]}"; do
    if ls $pattern >/dev/null 2>&1; then
        echo "$pattern" >> "$temp_list"
    fi
done

# Criar arquivo compactado
log "Criando arquivo compactado: $export_file"
tar -czf "$export_file" -T "$temp_list" 2>/dev/null || {
    # Fallback: incluir arquivos um por um
    tar -czf "$export_file" \
        --exclude='node_modules' \
        --exclude='dist' \
        --exclude='.git' \
        --exclude='*.tar.gz' \
        . 2>/dev/null || echo "Alguns arquivos podem não ter sido incluídos"
}

# Limpar arquivo temporário
rm -f "$temp_list"

# Criar arquivo de instruções
log "Criando arquivo de instruções..."
cat > "IMPORT_INSTRUCTIONS_${timestamp}.txt" << EOF
# Instruções para Importar o Ambiente

## Arquivo: $export_file

### Como Usar:

1. **Extrair o arquivo:**
   \`\`\`bash
   tar -xzf $export_file
   cd n8n-google-ai-node/ # ou o diretório extraído
   \`\`\`

2. **Restaurar o ambiente:**
   \`\`\`bash
   chmod +x *.sh
   ./restore-environment.sh
   \`\`\`

3. **Verificar instalação:**
   \`\`\`bash
   node --version
   npm --version
   npm run build
   \`\`\`

### Conteúdo do Arquivo:
- Código fonte completo do projeto
- Configurações do ambiente (.codespace-config/)
- Scripts de instalação e sincronização
- Dependências e configurações

### Requisitos:
- Node.js (será instalado automaticamente se não estiver presente)
- npm (vem com Node.js)
- Git (para clonar dependências)

### Solução de Problemas:
- Se o script automático falhar, consulte .codespace-config/README.md
- Para instalação manual, veja os arquivos em .codespace-config/
- Execute './sync-environment.sh' para verificar diferenças

Data de Criação: $(date)
Sistema Original: $(uname -a)
Node.js: $(node --version 2>/dev/null || echo "Não encontrado")
npm: $(npm --version 2>/dev/null || echo "Não encontrado")
EOF

# Mostrar informações sobre o export
log "Calculando tamanho do arquivo..."
file_size=$(du -h "$export_file" | cut -f1)

echo ""
echo "=== Exportação Concluída ==="
echo "📦 Arquivo criado: $export_file"
echo "📏 Tamanho: $file_size"
echo "📋 Instruções: IMPORT_INSTRUCTIONS_${timestamp}.txt"
echo ""
echo "✅ Para importar em outro ambiente:"
echo "   1. Copie o arquivo $export_file"
echo "   2. Execute: tar -xzf $export_file"
echo "   3. Execute: ./restore-environment.sh"
echo ""
echo "📋 Arquivos criados:"
ls -la "$export_file" "IMPORT_INSTRUCTIONS_${timestamp}.txt"
