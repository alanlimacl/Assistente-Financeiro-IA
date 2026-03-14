import requests
from requests.exceptions import RequestException 


def remover_gasto(id_gasto: int, token: str):
    """Remove um gasto do banco de dados pelo ID.
    Retorna uma string explicando o resultado."""

    try:
        URL = "http://localhost:8000/financas/remover-gasto"
        
        parametros = {'id_gasto': id_gasto}
        
        headers = {
            'Authorization': f'Bearer {token}'
        }

        resposta = requests.delete(URL, params= parametros, headers= headers )
        resposta.raise_for_status()
                    
    except RequestException as e:
        return {'status': 'erro', 'mensagem': str(e)}
    
    return resposta.json()
   