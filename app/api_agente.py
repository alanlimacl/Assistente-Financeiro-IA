from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from app.agente_agno.agente import pergunta_agente


app = FastAPI(title='Agente Financeiro IA', description='Agente de IA para ajuda Financeira Pessoal')

class RequisicaoUsuario(BaseModel):
    text: str


@app.get("/")
def read_root():
    return {'status':'online', 'mensagem': 'API do Agente Financeiro rodando!'}


@app.post("/perguntar")
def endpoint_perguntar(pergunta: RequisicaoUsuario):
    mensagem_ia = pergunta_agente(pergunta.text)
    return {"text": mensagem_ia}


if __name__ == "__main__":
    uvicorn.run("service_agente:app", host="localhost", port=8000, reload=True)