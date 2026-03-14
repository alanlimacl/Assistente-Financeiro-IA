import uvicorn
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.agente_agno.agente import criar_agente
from app.ferramentas.consultar_gasto_v1 import consultar_gasto
from app.ferramentas.adicionar_gasto_v1 import adicionar_gasto
from app.ferramentas.remover_gasto_v1 import remover_gasto
from app.roteador_api.config import ALGORITHM, SECRET_KEY
from app.config import MODELO_IA


agente_roteador = APIRouter(prefix='/agente', tags=['Agente'])


class RequisicaoUsuario(BaseModel):
    text: str


oauth2_esquema = OAuth2PasswordBearer(tokenUrl="/autenticador/login")

@agente_roteador.post("/perguntar")
async def perguntar_agente(mensagem: RequisicaoUsuario, token: str = Depends(oauth2_esquema)):
    # Pegar o Id do usuário
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = payload.get('sub')
        
        if id_usuario is None:
            raise HTTPException(status_code=401, detail='Token inválido: O ID do usuário não encontrado')
    
    except JWTError:
        raise HTTPException(status_code=401, detail='A sua sessão expirou.')
    
    
    # Função Casca
    def ferramenta_ia_consultar(data_inicio: str, data_final: str, categoria: str = None):
        """Use esta ferramenta para consultar os gastos do usuário no banco de dados. As datas devem estar no formato YYYY-MM-DD."""
        resultado_dict = consultar_gasto(data_inicio, data_final, token, categoria)
        return str(resultado_dict)

    # Função Casca
    def ferramenta_ia_adicionar(valor: float, item: str, categoria: str, metodo_pagamento: str, data: str = None):
        """Use esta ferramenta para adicionar um novo gasto do usuário no banco de dados."""
        resultado_dict = adicionar_gasto(valor, item, categoria, metodo_pagamento, token, data)
        return str(resultado_dict)


    def ferramenta_ia_remover(id_gasto: int):
        """Use essa ferramenta para remover um gasto do usuário no banco de dados."""
        resultado_dict = remover_gasto(id_gasto, token)
        return str(resultado_dict)
    
    
    # Criação da instância do Agente
    agente_financeiro = criar_agente(
        MODELO_IA, 
        ferramentas_com_token=[ferramenta_ia_consultar, ferramenta_ia_adicionar, ferramenta_ia_remover], 
        id_usuario=id_usuario )
 
 
    def gerar_resposta():
        resposta_stream = agente_financeiro.run(mensagem.text, stream=True)    

        for chunk in resposta_stream:
            if chunk.content:
                yield chunk.content.encode('utf-8')

    return StreamingResponse(gerar_resposta(), media_type='text/plain')

