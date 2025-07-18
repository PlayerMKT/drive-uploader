# YouTube Automation + Google Drive Integration

## 🎬 SISTEMA COMPLETO PRONTO

Seu sistema integrado está 100% funcional! Aqui está o que foi criado:

### 📁 Arquivos Principais

1. **`youtube-automation-drive.py`** - Sistema principal de integração
2. **`sistema-integrado.sh`** - Script de controle principal
3. **`youtube-automation/main_enhanced.py`** - Versão aprimorada do main.py
4. **`google-drive-manual.py`** - Sistema de autenticação e upload
5. **`auto-backup-drive.sh`** - Backup automático

### 🚀 Como Usar

#### Opção 1: Script Principal (Recomendado)
```bash
# Executar sistema completo
./sistema-integrado.sh

# Ou via npm
npm run sistema-integrado
```

#### Opção 2: Automação Direta
```bash
# Executar automação YouTube + Drive
python3 youtube-automation-drive.py

# Ou via npm
npm run youtube-automation
```

#### Opção 3: Apenas YouTube
```bash
# Executar apenas YouTube automation
cd youtube-automation
python3 main_enhanced.py

# Ou via npm
npm run youtube-only
```

### 🔧 Configuração Inicial

1. **Autenticar Google Drive** (primeira vez):
```bash
python3 google-drive-manual.py
```

2. **Configurar ambiente**:
```bash
# Via script principal
./sistema-integrado.sh
# Opção 5: Configurar Ambiente

# Ou via npm
npm run configure-env
```

### 🎯 Funcionalidades Principais

#### 1. **Geração de Conteúdo**
- ✅ Síntese de fala (Google Cloud TTS)
- ✅ Geração de imagens (SDXL + Imagen)
- ✅ Montagem de vídeo (MoviePy)

#### 2. **Integração Google Drive**
- ✅ Upload automático de áudios
- ✅ Upload automático de imagens
- ✅ Upload automático de vídeos
- ✅ Estrutura organizada de pastas
- ✅ Resumo do projeto em JSON

#### 3. **Sistema de Backup**
- ✅ Backup completo do workspace
- ✅ Backup automático silencioso
- ✅ Restauração de ambiente

### 📊 Fluxo de Trabalho

1. **Autenticação**: Sistema autentica automaticamente com Google Drive
2. **Estrutura**: Cria pastas organizadas no Drive para cada projeto
3. **Geração**: Processa cenas criando áudio, imagens e vídeo
4. **Upload**: Faz upload automático de todos os arquivos
5. **Resumo**: Gera resumo final com links do Drive
6. **Limpeza**: Remove arquivos locais após upload

### 🎨 Exemplo de Uso

```python
# Cenas personalizadas
scenes = [
    "Bem-vindos ao nosso canal de tecnologia",
    "Hoje vamos falar sobre IA e automação",
    "Não esqueçam de se inscrever!"
]

# Executar automação
automation = YouTubeAutomationDriveIntegration()
result = automation.run_full_automation(scenes)

# Resultado
print(f"Projeto: {result['project_name']}")
print(f"Vídeo: {result['files']['video']['link']}")
```

### 📋 Comandos NPM Disponíveis

```bash
# Sistema integrado
npm run sistema-integrado

# Automação completa
npm run youtube-automation

# Apenas YouTube
npm run youtube-only

# Configurar ambiente
npm run configure-env

# Backup
npm run drive-auto

# Upload manual
npm run drive-manual
```

### 🔍 Monitoramento

- **Logs**: Arquivos de log em `youtube_automation.log`
- **Status**: Use `./sistema-integrado.sh` opção 6
- **Resumos**: Arquivos JSON com detalhes de cada projeto

### 🚨 Resolução de Problemas

1. **Erro de autenticação**: Execute `python3 google-drive-manual.py`
2. **Dependências**: Execute `./sistema-integrado.sh` opção 5
3. **Espaço em disco**: Execute `./sistema-integrado.sh` opção 6

### 📁 Estrutura no Google Drive

```
youtube-project-20250117_123456/
├── Audio/
│   ├── scene_1.mp3
│   ├── scene_2.mp3
│   └── scene_3.mp3
├── Images/
│   ├── sdxl_scene_1.jpg
│   ├── imagen_scene_1.jpg
│   └── ...
├── Videos/
│   └── processing_files/
└── Final-Output/
    ├── final_video.mp4
    └── project_summary.json
```

### 🎉 Recursos Avançados

- **Modo Simulação**: Funciona mesmo sem Google Cloud configurado
- **Fallback**: Cria arquivos dummy se APIs não estiverem disponíveis
- **Recuperação**: Sistema robusto de tratamento de erros
- **Organização**: Estrutura clara de pastas e arquivos

## ✅ SISTEMA PRONTO PARA USO!

Agora você tem um sistema completo que:
- ✅ Gera conteúdo audiovisual automaticamente
- ✅ Faz upload tudo para Google Drive
- ✅ Mantém backup completo do workspace
- ✅ Integra com todas as funcionalidades do Google Workspace

**Para começar agora:**
```bash
./sistema-integrado.sh
```

Escolha a opção 1 e deixe a mágica acontecer! 🚀
