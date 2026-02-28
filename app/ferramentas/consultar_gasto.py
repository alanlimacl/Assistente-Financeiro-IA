from app.config import BANCO_DADOS
import sqlite3


def consultar_gastos(data_inicio: str, data_fim:str):
    """
    Consulta os gastos financeiros dentro de um intervalo de datas.
    
    IMPORTANTE: O agente deve converter qualquer pedido de mês (ex: 'Janeiro') 
    para as datas exatas de inicio e fim no formato YYYY-MM-DD.

    Args:
        data_inicio (str): A data inicial no formato YYYY-MM-DD.
        data_fim (str): A data final no formato YYYY-MM-DD.

    Returns:
        str: Um resumo dos gastos encontrados ou aviso de que nada foi achado.
    """
    
    print(f"\n🔍 DEBUG CONSULTA:")
    print(f"--> Buscando no arquivo: {BANCO_DADOS}") 
    print(f"--> Datas: {data_inicio} até {data_fim}")
   
    # Verificar a CONEXÃO com o Banco de Dados
    try:
        if not BANCO_DADOS.exists():
            return 'O Banco de Dados ainda não existe! Nehum gasto registrado'
        
        conexao = sqlite3.connect(BANCO_DADOS)
        cursor = conexao.cursor()

        # Executar comando SQL
        query = """ SELECT * 
                    FROM controle_financeiro
                    WHERE data BETWEEN ? AND ?
                """
      
        cursor.execute(query, (data_inicio, data_fim))
        conexao.commit()

        # Pegando todas as linhas do banco de dados
        resultados = cursor.fetchall()
        conexao.close()
        
        if not resultados:
            return 'Não há gastos registrado nesse periodo de tempo.'
        
        # Adicionando um limite nas consultas de dados. 
        # Para não sobrecarregar o Modelo, sendo assim, caso passe de 20 gastos, estará limitado a 20 gastos
        LIMITE_ITENS = 20
        total_encontrado = len(resultados)
        
        relatorio = f'Foram encontrados {total_encontrado} gastos neste periodo:\n'
        
        if total_encontrado > LIMITE_ITENS:
            relatorio += f'⚠️ Para manter a agilidade, estou mostrando apenas os {LIMITE_ITENS} primeiros. Diga ao usuário para olhar o painel completo no menu.\n\n'
        
        else:
            relatorio += 'Histórico de Gastos Encontrados:\n\n'
        
        for gasto in resultados[:LIMITE_ITENS]:
            relatorio += f'- ID: {gasto[0]} | Data: {gasto[5]} | Item: {gasto[1]} | Valor: R${gasto[2]:.2f} | Categoria: {gasto[3]}\n'
            
        return relatorio
        
    except sqlite3.OperationalError as e:
        return f'Erro ao acessar tabela: {e}'


if __name__ == '__main__':
    a = consultar_gastos(data_inicio='2026-02-01', data_fim='2026-02-23')
    print(a)