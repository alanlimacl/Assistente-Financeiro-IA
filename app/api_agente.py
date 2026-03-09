from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn
from app.agente_agno.agente import agente, pergunta_agente


app = FastAPI(title='Agente Financeiro IA', description='Agente de IA para ajuda Financeira Pessoal')

class RequisicaoUsuario(BaseModel):
    text: str


@app.get("/")
def read_root():
    return {'status':'online', 'mensagem': 'API do Agente Financeiro rodando!'}


def stream_agente_resposta(pergunta: RequisicaoUsuario):
    for chunk in agente.run(pergunta, stream=True):
        if chunk.content:
            yield chunk.content


@app.post("/perguntar")
def endpoint_perguntar(pergunta: RequisicaoUsuario):
    return StreamingResponse(stream_agente_resposta(pergunta), 
                             media_type='text/plain')


if __name__ == "__main__":
    uvicorn.run("service_agente:app", host="localhost", port=8000, reload=True)