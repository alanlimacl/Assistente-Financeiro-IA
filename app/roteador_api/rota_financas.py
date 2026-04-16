from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.roteador_api.esquemas import FinancasEsquema, MetaGastosEsquema
from app.roteador_api.dependencias import pegar_sessao_bd
from app.roteador_api.modelos import Financas, Usuario, MetaGastos
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


# Rota para consultar gastos
@financas_roteador.get("/consultar-gasto")
async def consultar_gasto(data_inicio: str, data_final: str, 
                          categoria: str = None,
                          usuario: Usuario = Depends(checar_token), 
                          sessao: Session = Depends(pegar_sessao_bd),
                          ):
    
    consulta = sessao.query(Financas).filter(Financas.id_usuario == usuario.id)
    
    if categoria:
        consulta = consulta.filter(Financas.categoria == categoria)
    
    consulta = consulta.filter(Financas.data.between(data_inicio, data_final))
    
    gastos_usuario = consulta.all()
    
    if not gastos_usuario:
        raise HTTPException(status_code=404, detail='Não foi encontrado gasto registrado pelo usuário.')    
        
    lista_gastos = []
    
    for gasto in gastos_usuario:
        lista_gastos.append({'id': gasto.id,
                            'valor': gasto.valor,
                             'item': gasto.item,
                             'categoria': gasto.categoria,
                             'metodo_pagamento':gasto.metodo_pagamento,
                             'data':gasto.data})
    
    
    return {'total_gastos': sum(gasto.valor for gasto in gastos_usuario),
            'quantidade': len(gastos_usuario),
            'gastos':lista_gastos}


# Rota para remover um gasto
@financas_roteador.delete("/remover-gasto")
async def remover_gasto(id_gasto: int,
                        usuario: Usuario = Depends(checar_token),
                        sessao: Session = Depends(pegar_sessao_bd)):
    
    gasto_para_remover = sessao.query(Financas).filter(Financas.id == id_gasto).first()
    
    if not gasto_para_remover:
        raise HTTPException(status_code=404, detail='Gasto não localizado.')
        
    if not gasto_para_remover.id_usuario == usuario.id:
        raise HTTPException(status_code=401, detail='Você não tem permissão para realizar essa operação.')
    
    sessao.delete(gasto_para_remover)
    sessao.commit()
    
    return {'mensagem': f'Gasto do ID: {gasto_para_remover.id} removido com sucesso.',
            'informacao': gasto_para_remover}
    

# Rota para adicionar metas
@financas_roteador.post('/meta-gastos')
async def adicionar_meta_gastos(meta_gasto: MetaGastosEsquema,
                                usuario: Usuario = Depends(checar_token),
                                sessao: Session = Depends(pegar_sessao_bd)):
    
    # Consultando informações para comparar no banco de dados
    metas_existentes = sessao.query(MetaGastos).filter(
        MetaGastos.id_usuario == usuario.id,
        MetaGastos.categoria == meta_gasto.categoria,
        MetaGastos.valor == meta_gasto.valor,
        MetaGastos.data_mes == meta_gasto.data_mes).first()
    
    if metas_existentes:
        # Se a meta já existe, atualiza o valor
        metas_existentes.valor = meta_gasto.valor
        sessao.commit()
        sessao.refresh(metas_existentes)

        return {'mensagem':f'Meta de {metas_existentes.categoria} para o mês ({metas_existentes.data_mes}) atualizada com sucesso.',
                'informacoes': metas_existentes}
    
    else:
        # Se não existe, cria uma nova
        nova_meta_gasto = MetaGastos(valor=meta_gasto.valor,
                                    categoria=meta_gasto.categoria,
                                    data_mes=meta_gasto.data_mes,
                                    id_usuario=usuario.id)
        
        sessao.add(nova_meta_gasto)
        sessao.commit()
        sessao.refresh(nova_meta_gasto)
    
        return {'mensagem': f'Nova meta de {nova_meta_gasto.categoria} para o mês ({nova_meta_gasto.data_mes}) criada com sucesso.',
                'informacoes': nova_meta_gasto}


# Rota para consultar as metas
@financas_roteador.get('/consultar-metas')
async def consultar_metas(data_mes: str,
                            categoria: str = None,
                            usuario: Usuario = Depends(checar_token),
                            sessao: Session = Depends(pegar_sessao_bd)):

    metas_existente = sessao.query(MetaGastos).filter(MetaGastos.data_mes == data_mes,
                                                      MetaGastos.id_usuario == usuario.id)
    
    if categoria:
        metas_existente = metas_existente.filter(MetaGastos.categoria == categoria)
    
    todas_metas = metas_existente.all()
    
    if not todas_metas:
        raise HTTPException(status_code=404, detail=f'Nenhuma meta encontrada para o mês {data_mes}')
    
    lista_metas = [
        {
            'id':meta.id,
            'valor': meta.valor,
            'categoria': meta.categoria,
            'data_mes': meta.data_mes
        }
        for meta in todas_metas
    ]
    
    return {'mensagem': f'Suas metas do mês ({data_mes})',
            'informacoes': lista_metas}