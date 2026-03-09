from fastapi import FastAPI
from app.roteador_api.rota_autenticador import autenticador_roteador
from app.roteador_api.rota_financas import financas_roteador

app = FastAPI()

@app.get("/")
async def root():
    return {'mensagem':'Bem-vindo a API para sua Assistência Financeira'}

app.include_router(autenticador_roteador)
app.include_router(financas_roteador)