# Como Publicar no GitHub

## Passo 0: Testar o Node Localmente no n8n

### ⚠️ IMPORTANTE: Para GitHub Codespaces

Se você está usando GitHub Codespaces (como indicado pela URL: `opulent-waffle-5g95x97v74xxh7ppp-5678.app.github.dev`), você **NÃO** pode usar caminhos de arquivo locais. Você precisa usar uma URL do GitHub.

### 🚀 Solução Rápida para Codespaces:

1. **Crie um repositório no GitHub PRIMEIRO:**
   - Vá para https://github.com
   - Clique em "New repository"
   - Nome: `n8n-nodes-google-ai`
   - Marque como **público**
   - **NÃO** inicialize com README

2. **Publique o código:**
   ```bash
   git remote add origin https://github.com/SEUUSERNAME/n8n-nodes-google-ai.git
   git push -u origin main
   ```

3. **No n8n, use a URL do GitHub:**
   - Vá para: Settings → Community Nodes
   - No campo "npm package name", use:
   ```
   https://github.com/SEUUSERNAME/n8n-nodes-google-ai.git
   ```

### Método 1: Instalar diretamente da pasta local (NÃO funciona no Codespaces)

```bash
# Navegue até a pasta do seu projeto n8n-nodes-google-ai
cd /workspaces/codespaces-blank

# Gere um pacote local
npm pack

# Isso criará um arquivo como n8n-nodes-google-ai-1.0.0.tgz
```

No n8n (localhost), use o caminho completo para o arquivo `.tgz`:
- Nome do pacote: `/workspaces/codespaces-blank/n8n-nodes-google-ai-1.0.0.tgz`

### Método 2: Usar npm link (Recomendado para desenvolvimento)

```bash
# Na pasta do seu projeto
npm link

# No diretório do n8n (se você tem acesso)
npm link n8n-nodes-google-ai
```

### Método 3: Instalar via Git (Após publicar no GitHub)

```bash
# Depois de publicar no GitHub, você pode instalar assim:
npm install https://github.com/SEUUSERNAME/n8n-nodes-google-ai.git
```

No n8n, use: `https://github.com/SEUUSERNAME/n8n-nodes-google-ai.git`

### Método 4: Usar pasta local diretamente

Se você tem acesso ao diretório do n8n:

```bash
# Copie a pasta do projeto para o diretório de nodes do n8n
cp -r /workspaces/codespaces-blank ~/.n8n/nodes/n8n-nodes-google-ai

# Ou crie um link simbólico
ln -s /workspaces/codespaces-blank ~/.n8n/nodes/n8n-nodes-google-ai
```

### ⚠️ Importante: Configuração da API Key

Antes de usar o node, você precisa:

1. Obter uma API Key do Google AI Studio: https://ai.google.dev/
2. No n8n, vá para "Credentials" e crie uma nova credencial "Google AI API"
3. Insira sua API Key

## Passo 1: Criar o Repositório no GitHub

1. Acesse [GitHub](https://github.com)
2. Clique em "New repository"
3. Nome do repositório: `n8n-nodes-google-ai`
4. Descrição: "n8n node for Google AI integration"
5. Marque como **público**
6. NÃO inicialize com README (já temos um)
7. Clique em "Create repository"

## Passo 2: Conectar o Repositório Local ao GitHub

```bash
# Adicionar o remote origin (substitua 'yourusername' pelo seu nome de usuário)
git remote add origin https://github.com/yourusername/n8n-nodes-google-ai.git

# Fazer o push inicial
git branch -M main
git push -u origin main
```

## Passo 3: Configurar NPM (Opcional)

Se você quiser publicar no npm:

```bash
# Fazer login no npm
npm login

# Publicar o pacote
npm publish --access public
```

## Passo 4: Configurar GitHub Actions (Opcional)

Para habilitar CI/CD:

1. Vá para o repositório no GitHub
2. Clique em "Settings"
3. Vá para "Secrets and variables" > "Actions"
4. Adicione um secret chamado `NPM_TOKEN` com seu token do npm

## Passo 5: Atualizar URLs no package.json

Antes de publicar, atualize as URLs no `package.json`:

```json
{
  "homepage": "https://github.com/SEUUSERNAME/n8n-nodes-google-ai",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/SEUUSERNAME/n8n-nodes-google-ai.git"
  },
  "author": {
    "name": "SEU NOME",
    "email": "seu.email@example.com"
  }
}
```

## Comandos Úteis para Desenvolvimento

```bash
# Instalar dependências
npm install

# Compilar o projeto
npm run build

# Modo de desenvolvimento (watch)
npm run dev

# Verificar linting
npm run lint

# Corrigir problemas de linting
npm run lintfix

# Formatar código
npm run format
```

## Estrutura do Projeto

```
n8n-nodes-google-ai/
├── .github/                 # Templates e workflows do GitHub
├── credentials/             # Credenciais do n8n
├── nodes/                   # Nodes do n8n
│   └── GoogleAi/           # Node do Google AI
├── dist/                    # Arquivos compilados
├── package.json            # Configuração do projeto
├── tsconfig.json           # Configuração do TypeScript
├── .eslintrc.json          # Configuração do ESLint
├── .prettierrc.json        # Configuração do Prettier
├── gulpfile.js             # Build dos ícones
├── README.md               # Documentação
├── LICENSE                 # Licença MIT
├── CHANGELOG.md            # Registro de mudanças
├── CONTRIBUTING.md         # Guia de contribuição
└── SECURITY.md             # Política de segurança
```

## Próximos Passos

1. Teste o node em uma instância n8n
2. Documente exemplos de uso
3. Adicione testes unitários
4. Melhore a documentação
5. Adicione suporte a mais modelos Google AI
6. Implemente funcionalidades de chat mais avançadas
