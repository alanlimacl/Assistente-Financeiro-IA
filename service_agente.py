from pydantic import BaseModel, Field
from fastapi import FastAPI
import uvicorn
from agente_agno import agente_financeiro


# FastAPI
app = FastAPI(title='Agente Financeiro IA', description='Agente de IA para ajuda Financeira Pessoal')

class DadosUsuario(BaseModel):
    question: str = Field(min_length=10, 
                          max_length=250 , 
                          examples= ["Hoje eu comprei um sapato por 59,00 reais, paguei no Cartão de Crédito Nubank"], 
                          description="Usuário informa o gasto dele e descreve com informações") 

@app.get("/")
def read_root():
    return {'status':'online', 'mensagem': 'API do Agente Financeiro rodando!'}


@app.post("/agente_financeiro")
def agente_financeiro_api(descreva:DadosUsuario):
    mensagem = agente_financeiro(descreva)
    return {"mensagens": mensagem}


if __name__ == "__main__":
    uvicorn.run("service_agente:app", host="localhost", port=8000, reload=True)