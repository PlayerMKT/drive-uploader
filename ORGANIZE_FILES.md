# 📁 Como Organizar os Arquivos nas Pastas Corretas

## ❌ Problema Identificado
Os arquivos foram enviados todos na raiz do repositório, mas o n8n precisa de uma estrutura específica de pastas.

## ✅ Estrutura Correta Necessária

### 📂 Como organizar no GitHub:

1. **Vá para o seu repositório:** https://github.com/EngThi/n8n-nodes-google-ai

2. **Crie as pastas necessárias:**

#### Pasta `nodes/GoogleAi/`
- Clique em "Add file" → "Create new file"
- Digite: `nodes/GoogleAi/README.md`
- Escreva qualquer coisa (ex: "temp file")
- Commit

#### Pasta `credentials/`
- Clique em "Add file" → "Create new file"  
- Digite: `credentials/README.md`
- Escreva qualquer coisa (ex: "temp file")
- Commit

#### Pasta `.github/workflows/`
- Clique em "Add file" → "Create new file"
- Digite: `.github/workflows/README.md`
- Escreva qualquer coisa (ex: "temp file")
- Commit

#### Pasta `.github/ISSUE_TEMPLATE/`
- Clique em "Add file" → "Create new file"
- Digite: `.github/ISSUE_TEMPLATE/README.md`
- Escreva qualquer coisa (ex: "temp file")
- Commit

3. **Mover os arquivos:**

#### Mover `GoogleAi.node.ts`:
- Clique no arquivo na raiz
- Clique no ícone de lápis (Edit)
- No campo do nome do arquivo, mude de `GoogleAi.node.ts` para `nodes/GoogleAi/GoogleAi.node.ts`
- Commit

#### Mover `googleai.svg`:
- Clique no arquivo na raiz
- Clique no ícone de lápis (Edit)
- No campo do nome do arquivo, mude de `googleai.svg` para `nodes/GoogleAi/googleai.svg`
- Commit

#### Mover `GoogleAiApi.credentials.ts`:
- Clique no arquivo na raiz
- Clique no ícone de lápis (Edit)
- No campo do nome do arquivo, mude de `GoogleAiApi.credentials.ts` para `credentials/GoogleAiApi.credentials.ts`
- Commit

#### Mover `ci.yml`:
- Clique no arquivo na raiz
- Clique no ícone de lápis (Edit)
- No campo do nome do arquivo, mude de `ci.yml` para `.github/workflows/ci.yml`
- Commit

#### Mover os templates:
- `bug_report.md` → `.github/ISSUE_TEMPLATE/bug_report.md`
- `feature_request.md` → `.github/ISSUE_TEMPLATE/feature_request.md`
- `pull_request_template.md` → `.github/pull_request_template.md`
- `copilot-instructions.md` → `.github/copilot-instructions.md`

4. **Deletar os arquivos README.md temporários** que criamos nas pastas.

## 🚀 Alternativa Mais Fácil

### Opção A: Deletar tudo e refazer
1. Vá para o repositório
2. Selecione todos os arquivos
3. Delete tudo
4. Extraia o ZIP localmente
5. Faça upload pasta por pasta:
   - Primeiro upload: pasta `nodes/`
   - Segundo upload: pasta `credentials/`
   - Terceiro upload: pasta `.github/`
   - Quarto upload: arquivos da raiz

### Opção B: Usar Git localmente
Se você tem Git instalado no seu PC:

```bash
# Clone o repositório
git clone https://github.com/EngThi/n8n-nodes-google-ai.git

# Copie os arquivos na estrutura correta
# Depois:
git add .
git commit -m "Organize files in correct folder structure"
git push
```

## 📋 Estrutura Final Esperada

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
└── .github/
    ├── workflows/
    │   └── ci.yml
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    ├── copilot-instructions.md
    └── pull_request_template.md
```

## ⚠️ Importante
Sem a estrutura correta de pastas, o n8n **NÃO** conseguirá instalar o node!

Qual método você prefere usar? A opção A (deletar e refazer) é mais simples!
