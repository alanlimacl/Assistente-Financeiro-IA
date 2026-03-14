import requests
from requests.exceptions import RequestException
from datetime import datetime

def adicionar_gasto(valor: float, item: str,
                    categoria: str, metodo_pagamento: str, 
                    token,
                    data: str = None) -> dict:
    """
    Usa esta ferramenta OBRIGATORIAMENTE sempre que o usuário relatar que gastou dinheiro, comprou algo ou pagou uma conta.

    Regras para extração dos parâmetros:
    - valor (float): Apenas o número financeiro positivo. Exemplo: se o usuário disser "gastei 50 reais", passe 50.0.
    - item (str): Nome curto e direto do que foi comprado ou pago (ex: "Acarajé", "Uber", "Conta de Luz").
    - categoria (str): Classifique o gasto em UMA destas categorias exatas: 'Alimentação', 'Transporte', 'Assinatura', 'Lazer', 'Saúde', 'Educação', 'Compras', ou 'Outros'. Não invente categorias fora desta lista.
    - metodo_pagamento (str): Identifique a forma de pagamento e use UMA destas opções exatas: 'Pix', 'Cartão de Crédito', 'Cartão de Débito', 'Dinheiro', ou 'Boleto'. Se o usuário não informar, assuma 'Pix' como padrão.
    - data (str): O dia em que o gasto ocorreu. Se o usuário disser "hoje", "agora" ou não especificar, passe exatamente a string "hoje". Se ele falar um dia específico (ex: "ontem", "dia 5"), tente formatar como 'YYYY-MM-DD'.

    Returns:
    dict: O JSON com o status de confirmação do banco de dados.
    """
    
    try:
        
        if not data or data.lower() == 'hoje':
            data_atual = str(datetime.now().strftime("%Y-%m-%d"))
            data = data_atual
        
    
        URL = "http://localhost:8000/financas/adicionar-gasto"

        headers = {
        'Authorization': f'Bearer {token}'
            }  
            
        parametros = {'valor': valor,
                    'item': item,
                    'categoria': categoria,
                    'metodo_pagamento': metodo_pagamento,
                    'data': data}

        resposta = requests.post(url=URL, json=parametros, headers=headers)
        resposta.raise_for_status()
        
    except RequestException as e:
        return {'status': 'erro', 'mensagem': str(e)}
    
    
    return resposta.json()



if __name__ == '__main__':
    teste = adicionar_gasto(10, 'teste', 'teste', 'teste', 'hoje')