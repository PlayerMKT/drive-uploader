# 🚀 Solução Rápida para GitHub Codespaces

## Problema Identificado
O n8n está rodando no GitHub Codespaces e não consegue acessar arquivos locais diretamente. Você precisa usar uma URL do GitHub.

## ✅ Solução Imediata

### 1. Crie um repositório no GitHub
- Vá para https://github.com
- Clique em "New repository"
- Nome: `n8n-nodes-google-ai`
- Marque como **público**
- **NÃO** inicialize com README

### 2. Publique o código (execute estes comandos):
```bash
git remote add origin https://github.com/SEUUSERNAME/n8n-nodes-google-ai.git
git push -u origin main
```

### 3. No n8n, use a URL do GitHub:
- Vá para: Settings → Community Nodes
- No campo "npm package name", use:
```
https://github.com/SEUUSERNAME/n8n-nodes-google-ai.git
```

## 📋 Comandos para Executar Agora

Substitua `SEUUSERNAME` pelo seu nome de usuário do GitHub e execute:

```bash
# Adicionar remote do GitHub
git remote add origin https://github.com/SEUUSERNAME/n8n-nodes-google-ai.git

# Fazer push
git push -u origin main
```

## 🔑 Depois da Instalação

1. Configure as credenciais do Google AI
2. Obtenha uma API Key em: https://ai.google.dev/
3. No n8n: Credentials → Add Credential → Google AI API

## ⚡ Teste Rápido

Depois de instalar, teste com este prompt:
```
Escreva um resumo sobre inteligência artificial em 3 parágrafos
```
