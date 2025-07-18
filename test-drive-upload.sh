#!/bin/bash

# Script para testar upload Google Drive
echo "🚀 TESTE GOOGLE DRIVE UPLOAD"
echo "============================="

# Matar processos Python existentes
pkill -f python 2>/dev/null || true

# Aguardar um momento
sleep 2

# Executar o uploader simples
echo "Executando uploader..."
python3 google-drive-simple.py
