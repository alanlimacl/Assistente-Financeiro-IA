import sqlite3
from app.config import BANCO_DADOS
from typing import Optional
import os


def somar_gastos_periodo(data_inical: str, 
                         data_final: str, 
                         categoria: Optional[str] = None) -> str:
    
    """ Ferramenta para somar o valor total de gastos em um período.
    Args:
        data_inicio (str): A data inicial no formato YYYY-MM-DD.
        data_fim (str): A data final no formato YYYY-MM-DD.
        categoria (str, opcional): A categoria para filtrar a soma (ex: 'Alimentação').
        
    Returns:
        str: Uma frase curta com o valor total somado."""
   
    try:
        if not os.path.exists(BANCO_DADOS):
            return 'Erro: O Banco de Dados não existe!'
        
        conexao = sqlite3.connect(BANCO_DADOS)
        cursor = conexao.cursor()
        
        if categoria:
            query = """ 
                    SELECT SUM(valor)
                    FROM controle_financeiro
                    WHERE data BETWEEN ? AND ? AND categoria LIKE ?         
                    """
            cursor.execute(query, (data_inical, data_final, categoria))
            
        else:
            query = """
                    SELECT SUM(valor)
                    FROM controle_financeiro
                    WHERE data BETWEEN ? AND ?
                    """
            cursor.execute(query, (data_inical, data_final))
            
        resultado = cursor.fetchone()[0]
        conexao.close()
        
        if resultado is None:
            return f'O valor total de gasto é R$ 0,00'

        return f'O valor total gasto é R$ {resultado:.2f}.'
    
    except sqlite3.Error as e:
        return f"Erro ao realizar a conexão: {e}"


if __name__ == '__main__':
    a = somar_gastos_periodo('2026-02-01', '2026-02-25')
    print(a)

