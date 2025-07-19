#!/usr/bin/env python3
"""
Drive Uploader - Backend FastAPI
Serve arquivos estáticos e fornece endpoints para callback OAuth2 se necessário
"""

import os
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# === CONFIGURAÇÕES ===
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "1060201687476-0c6m7fb4ttsmg84uibe6jh8utbmplr11.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "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")
CODESPACE_NAME = os.getenv("CODESPACE_NAME", "")
PORT = int(os.getenv("PORT", "8080"))
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-super-segura-aqui")

print("🚀 Iniciando Drive Uploader Server...")
print(f"📋 Client ID: {GOOGLE_CLIENT_ID[:20]}...")
print(f"🔐 Secret configurado: {bool(GOOGLE_CLIENT_SECRET)}")

# Criar aplicação FastAPI
app = FastAPI(
    title="Drive Uploader API",
    description="Backend para aplicação de upload ao Google Drive",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# === CONFIGURAR CORS ===
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# Adicionar URL do Codespaces se disponível
if CODESPACE_NAME:
    codespace_url = f"https://{CODESPACE_NAME}-8080.app.github.dev"
    origins.append(codespace_url)
    print(f"🌐 Codespace URL: {codespace_url}")
else:
    print("💻 Executando localmente")

# URL específica do usuário
user_codespace = "https://glowing-computing-machine-4jg6wwrp9qjphq5pq.github.dev"
origins.append(user_codespace)
print(f"🎯 URL do usuário: {user_codespace}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"🔒 CORS configurado para: {', '.join(origins)}")

# === VERIFICAR ESTRUTURA DE PASTAS ===
current_dir = Path(__file__).parent
frontend_path = current_dir.parent / "frontend"

if not frontend_path.exists():
    print(f"⚠️ Pasta frontend não encontrada: {frontend_path}")
    # Criar pasta frontend se não existir
    frontend_path.mkdir(exist_ok=True)
    print(f"📁 Pasta frontend criada: {frontend_path}")
else:
    print(f"📂 Frontend encontrado: {frontend_path}")

# === ROTAS DA API ===

@app.get("/api/health")
async def health_check():
    """Endpoint de verificação de saúde"""
    return {
        "status": "ok",
        "message": "Drive Uploader API funcionando!",
        "version": "1.0.0",
        "client_id_configured": bool(GOOGLE_CLIENT_ID),
        "frontend_path": str(frontend_path),
        "codespace": CODESPACE_NAME or "local"
    }

@app.get("/api/config")
async def get_config():
    """Retorna configurações públicas (sem secrets)"""
    return {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uris": origins,
        "scopes": [
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/userinfo.profile"
        ]
    }

@app.get("/api/oauth/callback")
async def oauth_callback(request: Request):
    """Callback OAuth2 (se necessário no futuro)"""
    # Por enquanto, apenas redireciona para a página principal
    # Implementação futura pode processar códigos de autorização aqui
    return RedirectResponse(url="/")

# === ROTA RAIZ ===
@app.get("/")
async def root():
    """Redireciona para o frontend"""
    return RedirectResponse(url="/index.html")

# === MONTAR ARQUIVOS ESTÁTICOS ===
try:
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
    print(f"📁 Arquivos estáticos montados: {frontend_path}")
except Exception as e:
    print(f"❌ Erro ao montar arquivos estáticos: {e}")

    # Criar arquivo index.html básico se não existir
    index_file = frontend_path / "index.html"
    if not index_file.exists():
        basic_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drive Uploader - Configuração Necessária</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; text-align: center; }
        .error { color: #ea4335; background: #fce8e6; padding: 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="error">
        <h1>🚧 Configuração Necessária</h1>
        <p>Os arquivos do frontend não foram encontrados.</p>
        <p>Certifique-se de que a pasta 'frontend' existe com os arquivos corretos.</p>
        <hr>
        <p><strong>API Status:</strong> Funcionando ✅</p>
        <p><strong>Client ID:</strong> Configurado """ + ('✅' if GOOGLE_CLIENT_ID else '❌') + """</p>
        <p><strong>Modo:</strong> """ + (CODESPACE_NAME or "Local") + """</p>
    </div>
</body>
</html>"""

        index_file.write_text(basic_html, encoding='utf-8')
        print(f"📝 Arquivo index.html básico criado")

# === EVENTO DE INICIALIZAÇÃO ===
@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print("🚀 DRIVE UPLOADER - SERVIDOR INICIADO!")
    print("=" * 50)
    print(f"📊 Porta: {PORT}")
    print(f"📁 Frontend: {frontend_path}")
    print(f"🔑 Client ID: {GOOGLE_CLIENT_ID[:30]}...")
    print(f"🌐 URLs permitidas: {len(origins)} configuradas")

    if CODESPACE_NAME:
        print(f"☁️ Codespace: {user_codespace}")
        print(f"⚠️ IMPORTANTE: Torne a porta {PORT} PÚBLICA no Codespaces!")
    else:
        print(f"💻 Local: http://localhost:{PORT}")

    print("=" * 50)
    print("📖 Documentação da API: /api/docs")
    print("🔍 Health Check: /api/health")
    print("⚙️ Configuração: /api/config")
    print("=" * 50)

# === MAIN ===
if __name__ == "__main__":
    print(f"🌐 Iniciando servidor na porta {PORT}...")
    print(f"🔗 Acesse: http://localhost:{PORT}")

    if CODESPACE_NAME:
        print(f"☁️ Codespace: {user_codespace}")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
        log_level="info"
    )
