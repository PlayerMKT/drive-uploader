# 📚 Guia Completo: Criando um Node n8n para Google AI

## 🎯 Objetivo
Criar um node personalizado para n8n que integra com Google AI (Gemini) e publicar no GitHub.

---

## 📋 Índice
1. [Configuração Inicial](#configuração-inicial)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Implementação do Node](#implementação-do-node)
4. [Configuração de Credenciais](#configuração-de-credenciais)
5. [Build e Compilação](#build-e-compilação)
6. [Publicação no GitHub](#publicação-no-github)
7. [Instalação no n8n](#instalação-no-n8n)
8. [Solução de Problemas](#solução-de-problemas)
9. [Estrutura Final](#estrutura-final)

---

## 1. Configuração Inicial

### 📦 Package.json
```json
{
  "name": "n8n-nodes-google-ai",
  "version": "1.0.0",
  "description": "n8n node for Google AI integration",
  "license": "MIT",
  "homepage": "https://github.com/EngThi/n8n-nodes-google-ai",
  "author": {
    "name": "EngThi",
    "email": "engthi@example.com"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/EngThi/n8n-nodes-google-ai.git"
  },
  "main": "index.js",
  "scripts": {
    "build": "tsc && gulp build:icons",
    "dev": "tsc --watch",
    "format": "prettier nodes credentials --write",
    "lint": "eslint nodes credentials package.json",
    "lintfix": "eslint nodes credentials package.json --fix",
    "prepublishOnly": "npm run build && npm run lint -s"
  },
  "files": [
    "dist"
  ],
  "n8n": {
    "n8nNodesApiVersion": 1,
    "credentials": [
      "dist/credentials/GoogleAiApi.credentials.js"
    ],
    "nodes": [
      "dist/nodes/GoogleAi/GoogleAi.node.js"
    ]
  },
  "devDependencies": {
    "@types/node": "^18.16.16",
    "@typescript-eslint/parser": "^5.59.9",
    "eslint": "^8.42.0",
    "eslint-plugin-n8n-nodes-base": "^1.12.1",
    "gulp": "^4.0.2",
    "n8n-workflow": "^1.0.0",
    "prettier": "^2.8.8",
    "typescript": "^5.1.3"
  },
  "peerDependencies": {
    "n8n-workflow": "*"
  },
  "keywords": [
    "n8n-community-node-package",
    "n8n",
    "google-ai",
    "ai",
    "machine-learning"
  ]
}
```

### 🔧 TypeScript Configuration (tsconfig.json)
```json
{
  "compilerOptions": {
    "target": "ES2019",
    "module": "commonjs",
    "lib": ["ES2019"],
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  },
  "include": [
    "credentials/**/*",
    "nodes/**/*"
  ],
  "exclude": [
    "node_modules",
    "dist"
  ]
}
```

### 🔨 Gulp Configuration (gulpfile.js)
```javascript
const { src, dest } = require('gulp');

function buildIcons() {
  return src('nodes/**/*.{png,svg}')
    .pipe(dest('dist/'));
}

exports.build = buildIcons;
exports['build:icons'] = buildIcons;
```

---

## 2. Estrutura do Projeto

### 📁 Estrutura de Pastas
```
n8n-nodes-google-ai/
├── package.json
├── README.md
├── tsconfig.json
├── gulpfile.js
├── .eslintrc.json
├── .prettierrc.json
├── .gitignore
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── nodes/
│   └── GoogleAi/
│       ├── GoogleAi.node.ts
│       └── googleai.svg
├── credentials/
│   └── GoogleAiApi.credentials.ts
├── dist/                 # Arquivos compilados
├── .github/              # Templates GitHub
│   ├── workflows/
│   │   └── ci.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── copilot-instructions.md
│   └── pull_request_template.md
└── .vscode/              # Configurações VS Code
    └── tasks.json
```

---

## 3. Implementação do Node

### 🤖 Node Principal (nodes/GoogleAi/GoogleAi.node.ts)
```typescript
import {
  IExecuteFunctions,
  INodeExecutionData,
  INodeType,
  INodeTypeDescription,
  NodeOperationError,
  NodeConnectionType,
  IHttpRequestMethods,
} from 'n8n-workflow';

export class GoogleAi implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Google AI',
    name: 'googleAi',
    icon: 'file:googleai.svg',
    group: ['transform'],
    version: 1,
    description: 'Interact with Google AI models',
    defaults: {
      name: 'Google AI',
    },
    inputs: ['main'] as NodeConnectionType[],
    outputs: ['main'] as NodeConnectionType[],
    credentials: [
      {
        name: 'googleAiApi',
        required: true,
      },
    ],
    properties: [
      {
        displayName: 'Resource',
        name: 'resource',
        type: 'options',
        noDataExpression: true,
        options: [
          {
            name: 'Generate Content',
            value: 'generateContent',
          },
          {
            name: 'Chat',
            value: 'chat',
          },
        ],
        default: 'generateContent',
      },
      {
        displayName: 'Model',
        name: 'model',
        type: 'options',
        options: [
          {
            name: 'Gemini Pro',
            value: 'gemini-pro',
          },
          {
            name: 'Gemini Pro Vision',
            value: 'gemini-pro-vision',
          },
        ],
        default: 'gemini-pro',
      },
      {
        displayName: 'Prompt',
        name: 'prompt',
        type: 'string',
        typeOptions: {
          rows: 4,
        },
        default: '',
        description: 'The prompt to send to the AI model',
        required: true,
      },
      {
        displayName: 'Temperature',
        name: 'temperature',
        type: 'number',
        typeOptions: {
          minValue: 0,
          maxValue: 1,
          numberStepSize: 0.1,
        },
        default: 0.7,
        description: 'Controls randomness in the output',
      },
      {
        displayName: 'Max Output Tokens',
        name: 'maxOutputTokens',
        type: 'number',
        default: 1000,
        description: 'Maximum number of tokens to generate',
      },
    ],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const returnData: INodeExecutionData[] = [];

    for (let i = 0; i < items.length; i++) {
      try {
        const model = this.getNodeParameter('model', i) as string;
        const prompt = this.getNodeParameter('prompt', i) as string;
        const temperature = this.getNodeParameter('temperature', i) as number;
        const maxOutputTokens = this.getNodeParameter('maxOutputTokens', i) as number;

        const credentials = await this.getCredentials('googleAiApi');
        const apiKey = credentials.apiKey as string;

        const baseUrl = 'https://generativelanguage.googleapis.com/v1beta';
        const url = `${baseUrl}/models/${model}:generateContent`;

        const requestBody = {
          contents: [
            {
              parts: [
                {
                  text: prompt,
                },
              ],
            },
          ],
          generationConfig: {
            temperature,
            maxOutputTokens,
          },
        };

        const options = {
          method: 'POST' as IHttpRequestMethods,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`,
          },
          body: JSON.stringify(requestBody),
        };

        const response = await this.helpers.request(url, options);

        if (response.candidates && response.candidates.length > 0) {
          const generatedText = response.candidates[0].content.parts[0].text;
          
          returnData.push({
            json: {
              prompt,
              response: generatedText,
              model,
              temperature,
              maxOutputTokens,
            },
          });
        } else {
          throw new NodeOperationError(
            this.getNode(),
            'No response generated from Google AI',
          );
        }
      } catch (error) {
        if (this.continueOnFail()) {
          returnData.push({
            json: {
              error: error instanceof Error ? error.message : 'Unknown error',
            },
          });
          continue;
        }
        throw error;
      }
    }

    return [returnData];
  }
}
```

---

## 4. Configuração de Credenciais

### 🔑 Credenciais (credentials/GoogleAiApi.credentials.ts)
```typescript
import {
  IAuthenticateGeneric,
  ICredentialTestRequest,
  ICredentialType,
  INodeProperties,
} from 'n8n-workflow';

export class GoogleAiApi implements ICredentialType {
  name = 'googleAiApi';
  displayName = 'Google AI API';
  documentationUrl = 'https://ai.google.dev/';
  properties: INodeProperties[] = [
    {
      displayName: 'API Key',
      name: 'apiKey',
      type: 'string',
      typeOptions: {
        password: true,
      },
      default: '',
      description: 'API key for Google AI',
    },
  ];

  authenticate: IAuthenticateGeneric = {
    type: 'generic',
    properties: {
      headers: {
        'Authorization': '=Bearer {{$credentials.apiKey}}',
      },
    },
  };

  test: ICredentialTestRequest = {
    request: {
      baseURL: 'https://generativelanguage.googleapis.com/v1beta',
      url: '/models',
      method: 'GET',
    },
  };
}
```

---

## 5. Build e Compilação

### 🛠️ Comandos para Build
```bash
# Instalar dependências
npm install

# Compilar projeto
npm run build

# Modo desenvolvimento (watch)
npm run dev

# Verificar linting
npm run lint

# Formatar código
npm run format
```

### 📝 Configuração ESLint (.eslintrc.json)
```json
{
  "env": {
    "node": true,
    "es2022": true
  },
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended",
    "plugin:n8n-nodes-base/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 2022,
    "sourceType": "module"
  },
  "plugins": [
    "@typescript-eslint",
    "n8n-nodes-base"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": "warn",
    "@typescript-eslint/no-explicit-any": "warn"
  }
}
```

---

## 6. Publicação no GitHub

### 🚀 Processo de Publicação

#### Passo 1: Criar Repositório
1. Vá para https://github.com
2. Clique em "New repository"
3. Nome: `n8n-nodes-google-ai`
4. Descrição: "n8n node for Google AI integration"
5. Marque como **público**
6. **NÃO** inicialize com README

#### Passo 2: Configurar Git Local
```bash
git init
git add .
git commit -m "Initial commit: n8n Google AI node"
git remote add origin https://github.com/EngThi/n8n-nodes-google-ai.git
git push -u origin main
```

#### Passo 3: Problema de Autenticação (Codespaces)
**Problema identificado:** GitHub Codespaces teve problemas de autenticação.

**Solução:** Upload manual dos arquivos.

---

## 7. Instalação no n8n

### 🎯 Processo de Instalação

#### Problema 1: Arquivo .tgz Local
**Erro:** `Package name must start with n8n-nodes-`
**Causa:** n8n no Codespaces não consegue acessar arquivos locais.

#### Solução: URL do GitHub
1. No n8n: Settings → Community Nodes
2. Campo "npm package name": `https://github.com/EngThi/n8n-nodes-google-ai.git`
3. Clique em "Install"

#### Problema 2: Estrutura de Pastas
**Problema:** Arquivos enviados sem estrutura de pastas.
**Solução:** Reorganizar arquivos nas pastas corretas.

### 📁 Estrutura Correta Necessária
```
n8n-nodes-google-ai/
├── package.json
├── nodes/
│   └── GoogleAi/
│       ├── GoogleAi.node.ts
│       └── googleai.svg
├── credentials/
│   └── GoogleAiApi.credentials.ts
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 8. Solução de Problemas

### ❌ Problemas Encontrados

1. **Erro de Compilação TypeScript**
   - Tipos incorretos para inputs/outputs
   - Método HTTP não tipado
   - Tratamento de erro inadequado

2. **Problema de Autenticação Git**
   - Codespaces não conseguiu fazer push
   - Credenciais SSH não configuradas

3. **Estrutura de Arquivos Incorreta**
   - Upload manual não manteve pastas
   - n8n não conseguiu instalar

### ✅ Soluções Implementadas

1. **Correção de Tipos TypeScript**
   ```typescript
   inputs: ['main'] as NodeConnectionType[],
   outputs: ['main'] as NodeConnectionType[],
   method: 'POST' as IHttpRequestMethods,
   error: error instanceof Error ? error.message : 'Unknown error',
   ```

2. **Upload Manual Organizado**
   - Criação de ZIP com estrutura correta
   - Instruções passo a passo para upload

3. **Arquivos de Configuração**
   - GitHub Actions para CI/CD
   - Templates para issues e PRs
   - Documentação completa

---

## 9. Estrutura Final

### 📦 Arquivos Criados

#### Principais:
- `package.json` - Configuração do projeto
- `nodes/GoogleAi/GoogleAi.node.ts` - Implementação do node
- `credentials/GoogleAiApi.credentials.ts` - Credenciais
- `tsconfig.json` - Configuração TypeScript
- `gulpfile.js` - Build dos ícones

#### Documentação:
- `README.md` - Documentação principal
- `CHANGELOG.md` - Histórico de mudanças
- `CONTRIBUTING.md` - Guia de contribuição
- `SECURITY.md` - Política de segurança
- `LICENSE` - Licença MIT

#### GitHub:
- `.github/workflows/ci.yml` - CI/CD pipeline
- `.github/ISSUE_TEMPLATE/` - Templates de issues
- `.github/pull_request_template.md` - Template de PR
- `.github/copilot-instructions.md` - Instruções Copilot

#### Configuração:
- `.eslintrc.json` - Linting
- `.prettierrc.json` - Formatação
- `.gitignore` - Arquivos ignorados
- `.vscode/tasks.json` - Tasks VS Code

---

## 10. Instruções Finais

### 🎯 Para Testar o Node

1. **Configurar Credenciais:**
   - Obter API Key: https://ai.google.dev/
   - No n8n: Credentials → Add Credential → Google AI API

2. **Instalar Node:**
   - Settings → Community Nodes
   - URL: `https://github.com/EngThi/n8n-nodes-google-ai.git`

3. **Teste Básico:**
   ```
   Prompt: "Escreva um resumo sobre inteligência artificial em 3 parágrafos"
   Model: gemini-pro
   Temperature: 0.7
   Max Tokens: 1000
   ```

### 📋 Funcionalidades Implementadas

- ✅ Geração de conteúdo com Gemini Pro
- ✅ Suporte a múltiplos modelos
- ✅ Parâmetros configuráveis (temperature, max tokens)
- ✅ Tratamento de erros robusto
- ✅ Suporte a continueOnFail
- ✅ Credenciais seguras
- ✅ Documentação completa
- ✅ CI/CD pipeline
- ✅ Templates GitHub

### 🚀 Próximos Passos

1. Testar com diferentes prompts
2. Implementar funcionalidades de chat avançadas
3. Adicionar suporte a imagens (Gemini Pro Vision)
4. Criar testes unitários
5. Publicar no npm oficial
6. Adicionar mais modelos Google AI

---

## 📚 Recursos Úteis

- [n8n Community Nodes Documentation](https://docs.n8n.io/integrations/community-nodes/)
- [Google AI Documentation](https://ai.google.dev/)
- [n8n Node Development Guide](https://docs.n8n.io/integrations/creating-nodes/)
- [TypeScript Documentation](https://www.typescriptlang.org/)

---

## 🎉 Conclusão

Este projeto demonstra como criar um node personalizado para n8n que integra com Google AI. O processo incluiu:

1. **Configuração** completa do projeto TypeScript
2. **Implementação** do node com todas as funcionalidades
3. **Configuração** de credenciais seguras
4. **Documentação** completa e profissional
5. **Publicação** no GitHub com CI/CD
6. **Solução** de problemas técnicos encontrados

O node está pronto para uso e pode ser facilmente instalado no n8n usando a URL do GitHub: `https://github.com/EngThi/n8n-nodes-google-ai.git`

**Data:** 4 de julho de 2025
**Autor:** EngThi
**Versão:** 1.0.0
