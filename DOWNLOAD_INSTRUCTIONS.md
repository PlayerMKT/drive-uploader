# 📦 Como Baixar e Fazer Upload dos Arquivos

## 📥 Download dos Arquivos

O arquivo `n8n-nodes-google-ai-files.zip` contém todos os arquivos do projeto.

**Para baixar:**
1. No VS Code, vá para o Explorer (painel esquerdo)
2. Localize o arquivo `n8n-nodes-google-ai-files.zip`
3. Clique com o botão direito no arquivo
4. Selecione "Download"

## 📤 Upload para o GitHub

### Opção 1: Upload via Interface Web
1. Vá para https://github.com/EngThi/n8n-nodes-google-ai
2. Clique em "Add file" → "Upload files"
3. Extraia o arquivo zip no seu computador
4. Arraste todos os arquivos e pastas para o GitHub
5. Escreva uma mensagem de commit: "Initial upload of n8n Google AI node"
6. Clique em "Commit changes"

### Opção 2: Upload do ZIP diretamente
1. Vá para https://github.com/EngThi/n8n-nodes-google-ai
2. Clique em "Add file" → "Upload files"
3. Arraste o arquivo `n8n-nodes-google-ai-files.zip`
4. Depois extraia no próprio GitHub ou localmente

## 🎯 Após o Upload

### Instalar no n8n:
1. Vá para o n8n: Settings → Community Nodes
2. No campo "npm package name", use:
   ```
   https://github.com/EngThi/n8n-nodes-google-ai.git
   ```
3. Clique em "Install"

### Configurar Credenciais:
1. Obtenha uma API Key em: https://ai.google.dev/
2. No n8n: Credentials → Add Credential → Google AI API
3. Insira sua API Key

## 📋 Estrutura dos Arquivos

```
n8n-nodes-google-ai/
├── package.json          # Configuração do projeto
├── README.md             # Documentação
├── tsconfig.json         # Configuração TypeScript
├── gulpfile.js           # Build dos ícones
├── .eslintrc.json        # Configuração ESLint
├── .prettierrc.json      # Configuração Prettier
├── .gitignore            # Arquivos ignorados pelo Git
├── LICENSE               # Licença MIT
├── CHANGELOG.md          # Histórico de mudanças
├── CONTRIBUTING.md       # Guia de contribuição
├── SECURITY.md           # Política de segurança
├── nodes/                # Código fonte do node
│   └── GoogleAi/
│       ├── GoogleAi.node.ts
│       └── googleai.svg
├── credentials/          # Credenciais
│   └── GoogleAiApi.credentials.ts
├── dist/                 # Arquivos compilados
├── .github/              # Templates GitHub
│   ├── workflows/
│   │   └── ci.yml
│   ├── ISSUE_TEMPLATE/
│   ├── copilot-instructions.md
│   └── pull_request_template.md
└── .vscode/              # Configurações VS Code
    └── tasks.json
```

## 🚀 Teste Final

Após instalar no n8n, teste com este prompt:
```
Escreva um resumo sobre inteligência artificial em 3 parágrafos
```

## ❓ Problemas?

Se houver problemas na instalação:
1. Verifique se o repositório está público
2. Tente usar a URL: `git+https://github.com/EngThi/n8n-nodes-google-ai.git`
3. Reinicie o n8n após a instalação
