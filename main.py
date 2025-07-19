import os
from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "73295299472-280tug542rma0alqbaidv813tf8u4i8l.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "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")
CODESPACE_NAME = "glowing-computing-machine-4jg6wwrp9qjphq5pq"  # só o nome, não URL
PORT = 8081
REDIRECT_PATH = "/auth/callback"
REDIRECT_URI = f"https://{CODESPACE_NAME}-{PORT}.app.github.dev{REDIRECT_PATH}"

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="um-segredo-bem-forte-aqui")
oauth = OAuth()

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile", "response_type": "code"},
    redirect_uri=REDIRECT_URI
)

@app.get('/')
async def homepage(request: Request):
    return RedirectResponse(url='/login')

@app.get('/login')
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, REDIRECT_URI)

@app.get(REDIRECT_PATH)
async def auth_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        return JSONResponse({"token": token})
    except Exception as e:
        return JSONResponse({"error": str(e)})

# Para rodar: uvicorn main:app --host 0.0.0.0 --port 8080
