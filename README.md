# n8n-nodes-google-ai

This is an n8n community node that integrates with Google AI services, allowing you to use Google's powerful AI models like Gemini Pro in your n8n workflows.

## 🚀 Sistema Completo de Backup e Clonagem

**Novo!** Este projeto agora inclui um sistema completo para backup e clonagem do ambiente de desenvolvimento:

- 📸 **Captura completa** do ambiente (dependências, configurações, ferramentas)
- 📦 **Export portátil** em arquivo compactado
- 🔄 **Restauração automática** em novos ambientes
- 🎛️ **Interface interativa** para gerenciar tudo
- 🎯 **Clone perfeito** de qualquer Codespace

### Comandos Rápidos
```bash
# Menu interativo completo
npm run env:manage

# Backup rápido do ambiente
npm run env:export

# Restaurar ambiente
npm run env:restore
```

**📚 Veja o guia completo:** [SISTEMA_COMPLETO_BACKUP.md](./SISTEMA_COMPLETO_BACKUP.md)

---

## Features

- **Multiple Models**: Support for Gemini Pro and Gemini Pro Vision
- **Content Generation**: Generate text content using AI prompts
- **Chat Functionality**: Interactive chat capabilities
- **Configurable Parameters**: Control temperature, max tokens, and other generation settings
- **Error Handling**: Robust error handling with continueOnFail support

## Installation

### For Local Development/Testing

Since this package is not yet published to npm, you can install it locally:

#### Method 1: Using the generated package file
1. Download or build the `.tgz` file
2. In n8n, go to "Settings" → "Community Nodes"
3. Use the full path to the `.tgz` file: `/workspaces/codespaces-blank/n8n-nodes-google-ai-1.0.0.tgz`

#### Method 2: Install from GitHub (after publishing)
1. In n8n, go to "Settings" → "Community Nodes"
2. Enter: `https://github.com/yourusername/n8n-nodes-google-ai.git`

#### Method 3: Using npm link (for developers)
```bash
# In the project directory
npm link

# In your n8n installation directory
npm link n8n-nodes-google-ai
```

### For Production Use

Once published to npm, follow the [installation guide](https://docs.n8n.io/integrations/community-nodes/installation/) in the n8n community nodes documentation.

### Prerequisites

- n8n installed and running
- Google AI API key (get one from [Google AI Studio](https://ai.google.dev/))

## Configuration

1. **Credentials**: Set up your Google AI API credentials
   - Go to your n8n instance
   - Navigate to Settings > Credentials
   - Create new credentials for "Google AI API"
   - Enter your API key

2. **Node Usage**: 
   - Add the Google AI node to your workflow
   - Select your credentials
   - Choose the model (Gemini Pro or Gemini Pro Vision)
   - Enter your prompt
   - Configure generation parameters (temperature, max tokens)

## Parameters

- **Resource**: Choose between "Generate Content" or "Chat"
- **Model**: Select AI model (Gemini Pro, Gemini Pro Vision)
- **Prompt**: Text input for the AI model
- **Temperature**: Control randomness (0-1)
- **Max Output Tokens**: Maximum number of tokens to generate

## Examples

### Simple Text Generation
```
Prompt: "Write a short story about a robot learning to paint"
Model: gemini-pro
Temperature: 0.7
Max Tokens: 500
```

### Technical Documentation
```
Prompt: "Explain how to implement authentication in a Node.js API"
Model: gemini-pro
Temperature: 0.3
Max Tokens: 1000
```

## Development

### Building the Node

```bash
# Install dependencies
npm install

# Build the node
npm run build

# Run linting
npm run lint

# Format code
npm run format
```

### Testing

Test your node by:
1. Building the project
2. Creating a symbolic link to your n8n installation
3. Restarting n8n
4. Testing with various prompts and configurations

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- [n8n Community Forum](https://community.n8n.io/)
- [Google AI Documentation](https://ai.google.dev/)
- [GitHub Issues](https://github.com/yourusername/n8n-nodes-google-ai/issues)

## Changelog

### 1.0.0
- Initial release
- Support for Gemini Pro models
- Basic content generation functionality
- Credential management
