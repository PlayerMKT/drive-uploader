# 🚀 Como Clonar Este Codespace Completo

Este repositório inclui um sistema automatizado para capturar e replicar **TODO** o ambiente de desenvolvimento, incluindo dependências, configurações e instalações.

## ⚡ Uso Rápido

### Para Exportar o Ambiente Atual:
```bash
npm run env:export
```

### Para Clonar em Novo Ambiente:
```bash
# 1. Baixe o arquivo .tar.gz gerado
# 2. Extraia:
tar -xzf n8n-google-ai-environment-*.tar.gz
cd n8n-google-ai-node/

# 3. Restaure tudo:
npm run env:restore
```

## 📋 Scripts NPM Disponíveis

```bash
# Gerenciamento de Ambiente
npm run env:manage    # Interface interativa completa
npm run env:capture   # Capturar ambiente atual
npm run env:export    # Exportar ambiente completo
npm run env:restore   # Restaurar ambiente
npm run env:sync      # Sincronizar ambiente

# Desenvolvimento
npm run dev           # Modo desenvolvimento (watch)
npm run build         # Build de produção
npm run lint          # Verificar código
npm run format        # Formatar código

# n8n
npm run n8n:start     # Iniciar n8n
npm run n8n:env       # Carregar variáveis
npm run n8n:config    # Ver configuração
```

## 🎯 Interface Interativa (Recomendado)

```bash
npm run env:manage
```

**Menu disponível:**
- 📊 Status do ambiente
- 📸 Capturar ambiente
- 🔄 Restaurar/Sincronizar
- 📦 Exportar tudo
- 🛠️ Instalar dependências
- 🏗️ Build do projeto
- 🚀 Iniciar desenvolvimento
- 🧹 Limpar e rebuild

## 🐳 Usando Docker (Alternativa)

```bash
# Desenvolvimento
docker-compose up n8n-google-ai-dev

# Produção  
docker-compose up n8n-google-ai-prod
```

## 📦 O que é Capturado

✅ **Sistema:**
- Versões Node.js, npm, nvm
- Variáveis de ambiente
- Configurações shell

✅ **Dependências:**
- Pacotes npm globais
- package.json + package-lock.json
- Pacotes Python
- Extensões VS Code

✅ **Configurações:**
- TypeScript, ESLint, Prettier
- Gulp, n8n configs
- Histórico de comandos

## 🔄 Fluxo de Trabalho

### 1. Desenvolvendo Localmente
```bash
git clone [repo]
npm run env:restore    # Restaurar ambiente
npm run dev           # Desenvolver
```

### 2. Salvando Mudanças
```bash
npm run env:capture   # Capturar mudanças
git add . && git commit -m "..."
git push
```

### 3. Compartilhando Ambiente
```bash
npm run env:export    # Gerar .tar.gz
# Compartilhar arquivo gerado
```

### 4. Novo Codespace/Máquina
```bash
# Extrair arquivo compartilhado
tar -xzf n8n-google-ai-environment-*.tar.gz
cd n8n-google-ai-node/
npm run env:restore   # Restaurar tudo
```

## 🆘 Solução de Problemas

### Build falhando?
```bash
npm run env:manage
# Escolher opção 9 (Limpar Cache e Rebuild)
```

### Dependências faltando?
```bash
npm run env:sync      # Verificar diferenças
npm run env:restore   # Restaurar tudo
```

### Ambiente diferente?
```bash
npm run env:capture   # Atualizar captura
npm run env:export    # Gerar novo export
```

## 📁 Arquivos Importantes

- `.codespace-config/` - Todas as configurações capturadas
- `Dockerfile` + `docker-compose.yml` - Containerização
- `ENVIRONMENT_GUIDE.md` - Documentação completa
- Scripts `*.sh` - Automação do ambiente

## 🎯 Casos de Uso

**✅ Novo desenvolvedor no time:**
1. Recebe arquivo `.tar.gz`
2. Executa `npm run env:restore`
3. Ambiente idêntico funcionando

**✅ Mudança de máquina:**
1. `npm run env:export` na máquina antiga
2. `npm run env:restore` na nova
3. Desenvolvimento continua sem interrupção

**✅ CI/CD:**
1. Docker images prontos
2. Ambiente reproduzível
3. Deploy automatizado

**✅ Backup de ambiente:**
1. `npm run env:export` regularmente
2. Versioning de ambientes
3. Rollback rápido se necessário

---

💡 **Dica:** Use `npm run env:manage` para interface amigável com todas as opções!
