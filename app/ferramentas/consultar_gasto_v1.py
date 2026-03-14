import requests
from requests.exceptions import RequestException

def consultar_gasto(data_inicio: str, data_final: str, token: str, categoria: str = None) -> dict:
    try:

        URL = "http://localhost:8000/financas/consultar-gasto"

        headers = {
        'Authorization': f'Bearer {token}'
            }  
            
        parametros = {'data_inicio': data_inicio,
                    'data_final': data_final,
                    'categoria': categoria}

        resposta = requests.get(url=URL, params=parametros, headers=headers)
        resposta.raise_for_status()
        
    except RequestException as e:
        return {'status': 'erro', 'mensagem': str(e)}


    return resposta.json()


if __name__ == '__main__':
    pass