<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# n8n Google AI Node Instructions

This project is an n8n custom node for integrating with Google AI services. When working on this project:

## Development Guidelines

1. **n8n Node Structure**: Follow n8n's node development patterns
   - Use proper INodeType interface implementations
   - Implement proper credential management
   - Handle errors gracefully with continueOnFail support

2. **Google AI Integration**: 
   - Use Google AI REST API endpoints
   - Implement proper authentication with API keys
   - Support multiple models (Gemini Pro, Gemini Pro Vision)
   - Handle rate limiting and error responses

3. **TypeScript Best Practices**:
   - Use proper type definitions from n8n-workflow
   - Implement error handling with NodeOperationError
   - Use async/await for API calls

4. **Node Properties**:
   - Provide clear descriptions for all parameters
   - Use appropriate input types (string, number, options)
   - Set reasonable defaults for optional parameters

## Key Features to Implement

- Content generation with Gemini models
- Chat functionality
- Temperature and token controls
- Multi-model support
- Error handling and validation

## Testing

- Test with various prompt types
- Verify credential authentication
- Test error scenarios and edge cases
- Ensure proper data flow between nodes
