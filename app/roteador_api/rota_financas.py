from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.roteador_api.esquemas import FinancasEsquema
from app.roteador_api.dependencias import pegar_sessao_bd
from app.roteador_api.modelos import Financas, Usuario
from app.roteador_api.dependencias import checar_token
from app.roteador_api.config import oauth2_esquema

financas_roteador = APIRouter(prefix='/financas', tags=['Financas'], dependencies=[Depends(checar_token)])

@financas_roteador.post("/adicionar-gasto")
async def adicionar_gasto(financa_esquema: FinancasEsquema, 
                          usuario: Usuario = Depends(checar_token), 
                          sessao: Session = Depends(pegar_sessao_bd)):
    
    novo_gasto = Financas(valor= financa_esquema.valor,
                            item= financa_esquema.item,
                            categoria= financa_esquema.categoria,
                            metodo_pagamento= financa_esquema.metodo_pagamento,
                            data= financa_esquema.data,
                            id_usuario= usuario.id)
    
    sessao.add(novo_gasto)
    sessao.commit()
    
    return {'mensagem': 'Gasto adicionado com sucesso',
            'id_gasto': novo_gasto.id,
            'informacoes': novo_gasto}


@financas_roteador.get("/consultar-gasto")
async def consultar_gasto(data_inicio: str, data_final: str, 
                          categoria: str = None,
                          usuario: Usuario = Depends(checar_token), 
                          sessao: Session = Depends(pegar_sessao_bd)):
    
    consulta = sessao.query(Financas).filter(Financas.id_usuario == usuario.id)
    
    if categoria:
        consulta = consulta.filter(Financas.categoria == categoria)
    
    consulta = consulta.filter(Financas.data.between(data_inicio, data_final))
    
    gastos_usuario = consulta.all()
    
    lista_gastos = []
    
    for gasto in gastos_usuario:
        lista_gastos.append({'valor': gasto.valor,
                             'item': gasto.item,
                             'categoria': gasto.categoria,
                             'metodo_pagamento':gasto.metodo_pagamento,
                             'data':gasto.data})
    
    
    return {'total_gastos': sum(gasto.valor for gasto in gastos_usuario),
            'quantidade': len(gastos_usuario),
            'gastos':lista_gastos}
    