# Configuração do Ambiente Capturada

Este diretório contém todas as configurações e dependências capturadas do ambiente original.

## Arquivos Capturados

- `system-info.txt` - Informações do sistema operacional
- `tool-versions.txt` - Versões das ferramentas instaladas
- `npm-global-packages.json` - Pacotes npm globais (formato JSON)
- `npm-global-packages.txt` - Pacotes npm globais (formato texto)
- `node-config.txt` - Configuração do Node.js
- `environment-variables.txt` - Variáveis de ambiente importantes
- `vscode-extensions.txt` - Extensões do VS Code instaladas
- `python-requirements.txt` - Pacotes Python instalados
- `recent-commands.txt` - Comandos recentes do terminal
- `install-environment.sh` - Script de instalação automática

## Como Usar

1. Clone este repositório
2. Execute o script de instalação:
   ```bash
   chmod +x .codespace-config/install-environment.sh
   ./.codespace-config/install-environment.sh
   ```

3. Verifique se tudo foi instalado corretamente:
   ```bash
   node --version
   npm --version
   npm run build
   ```

## Restauração Manual

Se o script automático falhar, você pode instalar manualmente:

### Node.js e npm
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install node
```

### Dependências do Projeto
```bash
npm install
```

### Pacotes Globais
Consulte `npm-global-packages.txt` para a lista completa.

### Extensões VS Code
Consulte `vscode-extensions.txt` para a lista completa.

