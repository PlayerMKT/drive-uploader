# 🔄 Scripts de Automação - n8n Google AI

Este projeto inclui scripts automatizados para gerenciar o backup e limpeza do Codespace.

## 📋 Scripts Disponíveis

### 1. 🚀 `backup-to-github.sh`
**Backup automático para GitHub**

```bash
./backup-to-github.sh
```

**O que faz:**
- ✅ Adiciona todos os arquivos ao Git
- 💾 Cria commit com timestamp automático
- ☁️ Envia tudo para o GitHub
- 📊 Mostra resumo do que foi salvo

### 2. 🧹 `cleanup-codespace.sh`
**Limpeza do Codespace**

```bash
./cleanup-codespace.sh
```

**O que faz:**
- 📦 Faz backup automático antes de limpar
- 🗑️ Remove arquivos `.zip` e `.tgz` (já estão no Git)
- 📁 Remove `node_modules` (pode ser reinstalado)
- 💾 Limpa cache do npm e sistema
- 🧹 Remove pasta `upload-files` duplicada
- 📊 Mostra espaço liberado

## 🎯 Uso Recomendado

### Para Backup Rápido:
```bash
# Salvar tudo no GitHub
./backup-to-github.sh
```

### Para Otimizar Codespace:
```bash
# Limpar e otimizar (já inclui backup)
./cleanup-codespace.sh
```

### Após Limpeza (se necessário):
```bash
# Reinstalar dependências
npm install

# Rebuildar o projeto
npm run build
```

## 🔒 Segurança

- ✅ **Todos os arquivos importantes são salvos no Git antes da limpeza**
- ✅ **O `.gitignore` protege arquivos sensíveis**
- ✅ **Você pode sempre recuperar tudo do GitHub**

## 📈 Benefícios

- 🚀 **Codespace mais rápido** (menos arquivos)
- ☁️ **Backup seguro no GitHub**
- 🔄 **Processo automatizado**
- 💾 **Mais espaço disponível**

## 🆘 Recuperação

Se precisar restaurar tudo:

```bash
# Clonar o repositório
git clone [seu-repo-url] n8n-google-ai

# Instalar dependências
cd n8n-google-ai
npm install

# Rebuildar
npm run build
```

---

💡 **Dica:** Execute `./cleanup-codespace.sh` regularmente para manter o Codespace otimizado!
