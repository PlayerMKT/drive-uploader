# Security Policy

## Supported Versions

We currently support the following versions of n8n-nodes-google-ai:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it to us through GitHub's security advisory feature:

1. Go to the [Security tab](https://github.com/yourusername/n8n-nodes-google-ai/security)
2. Click "Report a vulnerability"
3. Fill out the form with details about the vulnerability

### What to include in your report:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fixes (if any)

### What to expect:

- **Acknowledgment**: We will acknowledge receipt of your report within 48 hours
- **Initial Assessment**: We will provide an initial assessment within 7 days
- **Updates**: We will keep you informed of our progress
- **Resolution**: We aim to resolve critical vulnerabilities within 90 days

## Security Best Practices

### For Users:

- Keep your API keys secure and never commit them to version control
- Use environment variables or n8n's credential system for API keys
- Regularly update the node to the latest version
- Monitor your Google AI API usage and billing

### For Developers:

- Never log or expose API keys in error messages
- Validate all user inputs
- Use secure methods for API communication
- Follow n8n's security guidelines for node development

## Disclosure Policy

We follow a responsible disclosure policy:

- We will not disclose vulnerabilities until they are fixed
- We will credit security researchers who responsibly disclose vulnerabilities
- We will provide security updates as soon as possible
