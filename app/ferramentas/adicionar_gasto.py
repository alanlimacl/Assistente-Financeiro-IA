from datetime import datetime
from app.config import BANCO_DADOS
import sqlite3
import os


# Ferramenta para adicionar os gastos no Banco de Dados
def adicionar_gastos(
    item: str,
    valor: float,
    categoria: str,
    metodo_pagamento: str,
    data: str = None) -> str:
    
    if not data or data.lower() == 'hoje':
        data_atual = datetime.now().strftime("%Y-%m-%d")
        data = data_atual
        
    # Verificar a CONEXÃO com o Banco de Dados SQL
    try:
        os.makedirs(os.path.dirname(BANCO_DADOS), exist_ok=True)
        
        conexao = sqlite3.connect(BANCO_DADOS)
        cursor = conexao.cursor()

    except sqlite3.OperationalError as e:
        return(f'Erro de Conexão com o Banco de Dados: {e}')
    
    
    # Verificar a execução do COMANDO SQL
    try:
        query = """INSERT INTO controle_financeiro 
                 (item, valor, categoria, metodo_pagamento, data) 
                 VALUES (?, ?, ?, ?, ?)"""
                 
        cursor.execute(query, (item, valor, categoria, metodo_pagamento, data))
    
        conexao.commit()
        conexao.close()
        
        return f"Sucesso: Gasto '{item}' no valor de R$ '{valor} registrado na data '{data}', metodo pagamento: '{metodo_pagamento}'"
    
    except sqlite3.OperationalError as e:
        return(f'Erro Operacional no Banco de Dados: {e}')
        