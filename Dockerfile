# Use Node.js 22.16.0 (mesma versão do ambiente original)
FROM node:22.16.0

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de configuração primeiro (para cache do Docker)
COPY package*.json ./
COPY tsconfig.json ./
COPY gulpfile.js ./

# Instalar dependências do projeto
RUN npm install

# Copiar código fonte
COPY . .

# Instalar pacotes globais necessários
RUN npm install -g n8n pnpm

# Executar build
RUN npm run build

# Expor porta padrão do n8n
EXPOSE 5678

# Comando padrão
CMD ["npm", "run", "dev"]
