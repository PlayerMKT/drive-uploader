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
