from app.utils import DB_PATH
import sqlite3

def remover_gastos(id_gasto: int):
    """Remove um gasto do banco de dados pelo ID.
    Retorna uma string explicando o resultado para a LLM."""

    try:
        # Verificar a CONEXÃO com o Banco de Dados
        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
    
    except sqlite3.OperationalError as e:
        return(f'Erro na CONEXÃO com o Banco de Dados: {e}')
    
    
    try:
        query = 'DELETE FROM controle_financeiro WHERE id_gasto = ?'
        cursor.execute(query, (id_gasto, ))
        
        if cursor.rowcount == 0:
            conexao.close()
            return f'Erro: Não foi encontrado nenhum gasto com o ID {id_gasto}. Nada foi apagado'
        
        conexao.commit()
        conexao.close()

        return f'Sucesso: O gasto com ID {id_gasto} foi removido com sucesso.'
    
    except sqlite3.OperationalError as e:
        return(f'Erro ao remover dado: {id_gasto} :{e}')
    