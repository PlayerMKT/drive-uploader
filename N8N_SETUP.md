# Configuração Automática do n8n

Este projeto inclui scripts e configurações para facilitar o uso do n8n no GitHub Codespaces.

## Arquivos de Configuração

### `.env`
Contém todas as variáveis de ambiente necessárias para o n8n:
- `N8N_HOST=0.0.0.0` - Permite acesso externo
- `N8N_PORT=5678` - Porta do servidor
- `WEBHOOK_URL` - URL pública para webhooks
- `N8N_EDITOR_BASE_URL` - URL base do editor

### `start-n8n.sh`
Script completo que:
- Carrega as variáveis do arquivo `.env`
- Para instâncias anteriores do n8n
- Inicia o n8n com as configurações corretas
- Verifica se o serviço está funcionando

### `load-n8n-env.sh`
Script simples para carregar apenas as variáveis de ambiente.

## Como Usar

### Opção 1: Script Completo (Recomendado)
```bash
./start-n8n.sh
```

### Opção 2: Via npm
```bash
npm run n8n:start
```

### Opção 3: Carregar apenas variáveis
```bash
source ./load-n8n-env.sh
n8n start
```

### Opção 4: Carregar do .env
```bash
export $(cat .env | xargs)
n8n start
```

## Scripts npm Disponíveis

- `npm run n8n:start` - Inicia o n8n com configurações
- `npm run n8n:env` - Carrega variáveis de ambiente
- `npm run n8n:config` - Mostra configurações atuais

## Variáveis Automáticas

As variáveis também foram adicionadas ao `~/.bashrc`, então estarão disponíveis automaticamente em novas sessões do terminal.

## URLs de Acesso

- **Editor n8n**: https://opulent-waffle-5g95x97v74xxh7ppp-5678.app.github.dev
- **Webhooks**: Mesma URL base + `/webhook/[seu-webhook-id]`

## Notas Importantes

1. As URLs do GitHub Codespaces mudam a cada reinicialização do ambiente
2. Se precisar atualizar as URLs, edite o arquivo `.env` e recarregue as variáveis
3. O script `start-n8n.sh` sempre para instâncias anteriores antes de iniciar uma nova
