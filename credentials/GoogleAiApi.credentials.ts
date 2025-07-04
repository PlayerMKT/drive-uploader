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
