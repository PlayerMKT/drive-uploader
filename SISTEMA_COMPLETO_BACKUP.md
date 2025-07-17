# Sistema Completo de Backup e Clonagem do Codespace

## 🎯 Objetivo
Este sistema permite capturar, exportar e replicar completamente o ambiente do seu Codespace, incluindo todas as dependências, configurações e ferramentas instaladas.

## 📁 Arquivos do Sistema

### Scripts Principais
- `capture-environment.sh` - Captura todas as configurações do ambiente atual
- `export-environment.sh` - Cria arquivo compactado para transferência
- `restore-environment.sh` - Restaura ambiente a partir de backup
- `manage-environment.sh` - Interface interativa para gerenciar o ambiente
- `sync-environment.sh` - Sincroniza ambiente com configurações salvas

### Scripts de Automação
- `auto-save-and-clean.sh` - Backup automático e limpeza
- `backup-to-github.sh` - Backup para repositório GitHub
- `setup-github.sh` - Configuração inicial do GitHub

## 🚀 Como Usar

### 1. Capturar Ambiente Atual
```bash
# Método 1: Script direto
./capture-environment.sh

# Método 2: Via npm
npm run env:capture

# Método 3: Menu interativo
npm run env:manage
# Escolha opção 2
```

### 2. Exportar para Arquivo Portátil
```bash
# Método 1: Script direto
./export-environment.sh

# Método 2: Via npm
npm run env:export

# Método 3: Menu interativo
npm run env:manage
# Escolha opção 5
```

### 3. Clonar em Novo Ambiente

#### Opção A: A partir de arquivo compactado
```bash
# 1. Transfira o arquivo .tar.gz para o novo ambiente
# 2. Extraia o arquivo
tar -xzf n8n-google-ai-environment-YYYYMMDD_HHMMSS.tar.gz

# 3. Execute a restauração
./restore-environment.sh
```

#### Opção B: A partir do repositório GitHub
```bash
# 1. Clone o repositório
git clone https://github.com/EngThi/n8n-google-ai-node.git
cd n8n-google-ai-node

# 2. Execute a instalação automática
./.codespace-config/install-environment.sh
```

### 4. Menu Interativo Completo
```bash
npm run env:manage
```

Opções disponíveis:
1. 📊 Mostrar Status do Ambiente
2. 📸 Capturar Ambiente Atual
3. 🔄 Restaurar Ambiente
4. 🔄 Sincronizar Ambiente
5. 📦 Exportar Ambiente Completo
6. 🛠️ Instalar Dependências do Projeto
7. 🏗️ Executar Build
8. 🚀 Iniciar Servidor de Desenvolvimento
9. 🧹 Limpar Cache e Rebuild
0. ❌ Sair

## 📋 O Que é Capturado

### Informações do Sistema
- Versões do Node.js, npm, Python, Git
- Configurações do sistema operacional
- Variáveis de ambiente importantes

### Dependências
- Pacotes npm globais e locais
- Package.json e package-lock.json
- Pacotes Python (requirements.txt)
- Extensões do VS Code

### Configurações
- Arquivos de configuração (.eslintrc, .prettierrc, tsconfig.json, etc.)
- Configurações do bash (.bashrc, .profile)
- Histórico de comandos recentes

### Scripts Automatizados
- Script de instalação automática
- Instruções detalhadas de uso
- Verificações de integridade

## 🔧 Comandos Rápidos

```bash
# Verificar status atual
npm run env:manage

# Backup completo rápido
npm run env:export

# Restaurar último backup
npm run env:restore

# Sincronizar com configurações
npm run env:sync

# Iniciar desenvolvimento
npm run dev

# Build do projeto
npm run build
```

## 📦 Arquivos Gerados

### .codespace-config/
- `system-info.txt` - Informações do sistema
- `tool-versions.txt` - Versões das ferramentas
- `npm-global-packages.json` - Pacotes npm globais
- `python-requirements.txt` - Dependências Python
- `vscode-extensions.txt` - Extensões VS Code
- `install-environment.sh` - Script de instalação
- `README.md` - Instruções detalhadas

### Arquivos de Export
- `n8n-google-ai-environment-YYYYMMDD_HHMMSS.tar.gz` - Ambiente compactado
- `IMPORT_INSTRUCTIONS_YYYYMMDD_HHMMSS.txt` - Instruções de importação

## 🎯 Casos de Uso

### Desenvolvedor Individual
1. Capture o ambiente: `npm run env:capture`
2. Exporte para arquivo: `npm run env:export`
3. Guarde o arquivo .tar.gz como backup

### Equipe de Desenvolvimento
1. Capture e commite as configurações no Git
2. Outros membros executam: `git pull && npm run env:restore`
3. Todos ficam com ambiente idêntico

### Migração de Ambiente
1. No ambiente antigo: `npm run env:export`
2. Transfira o arquivo .tar.gz
3. No novo ambiente: `tar -xzf arquivo.tar.gz && ./restore-environment.sh`

### CI/CD Pipeline
1. Use os scripts para garantir ambiente consistente
2. Dockerize com base nas configurações capturadas

## 🛠️ Troubleshooting

### Problemas Comuns

#### Script não executa
```bash
chmod +x *.sh
```

#### Dependências faltando
```bash
npm run env:manage
# Escolha opção 6 (Instalar Dependências)
```

#### Build falha
```bash
npm run env:manage
# Escolha opção 9 (Limpar Cache e Rebuild)
```

#### Ambiente inconsistente
```bash
npm run env:restore
```

## 🔒 Segurança

- ⚠️ **NÃO** inclua secrets ou tokens nos backups
- ✅ Use variáveis de ambiente para dados sensíveis
- ✅ Revise arquivos antes de compartilhar
- ✅ Use .gitignore para arquivos sensíveis

## 📚 Recursos Adicionais

- `CLONE_GUIDE.md` - Guia detalhado de clonagem
- `ENVIRONMENT_GUIDE.md` - Guia de configuração de ambiente
- `AUTOMATION_GUIDE.md` - Guia de automação
- `CONTRIBUTING.md` - Guia de contribuição

## 🎉 Resultado

Com este sistema você pode:
- ✅ Clonar perfeitamente qualquer Codespace
- ✅ Compartilhar ambientes com a equipe
- ✅ Fazer backup completo do desenvolvimento
- ✅ Migrar entre diferentes plataformas
- ✅ Automatizar setup de novos ambientes
- ✅ Manter consistência entre todos os desenvolvedores

---

**🚀 Agora você tem controle total sobre seus ambientes de desenvolvimento!**
