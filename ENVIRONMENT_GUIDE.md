# Ambiente N8N Google AI - Documentação Completa

Este projeto inclui um sistema completo para capturar, salvar e replicar todo o ambiente de desenvolvimento, incluindo todas as dependências, configurações e instalações.

## 🚀 Scripts de Gerenciamento de Ambiente

### Scripts Principais

1. **`./manage-environment.sh`** - Interface interativa completa
2. **`./capture-environment.sh`** - Captura o ambiente atual
3. **`./restore-environment.sh`** - Restaura ambiente capturado
4. **`./sync-environment.sh`** - Sincroniza ambiente
5. **`./export-environment.sh`** - Exporta ambiente completo

### Uso Rápido

```bash
# Interface interativa (recomendado)
./manage-environment.sh

# Ou comandos diretos
./capture-environment.sh  # Capturar ambiente atual
./export-environment.sh   # Exportar para arquivo .tar.gz
```

## 📦 O que é Capturado

### Informações do Sistema
- Versões do Node.js, npm, nvm
- Variáveis de ambiente importantes
- Configurações do shell (bashrc, profile)
- Informações do sistema operacional

### Dependências
- Pacotes npm globais instalados
- Dependências do projeto (package.json, package-lock.json)
- Pacotes Python (se disponível)
- Extensões do VS Code

### Configurações
- Arquivos de configuração do projeto
- Histórico de comandos recentes
- Configurações do Node.js e npm

## 🔄 Como Replicar o Ambiente

### Método 1: Usando o Exportador (Recomendado)

1. **No ambiente original:**
   ```bash
   ./export-environment.sh
   ```

2. **No novo ambiente:**
   ```bash
   # Extrair arquivo
   tar -xzf n8n-google-ai-environment-YYYYMMDD_HHMMSS.tar.gz
   cd n8n-google-ai-node/
   
   # Restaurar ambiente
   chmod +x *.sh
   ./restore-environment.sh
   ```

### Método 2: Clone do Repositório

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/EngThi/n8n-google-ai-node.git
   cd n8n-google-ai-node
   ```

2. **Restaurar ambiente:**
   ```bash
   chmod +x *.sh
   ./restore-environment.sh
   ```

### Método 3: Docker (Mais Portável)

```bash
# Desenvolvimento
docker-compose up n8n-google-ai-dev

# Produção
docker-compose up n8n-google-ai-prod
```

## 🛠️ Estrutura dos Arquivos Capturados

```
.codespace-config/
├── README.md                    # Documentação da configuração
├── install-environment.sh       # Script de instalação automática
├── system-info.txt             # Informações do sistema
├── tool-versions.txt           # Versões das ferramentas
├── npm-global-packages.json    # Pacotes globais (JSON)
├── npm-global-packages.txt     # Pacotes globais (texto)
├── node-config.txt             # Configuração do Node.js
├── environment-variables.txt   # Variáveis de ambiente
├── vscode-extensions.txt       # Extensões do VS Code
├── python-requirements.txt     # Pacotes Python
├── recent-commands.txt         # Comandos recentes
├── package-lock.json          # Lock file do projeto
├── bashrc-backup              # Backup do .bashrc
├── profile-backup             # Backup do .profile
└── [outros arquivos de config]
```

## 🔍 Verificação do Ambiente

### Status Automático
```bash
./sync-environment.sh
```

### Verificação Manual
```bash
# Verificar versões
node --version
npm --version

# Verificar pacotes globais
npm list -g --depth=0

# Testar build
npm run build

# Testar desenvolvimento
npm run dev
```

## 🚨 Solução de Problemas

### Problema: Node.js não instalado
```bash
# Instalar via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 22.16.0
nvm use 22.16.0
```

### Problema: Dependências faltando
```bash
# Limpar e reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Problema: Build falhando
```bash
# Rebuild completo
./manage-environment.sh
# Escolher opção 9 (Limpar Cache e Rebuild)
```

### Problema: Pacotes globais faltando
```bash
# Consultar lista capturada
cat .codespace-config/npm-global-packages.txt

# Instalar manualmente
npm install -g n8n pnpm
```

## 📋 Comandos Úteis

### Desenvolvimento
```bash
npm run dev          # Modo desenvolvimento (watch)
npm run build        # Build de produção
npm run lint         # Verificar código
npm run format       # Formatar código
```

### n8n Específicos
```bash
npm run n8n:start    # Iniciar n8n
npm run n8n:env      # Carregar variáveis de ambiente
npm run n8n:config   # Mostrar configuração
```

### Ambiente
```bash
./manage-environment.sh    # Interface completa
./capture-environment.sh   # Capturar estado atual
./export-environment.sh    # Exportar tudo
```

## 🐳 Docker

### Desenvolvimento
```bash
docker-compose up n8n-google-ai-dev
```

### Produção
```bash
docker-compose up n8n-google-ai-prod
```

### Build Manual
```bash
docker build -t n8n-google-ai .
docker run -p 5678:5678 n8n-google-ai
```

## 📁 Arquivos Importantes

- `package.json` - Dependências e scripts
- `tsconfig.json` - Configuração TypeScript
- `gulpfile.js` - Build system
- `nodes/` - Nós do n8n
- `credentials/` - Credenciais do n8n
- `.codespace-config/` - Configuração capturada

## ✅ Lista de Verificação para Nova Instalação

- [ ] Node.js 22.16.0 instalado
- [ ] npm funcionando
- [ ] Dependências do projeto instaladas (`npm install`)
- [ ] Build executando sem erros (`npm run build`)
- [ ] Pacotes globais instalados (n8n, pnpm)
- [ ] Configurações restauradas
- [ ] Testes passando

## 🤝 Contribuição

1. Capture o ambiente: `./capture-environment.sh`
2. Faça suas alterações
3. Teste: `npm run build && npm run lint`
4. Exporte: `./export-environment.sh`
5. Commit e push

---

**Criado em:** $(date)
**Ambiente:** Codespaces / Linux
**Node.js:** $(node --version 2>/dev/null || echo "N/A")
**npm:** $(npm --version 2>/dev/null || echo "N/A")
