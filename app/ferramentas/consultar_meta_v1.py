import requests
from requests.exceptions import RequestException

def consultar_meta(data_mes: str, token: str, categoria: str = None) -> dict:
    """
    Consulta as metas financeiras (orçamento) definidas pelo usuário para um mês específico.
    
    Use esta ferramenta SEMPRE que o usuário:
    1. Perguntar sobre seu orçamento atual ou limites de gastos.
    2. Perguntar se "pode" ou "deve" gastar dinheiro com algo (para checar o limite antes de aconselhar).
    3. Pedir um resumo de como estão divididas as suas metas do mês.
    
    Args:
        data_mes (str): O mês e ano da consulta obrigatoriamente no formato 'YYYY-MM' (ex: '2026-04').
        categoria (str, opcional): A categoria específica para filtrar (ex: 'Lazer', 'Mercado'). 
                                   Se não for informada, retorna todas as metas do mês.
                                   
    Returns:
        dict: Retorna as metas encontradas com seus respectivos valores, ou um erro 404 
              indicando que o usuário ainda não definiu o orçamento para este mês.
    """
    try:

        URL = "http://localhost:8000/financas/consultar-metas"

        headers = {
        'Authorization': f'Bearer {token}'
            }  
            
        parametros = {'data_mes': data_mes,
                    'categoria': categoria}

        resposta = requests.get(url=URL, params=parametros, headers=headers)
        resposta.raise_for_status()
        
    except RequestException as e:
        return {'status': 'erro', 'mensagem': str(e)}


    return resposta.json()


if __name__ == '__main__':
    pass