from app.utils import DB_PATH
import sqlite3
import os

def consultar_gastos():
    """Consulta os gastos e RETORNA uma string formatada para o Agente"""
    
    # Verificar a CONEXÃO com o Banco de Dados
    try:
        if not os.path.exists(DB_PATH):
            return 'O Banco de Dados ainda não existe! Nehum gasto registrado'
        
        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()

        # Executar comando SQL
        cursor.execute("""SELECT * FROM controle_financeiro""")
        conexao.commit()

        # Pegando todas as linhas do banco de dados
        resultados = cursor.fetchall()
        conexao.close()
        
        if not resultados:
            return 'A Tabela existe, mas não há gastos registrados.'
        
        relatorio = 'Histórico de Gastos Encontrados:\n'
        for gasto in resultados:
            relatorio += f'- ID: {gasto[0]} | Data: {gasto[5]} | Item: {gasto[1]} | Valor: R${gasto[2]} | Categoria: {gasto[3]}\n'
            
        return relatorio
        
    
    except sqlite3.OperationalError as e:
        return f'Erro ao acessar tabela: {e}'
