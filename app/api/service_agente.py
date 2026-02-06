from pydantic import BaseModel, Field
from fastapi import FastAPI
import uvicorn
from app.core.agente_agno import agente_financeiro


# FastAPI
app = FastAPI(title='Agente Financeiro IA', description='Agente de IA para ajuda Financeira Pessoal')

class RequisicaoUsuario(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {'status':'online', 'mensagem': 'API do Agente Financeiro rodando!'}


@app.post("/perguntar")
def endpoint_perguntar(pergunta: RequisicaoUsuario):
    mensagem_ia = agente_financeiro(pergunta.text)
    return {"text": mensagem_ia}


if __name__ == "__main__":
    uvicorn.run("service_agente:app", host="localhost", port=8000, reload=True)